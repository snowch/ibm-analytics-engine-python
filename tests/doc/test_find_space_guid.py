import sys
import os
import tempfile
import json

curfilePath = os.path.abspath(__file__)
scriptDir = os.path.abspath(os.path.join(curfilePath, os.pardir, os.pardir, os.pardir, 'docs', 'example_scripts'))

from unittest import TestCase
from mock import Mock, MagicMock
import mock

class MockResponse:
    def __init__(self, json_data, status_code):
        self.json_data = json_data
        self.status_code = status_code
    def raise_for_status(self):
        return
    def json(self):
        return self.json_data

class DocExampleScripts_Test(TestCase):

    def mocked_requests_get(*args, **kwargs):
        if args[0] == 'https://api.ng.bluemix.net/v2/info':
            return MockResponse({"authorization_endpoint": "https://login.ng.bluemix.net/UAALoginServerWAR"}, 200)
        if args[0] == 'https://api.ng.bluemix.net/v2/organizations?q=name:your_org_name':
            return MockResponse({ "total_results": 1, "resources": [{ "metadata": { "guid": '1234567890' }}]}, 200)
        if args[0] == 'https://api.ng.bluemix.net/v2/spaces?q:organization_guid=1234567890':
            return MockResponse({ "total_results": 1, "resources": [{ "metadata": { "guid": '1234567890' }, "entity": { "name": "your_space_name" }}]}, 200)

        raise RuntimeError("Should not reach here: url {} ".format(args[0]))

    def mocked_requests_post(*args, **kwargs):
        if args[0] == 'https://login.ng.bluemix.net/UAALoginServerWAR/oauth/token':
            return MockResponse({'access_token': 'aaaaa', 'token_type': 'bearer', 'refresh_token': 'aaaaa', 'expires_in': 1209599}, 200)

        raise RuntimeError("Should not reach here: url {} ".format(args[0]))

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test(self, mock_get, mock_post):

        tmp = tempfile.NamedTemporaryFile(delete=True)
        try:
            data = json.dumps({
                "name": "iae-key",
                "description": "",
                "createdAt": "2017-11-14T12:30+0000",
                             "apiKey": ""
            }).encode('utf-8')
            tmp.write(data)
            tmp.flush()

            from ibm_analytics_engine import cf
            class MonkeyPatchedCloudFoundryAPI(cf.client.CloudFoundryAPI):
                def __init__(self, api_key_filename=None):
                    super(self.__class__, self).__init__(api_key_filename=tmp.name)
            cf.client.CloudFoundryAPI = MonkeyPatchedCloudFoundryAPI

            sys.path.append(os.path.abspath(os.path.join(scriptDir)))
            import find_space_guid

            #try:
            #    # Python 2x
            #    execfile(scriptfile, globals(), locals())
            #except:
            #    # Python 3x
            #    exec(open(scriptfile).read(), globals(), locals())
        finally:
            tmp.close()  # deletes the file
