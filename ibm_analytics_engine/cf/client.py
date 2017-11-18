from __future__ import absolute_import

from .logger import Logger

from .service_instances import ServiceInstance
from .service_keys import ServiceKey
from .spaces import Space
from .organizations import Organization

import requests
import json
from datetime import datetime, timedelta


class CloudFoundryAPI:

    def __init__(self, api_key=None, api_key_filename=None, api_endpoint='https://api.ng.bluemix.net', provision_poll_timeout_mins=30):

        self.log = Logger().get_logger(self.__class__.__name__)
        self.provision_poll_timeout_mins = provision_poll_timeout_mins 

        assert api_key is not None or api_key_filename is not None, "You must provide a value for api_key or for api_key_filename"

        if api_key_filename is not None:
            try:
                with open(api_key_filename, 'r') as api_file:
                    d = json.load(api_file)
                    self.api_key = d['apiKey']
            except:
                self.log.error('Error retrieving "apiKey" from file {}'.format(api_key_filename))
                raise
        else:
            self.api_key = api_key

        self.api_endpoint = api_endpoint
        self.info = self._get_info()

        self.service_instances = ServiceInstance(self)
        self.service_keys = ServiceKey(self)
        self.spaces = Space(self)
        self.organizations = Organization(self)

    def auth(self):
        self.log.debug('Authenticating to CloudFoundry')
        url = self.info['authorization_endpoint'] + '/oauth/token'
        headers = { 
                    'Content-Type': 'application/x-www-form-urlencoded;charset=utf-8',
                    'Accept': 'application/x-www-form-urlencoded;charset=utf-8', 
                    'Authorization': 'Basic Y2Y6'
                }
        data = 'grant_type=password&username=apikey&password={}'.format(self.api_key)
        try:
            response = requests.post(url, headers=headers, data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log.error('Cloud Foundry Auth Response: ' + response.text)
            raise

        self.auth_token = response.json()
        self.expires_at = datetime.now() + timedelta(seconds=self.auth_token['expires_in']/60)
        self.log.debug('Authenticated to CloudFoundry')

    def get_oidc_token(self):
        self.log.debug('Authenticating to CloudFoundry')

        auth_token = self.get_auth_token()
        refresh_token = auth_token['refresh_token']
        access_token = auth_token['access_token']
        token_type = auth_token['token_type']

        url='https://iam.bluemix.net/identity/token'
        data="grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={}".format(self.api_key)

        try:
            #response = requests.post(url, headers=headers, data=data)
            response = requests.post(url, data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log.error('Cloud Foundry Auth Response: ' + response.text)
            raise

        self.oidc_token = response.json()
        #self.expires_at = datetime.now() + timedelta(seconds=self.auth_token['expires_in']/60)
        self.log.debug('Authenticated to CloudFoundry')
        return self.oidc_token


    def get_auth_token(self):
        if not hasattr(self, 'auth_token') or datetime.now() > self.expires_at:
            self.auth()
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
            self.log.error('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, response.text))
            raise

        try:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, json.dumps(response.json())))
        except ValueError:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, response.text))

        return response

    def _get_info(self):
        url = '{}/v2/info'.format(self.api_endpoint)
        response = self._request(url=url, http_method='get', description='_get_info', create_auth_headers=False)
        return response.json()

    def print_orgs_and_spaces(self):
        spaces_json = self.spaces.get_spaces()
        organizations_json = self.organizations.get_organizations()
        def get_spaces(organization_guid, spaces_json):
            spaces = []
            for spc in spaces_json['resources']:
                if spc['entity']['organization_guid'] == organization_guid:
                    spaces.append(spc)
            return spaces

        for organization in organizations_json['resources']:
            print('name:{} organization_guid:{}'.format(organization['entity']['name'], organization['metadata']['guid']))
            for space in get_spaces(organization['metadata']['guid'], spaces_json):
                print('\tname:{} space_guid:{}'.format(space['entity']['name'], space['metadata']['guid']))
            print()

