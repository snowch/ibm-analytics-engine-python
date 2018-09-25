from __future__ import absolute_import

from .logger import Logger
from .ibm_cloud_region import Region

from .resource_controller import ResourceController
from .analytics_engines import AnalyticsEngines


import requests
import json
from datetime import datetime, timedelta

import sys
PY3 = sys.version_info[0] == 3

if PY3:
    string_types = str
else:
    string_types = basestring

class AnalyticsEngineException(Exception):
    def __init__(self, message, *args):
        self.message = message
        super( AnalyticsEngineException, self).__init__(message, *args) 

class AnalyticsEngine(object):

    def __init__(self, 
                 api_key = None, 
                 api_key_filename = None,
                 region = 'us-south',
                 provision_poll_timeout_mins = 30):

        self.log = Logger().get_logger(self.__class__.__name__)
        self.provision_poll_timeout_mins = provision_poll_timeout_mins 

        assert api_key is not None or api_key_filename is not None, "You must provide a value for api_key or for api_key_filename"
        
        assert isinstance(region, string_types), "region parameter must be of type string"

        # allow tests to override the api_key_filename parameter
        if hasattr(AnalyticsEngine, 'api_key_filename') and AnalyticsEngine is not None:
            api_key_filename = AnalyticsEngine.api_key_filename

        if api_key_filename is not None:
            try:
                with open(api_key_filename, 'r') as api_file:
                    d = json.load(api_file)
                    try:
                        self.api_key = d['apikey']
                    except KeyError:
                        # The attibute name used to be
                        self.api_key = d['apiKey']

            except:
                self.log.error('Error retrieving "apiKey" from file {}'.format(api_key_filename))
                raise
        else:
            self.api_key = api_key

        self.region = Region(region)
        self.api_endpoint = self.region.api_endpoint()
        self.iam_endpoint = self.region.iam_endpoint()

        self.resource_controller = ResourceController(self, self.region)
        self.analytics_engines = AnalyticsEngines(self, self.region)


    def _auth(self):
        
        self.log.debug('Authenticating to IAM')
        url = self.iam_endpoint + '/identity/token'
        data = "apikey={}&grant_type=urn%3Aibm%3Aparams%3Aoauth%3Agrant-type%3Aapikey".format(self.api_key)
        headers = { 
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": "Basic Yng6Yng=" 
            }
        
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log.error('IAM Auth Response: ' + response.text)
            # TODO we should define a custom application exception for this
            raise

        self.auth_token = response.json()
        self.expires_at = datetime.now() + timedelta(seconds=self.auth_token['expires_in']/60)
        self.log.debug('Authenticated to IAM')

    def get_auth_token(self):
        if not hasattr(self, 'auth_token') or not hasattr(self, 'expires_at') or datetime.now() > self.expires_at:
            self._auth()
        return self.auth_token

    def _request_headers(self):

        auth_token = self.get_auth_token()
        access_token = auth_token['access_token']
        token_type = auth_token['token_type']

        headers = {
            'accept': 'application/json',
            'authorization': '{} {}'.format(token_type, access_token),
            'cache-control': 'no-cache', 
            'content-type': 'application/json'
            }
        return headers

    def _request(self, url, http_method='get', data=None, description='', create_auth_headers=True):
        if create_auth_headers:
            headers = self._request_headers()
        else:
            headers = {}
        try:
            if http_method == 'get':
                response = requests.get(url, headers=headers)
            elif http_method == 'post':
                response = requests.post(url, headers=headers, data=json.dumps(data))
            elif http_method == 'delete':
                response = requests.delete(url, headers=headers)

            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, response.text))
            raise AnalyticsEngineException(message=response.text)

        try:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, json.dumps(response.json())))
        except ValueError:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, response.text))

        return response

        
    def create(self, data):
        return self.resource_controller.create(data)
        
    def cluster_status(self, instance_id, wait_until_finished_preparing = False):
        if wait_until_finished_preparing is True:
            # Wait until status is no longer 'Preparing' 
            return self.analytics_engines.poll_for_completion(instance_id)
        else:
            return self.analytics_engines.cluster_status(instance_id)
