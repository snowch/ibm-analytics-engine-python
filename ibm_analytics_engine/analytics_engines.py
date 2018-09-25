from __future__ import absolute_import

from .logger import Logger

from datetime import datetime, timedelta
import time
import requests
import json

class AnalyticsEngines:

    def __init__(self, client, region):
        self.client = client
        self.region = region
    
    def cluster_status(self, instance_id):
        url = self.region.iae_endpoint() + '/v2/analytics_engines/{}/state'.format(instance_id)
        response = self.client._request(url=url, http_method='get', description='cluster_status')
        return response.json()
    
    def poll_for_completion(self, instance_id):
        url = self.region.iae_endpoint() + '/v2/analytics_engines/{}/state'.format(instance_id)
        headers = self.client._request_headers()
        
        provision_poll_timeout_mins = self.client.provision_poll_timeout_mins
        
        poll_start = datetime.now()
        
        # Status codes: https://console.bluemix.net/docs/services/AnalyticsEngine/track-instance-provisioning.html#tracking-the-status-of-the-cluster-provisioning
        
        status = self.cluster_status(instance_id)['state']
        while status == 'Preparing':

            if (datetime.now() - poll_start).seconds > (provision_poll_timeout_mins * 60):
                raise TimeoutError('Failed to provision with {} minutes'.format(provision_poll_timeout_mins))

            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()

                d = response.json()
                status = d['state']
       
            except requests.exceptions.RequestException as e:
                self.client.log.error('Service Provision Status Response: ' + response.text)
                raise

            time.sleep(30)

        self.client.log.debug('provisioning completed: ' + status)

        # returns current non-Preparing status
        return { 'state': status }

        