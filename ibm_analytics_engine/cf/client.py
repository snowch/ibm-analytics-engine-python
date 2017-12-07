from __future__ import absolute_import

from .logger import Logger

from .service_instances import ServiceInstance
from .service_keys import ServiceKey
from .spaces import Space
from .organizations import Organization

import requests
import json
from datetime import datetime, timedelta

class CloudFoundryException(Exception):
    def __init__(self, message, *args):
        self.message = message
        super(CloudFoundryException, self).__init__(message, *args) 


class CloudFoundryAPI(object):

    def __init__(self, api_key=None, api_key_filename=None, api_endpoint='https://api.ng.bluemix.net', provision_poll_timeout_mins=30):

        self.log = Logger().get_logger(self.__class__.__name__)
        self.provision_poll_timeout_mins = provision_poll_timeout_mins 

        assert api_key is not None or api_key_filename is not None, "You must provide a value for api_key or for api_key_filename"

        # allow tests to override the api_key_filename parameter
        if hasattr(CloudFoundryAPI, 'api_key_filename') and CloudFoundryAPI is not None:
            api_key_filename = CloudFoundryAPI.api_key_filename

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
            # TODO we should define a custom application exception for this
            raise

        self.auth_token = response.json()
        self.expires_at = datetime.now() + timedelta(seconds=self.auth_token['expires_in']/60)
        self.log.debug('Authenticated to CloudFoundry')

    def oidc_token(self):
        self.log.debug('Retrieving IAM token')

        url='https://iam.bluemix.net/identity/token'
        data="grant_type=urn:ibm:params:oauth:grant-type:apikey&apikey={}".format(self.api_key)

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            self.log.error('IAM token response: ' + response.text)
            raise

        self.oidc_token = response.json()
        self.oidc_expires_at = datetime.now() + timedelta(seconds=self.oidc_token['expires_in']/60)
        self.log.debug('Retrieved IAM token')
        return self.oidc_token

    def get_auth_token(self):
        if not hasattr(self, 'auth_token') or not hasattr(self, 'expires_at') or datetime.now() > self.expires_at:
            self.auth()
        return self.auth_token

    def get_oidc_token(self):
        if not hasattr(self, 'oidc_token') or not hasattr(self, 'oidc_expires_at') or datetime.now() > self.oidc_expires_at:
            self.oidc_token()
        return self.oidc_token

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
            raise CloudFoundryException(message=response.text)

        try:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, json.dumps(response.json())))
        except ValueError:
            self.log.debug('{} : {} {} : {} {}'.format(description, http_method, url, response.status_code, response.text))

        return response

    def _get_info(self):
        url = '{}/v2/info'.format(self.api_endpoint)
        response = self._request(url=url, http_method='get', description='_get_info', create_auth_headers=False)
        return response.json()

    def space_guid(self, org_name, space_name):

        assert org_name is not None, "org_name must be provided"
        assert space_name is not None, "space_name must be provided"

        org_json = self.organizations.get_organizations(org_name)
        # Organisation names should be unique - there should only be one result
        if org_json['total_results'] != 1:
            raise ValueError('organization name "{}" was not found'.format(org_name))
        org_guid = org_json['resources'][0]['metadata']['guid']

        space_filter_string = 'q:organization_guid={}'.format(org_guid)
        spaces_json = self.spaces.get_spaces(filter_string=space_filter_string)
        if spaces_json['total_results'] == 0:
            raise ValueError('no spaces found for orgnaization "{}"'.format(org_name))

        for spc in spaces_json['resources']:
            if spc['entity']['name'] == space_name:
                return spc['metadata']['guid']

        raise ValueError('space "{}" not found for organization "{}"'.format(space_name, org_name))

    def orgs_and_spaces(self, org_name=None, space_name=None):
        if space_name is not None:
            spaces_json = self.spaces.get_spaces(name=space_name)
        else:
            spaces_json = self.spaces.get_spaces()

        if org_name is not None:
            organizations_json = self.organizations.get_organizations(org_name)
        else:
            organizations_json = self.organizations.get_organizations()

        def get_spaces_for_org(organization_guid, spaces_json):
            spaces = []
            for spc in spaces_json['resources']:
                if spc['entity']['organization_guid'] == organization_guid:
                    spaces.append(spc)
            return spaces

        orgs_and_spaces = []
        for organization in organizations_json['resources']:
            spaces = []
            for space in get_spaces_for_org(organization['metadata']['guid'], spaces_json):
                spaces.append({ 'name': space['entity']['name'], 'guid': space['metadata']['guid'] })
            orgs_and_spaces.append({ 'name': organization['entity']['name'], 'guid': organization['metadata']['guid'], 'spaces': spaces })

        return orgs_and_spaces

    def print_orgs_and_spaces(self, org_name=None, space_name=None):
        oas = self.orgs_and_spaces(org_name, space_name)
        max_len = 0
        for o in oas:
            if len(o['name']) > max_len:
                max_len = len(o['name'])
            for s in o['spaces']:
                if len(s['name']) > max_len:
                    max_len = len(s['name'])

        for o in oas:
            orgname=o['name']
            orgguid=o['guid']
            format='Org: {orgname:{width}}   {orgguid}'.format(orgname=orgname, width=max_len, orgguid=orgguid)
            print('-' * len(format))
            print(format)
            for s in o['spaces']:
                spcname=s['name']
                spcguid=s['guid']
                print('> Spc: {spcname:{width}} {spcguid}'.format(spcname=spcname, width=max_len, spcguid=spcguid))
