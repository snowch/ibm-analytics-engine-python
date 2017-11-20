from __future__ import absolute_import

from .logger import Logger

import requests
import json
from datetime import datetime, timedelta


class DataPlatformAPI:

    def __init__(self, cf_client):
        assert cf_client is not None
        self.cf_client = cf_client
        self.log = Logger().get_logger(self.__class__.__name__)

    def _request_headers(self):
        iam_token = self.cf_client.get_oidc_token()['access_token']
        headers = { 'Authorization': 'Bearer {}'.format(iam_token) }
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

    def status(self, vcap):
        api_url = vcap['cluster_management']['api_url'] + '/state'
        response = self._request(url=api_url, http_method='get', description='status')
        return response.json()
