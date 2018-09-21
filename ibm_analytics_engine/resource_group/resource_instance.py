from __future__ import absolute_import

from .logger import Logger

from datetime import datetime, timedelta
import time
import requests
import json

class ResourceInstance:

    def __init__(self, cf_client):
        self.cf_client = cf_client

    def create(self, data):

        url = 'https://resource-controller.ng.bluemix.net/v1/resource_instances'
        response = self.cf_client._request(url=url, http_method='post', description='create_resource_instances', data=data)
        return response.json()

    def poll_for_completion(self, service_instance_id):
        url = '{}/v2/service_instances/{}'.format(self.cf_client.api_endpoint, service_instance_id)
        headers = self.cf_client._request_headers()
        
        poll_start = datetime.now()

        # Status codes: https://apidocs.cloudfoundry.org/245/service_instances/creating_a_service_instance.html
        status = 'in progress'
        while status == 'in progress':

            if (datetime.now() - poll_start).seconds > (self.cf_client.provision_poll_timeout_mins * 60):
                raise TimeoutError('Failed to provision with {} minutes'.format(self.cf_client.provision_poll_timeout_mins))

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()

                d = response.json()
                last_operation = d['entity']['last_operation']
                self.cf_client.log.debug('Poll status response for service_instance_guid: {} : {}'.format(service_instance_id,  str(last_operation)))

                if last_operation['type'] == 'create':
                    status = last_operation['state']
            except requests.exceptions.RequestException as e:
                self.cf_client.log.error('Service Provision Status Response: ' + response.text)
                raise

            time.sleep(30)

        self.cf_client.log.debug('provisioning completed: ' + status)

        # returns succeeded or failed
        return status

