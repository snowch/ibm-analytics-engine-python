from __future__ import absolute_import

from .logger import Logger

from datetime import datetime, timedelta
import time
import requests
import json

class ServiceKey:

    def __init__(self, cf_client):
        self.cf_client = cf_client

    def get_service_keys(self, service_instance_guid, name=None):
        if name:
            url = '{}/v2/service_keys?q=service_instance_guid:{}&q=name:{}'.format(self.cf_client.api_endpoint, service_instance_guid, name)
        else:
            url = '{}/v2/service_keys?q=service_instance_guid:{}'.format(self.cf_client.api_endpoint, service_instance_guid)

        response = self.cf_client._request(url=url, http_method='get', description='get_service_keys')
        return response.json()

    def create_service_key(self, service_instance_guid, name='Credentials-1'):
        url = '{}/v2/service_keys'.format(self.cf_client.api_endpoint)
        data = {
            "service_instance_guid": service_instance_guid, 
            "name": name, 
            }
        response = self.cf_client._request(url=url, http_method='post', data=data, description='create_service_key')
        return response.json()

