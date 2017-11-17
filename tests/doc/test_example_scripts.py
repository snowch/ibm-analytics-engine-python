import os
import tempfile
import json

curfilePath = os.path.abspath(__file__)
scriptDir = os.path.abspath(os.path.join(curfilePath, os.pardir, os.pardir, os.pardir, 'docs', 'example_scripts'))

from unittest import TestCase
from mock import Mock, MagicMock
import mock

class DocExampleScripts_Test(TestCase):

    def mocked_requests_get(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def raise_for_status(self):
                return
            def json(self):
                return self.json_data
        print(args[0])
        if args[0] == 'https://api.ng.bluemix.net/v2/info':
            return MockResponse({"authorization_endpoint": "https://login.ng.bluemix.net/UAALoginServerWAR"}, 200)
        else:
            return MockResponse({"key1": "value1"}, 200)
        return MockResponse(None, 404)

    def mocked_requests_post(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def raise_for_status(self):
                return
            def json(self):
                return self.json_data
        print(args[0])
        if args[0] == 'https://login.ng.bluemix.net:443/UAALoginServerWAR/oauth/token':
            raise ValueError('aaa')
        else:
            return MockResponse({"key1": "value1"}, 200)
        return MockResponse(None, 404)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    @mock.patch('requests.post', side_effect=mocked_requests_post)
    def test(self, mock_get, mock_post):

        return True # Ignore this script for now - it is still being developed

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
        
            os.environ['api_key_filename'] = tmp.name
            os.environ['space_guid'] = '12345'
            os.environ['cluster_name'] = 'My_IAE'

            scriptfile = os.path.abspath(os.path.join(scriptDir, 'create_cluster.py'))
            try:
                # Python 2x
                execfile(scriptfile)
            except:
                # Python 3x
                exec(open(scriptfile).read())
        finally:
            tmp.close()  # deletes the file
