from __future__ import absolute_import

from .logger import Logger

class Organization:

    def __init__(self, cf_client):
        self.cf_client = cf_client

    def get_organizations(self, name=None):
        if name:
            url = '{}/v2/organizations?q=name:{}'.format(self.cf_client.api_endpoint, name)
        else:
            url = '{}/v2/organizations'.format(self.cf_client.api_endpoint)

        response = self.cf_client._request(url=url, http_method='get', description='get_space')
        return response.json()

