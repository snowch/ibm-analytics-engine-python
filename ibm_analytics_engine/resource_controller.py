from __future__ import absolute_import

from .logger import Logger

from datetime import datetime, timedelta
import time
import requests
import json

# API Docs https://console.stage1.bluemix.net/apidocs/resource-controller
class ResourceController:

    def __init__(self, client, region):
        self.client = client
        self.region = region

    def create(self, data):
        url = self.region.rc_endpoint() + '/v1/resource_instances'
        response = self.client._request(url=url, http_method='post', description='create_resource_instances', data=data)
        return response.json()
    
    def list(self):
        #TODO - 
        return
    
    def delete(self, instance_id):
        #TODO - 
        return

    # See https://console.bluemix.net/docs/services/AnalyticsEngine/Retrieve-service-credentials-and-service-end-points.html#obtaining-the-credentials-using-the-ibm-cloud-rest-api
    def create_credentials(self, instance_id, key_name, service_instance_name, role):
        url = self.region.rc_endpoint() + '/v1/resource_keys'
        data = {
            "name": key_name,
            "source_crn": service_instance_name,
            "parameters": {
                "role_crn": role
                }
            }
        response = self.client._request(url=url, http_method='post', description='create_credentials', data=data)
        return response.json()
        