from __future__ import absolute_import

from .logger import Logger

class Space:

    def __init__(self, cf_client):
        self.cf_client = cf_client

    def get_spaces(self, name=None, filter_string=None):
        assert name is None or filter_string is None or \
               name is None and filter_string is None, "You can provide name or filter_string, but not both"

        if name:
            url = '{}/v2/spaces?q=name:{}'.format(self.cf_client.api_endpoint, name)
        elif filter_string:
            url = '{}/v2/spaces?{}'.format(self.cf_client.api_endpoint, filter_string)
        else:
            url = '{}/v2/spaces'.format(self.cf_client.api_endpoint)

        response = self.cf_client._request(url=url, http_method='get', description='get_space')
        return response.json()

