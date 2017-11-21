from __future__ import absolute_import

from .logger import Logger

from datetime import datetime, timedelta
import time
import requests
import json

class ServiceInstance:

    def __init__(self, cf_client):
        self.cf_client = cf_client

    def get_service_instances(self, space_guid):

        # https://apidocs.cloudfoundry.org/270/spaces/get_space_summary.html
        # TODO: 
        # - replace spaces call with https://apidocs.cloudfoundry.org/270/service_instances/list_all_service_instances.html
        #   note list_all_service_instances uses pagination

        url = '{}/v2/spaces/{}/summary'.format(self.cf_client.api_endpoint, space_guid)
        response = self.cf_client._request(url=url, http_method='get', description='get_service_instances')
        return response.json()['services']

    # TODO rename service_instance_id to service_instance_guid
    def delete_service_instance(self, service_instance_id, recursive=False):
        url = '{}/v2/service_instances/{}?recursive={}'.format(self.cf_client.api_endpoint, service_instance_id, json.dumps(recursive))
        response = self.cf_client._request(url=url, http_method='delete', description='delete_service_instances')
        return response

    # TODO rename to create_service_instance
    def provision(self, service_instance_name, service_plan_guid, space_guid, parameters, poll_for_completion=False):
        url = '{}/v2/service_instances?accepts_incomplete=true'.format(self.cf_client.api_endpoint)
        data = {
            "name": service_instance_name, 
            "space_guid": space_guid, 
            "service_plan_guid": service_plan_guid,
            "parameters": parameters
            }
        response = self.cf_client._request(url=url, http_method='post', data=data, description='provision')
        new_instance_guid = response.json()['metadata']['guid']
        if poll_for_completion:
            self.poll_for_completion(new_instance_guid)
        return response.json()

    def status(self, service_instance_id):
        url = '{}/v2/service_instances/{}'.format(self.cf_client.api_endpoint, service_instance_id)
        response = self.cf_client._request(url=url, http_method='get', description='get_status')
        return response.json()

    # TODO rename service_instance_id to service_instance_guid
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

