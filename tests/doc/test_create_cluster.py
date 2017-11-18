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

        print('GET: ' + args[0]) 

        if args[0] == 'https://api.ng.bluemix.net/v2/info':
            return MockResponse({"authorization_endpoint": "https://login.ng.bluemix.net/UAALoginServerWAR"}, 200)
        elif args[0] == 'https://api.ng.bluemix.net/v2/service_instances/1234567890':
            return MockResponse(
                    {"metadata": {"guid": "1234567890", "url": "/v2/service_instances/1234567890", "created_at": "2017-11-16T15:23:26Z", "updated_at": "2017-11-16T15:23:26Z"}, "entity": {"name": "AE", "credentials": {}, "service_plan_guid": "acb06a56-fab1-4cb1-a178-c811bc676164", "space_guid": "1234567890", "gateway_data": None, "dashboard_url": "https://ibmae-ui.mybluemix.net/analytics/engines/paygo/jumpout?apiKey=1234567890", "type": "managed_service_instance", "last_operation": {"type": "create", "state": "succeeded", "description": "", "updated_at": "2017-11-16T15:23:26Z", "created_at": "2017-11-16T15:23:26Z"}, "tags": [], "service_guid": "1234567890", "space_url": "/v2/spaces/1234567890", "service_plan_url": "/v2/service_plans/1234567890", "service_bindings_url": "/v2/service_instances/1234567890/service_bindings", "service_keys_url": "/v2/service_instances/1234567890/service_keys", "routes_url": "/v2/service_instances/1234567890/routes", "service_url": "/v2/services/1234567890"}}, 200)

        raise RuntimeError("Should not reach here")

    def mocked_requests_post(*args, **kwargs):
        class MockResponse:
            def __init__(self, json_data, status_code):
                self.json_data = json_data
                self.status_code = status_code
            def raise_for_status(self):
                return
            def json(self):
                return self.json_data

        print('POST: ' + args[0])

        if args[0] == 'https://login.ng.bluemix.net/UAALoginServerWAR/oauth/token':
            return MockResponse({'access_token': 'aaaaa', 'token_type': 'bearer', 'refresh_token': 'aaaaa', 'expires_in': 1209599}, 200)
        elif args[0] == 'https://api.ng.bluemix.net/v2/service_instances?accepts_incomplete=true':
            return MockResponse(
                    {"metadata": {"guid": "1234567890", "url": "/v2/service_instances/1234567890", "created_at": "2017-11-16T15:23:26Z", "updated_at": "2017-11-16T15:23:26Z"}, "entity": {"name": "AE", "credentials": {}, "service_plan_guid": "acb06a56-fab1-4cb1-a178-c811bc676164", "space_guid": "1234567890", "gateway_data": None, "dashboard_url": "https://ibmae-ui.mybluemix.net/analytics/engines/paygo/jumpout?apiKey=1234567890", "type": "managed_service_instance", "last_operation": {"type": "create", "state": "in progress", "description": "", "updated_at": "2017-11-16T15:23:26Z", "created_at": "2017-11-16T15:23:26Z"}, "tags": [], "service_guid": "1234567890", "space_url": "/v2/spaces/1234567890", "service_plan_url": "/v2/service_plans/1234567890", "service_bindings_url": "/v2/service_instances/1234567890/service_bindings", "service_keys_url": "/v2/service_instances/1234567890/service_keys", "routes_url": "/v2/service_instances/1234567890/routes", "service_url": "/v2/services/1234567890"}}, 200)
        elif args[0] == 'https://api.ng.bluemix.net/v2/service_keys':
            return MockResponse(
                    {"metadata": {"guid": "1234567890", "url": "/v2/service_keys/1234567890", "created_at": "2017-11-16T15:33:52Z", "updated_at": "2017-11-16T15:33:52Z"}, "entity": {"name": "Credentials-1", "service_instance_guid": "1234567890", "credentials": {"cluster_management": {"api_url": "https://api.dataplatform.ibm.com/v2/analytics_engines/1234567890", "instance_id": "1234567890"}, "cluster": {"cluster_id": "1234567890", "user": "clsadmin", "password": "XXXXXXXXXX", "service_endpoints": {"ambari_console": "https://testhostname:9443", "livy": "https://testhostname:8443/gateway/default/livy/v1/batches", "spark_history_server": "https://testhostname:8443/gateway/default/sparkhistory", "notebook_gateway_websocket": "wss://testhostname:8443/gateway/default/jkgws/", "notebook_gateway": "https://testhostname:8443/gateway/default/jkg/", "webhdfs": "https://testhostname:8443/gateway/default/webhdfs/v1/", "ssh": "ssh clsadmin@testhostname"}, "service_endpoints_ip": {"ambari_console": "https://1.1.1.1:9443", "livy": "https://1.1.1.1:8443/gateway/default/livy/v1/batches", "spark_history_server": "https://1.1.1.1:8443/gateway/default/sparkhistory", "notebook_gateway_websocket": "wss://1.1.1.1:8443/gateway/default/jkgws/", "notebook_gateway": "https://1.1.1.1:8443/gateway/default/jkg/", "webhdfs": "https://1.1.1.1:8443/gateway/default/webhdfs/v1/", "ssh": "ssh clsadmin@1.1.1.1"}}}, "service_instance_url": "/v2/service_instances/1234567890"}}, 200)

        raise RuntimeError("Should not reach here")

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
        
            os.environ['API_KEY_FILENAME'] = tmp.name
            os.environ['SPACE_GUID'] = '12345'
            os.environ['CLUSTER_NAME'] = 'My_IAE'

            scriptfile = os.path.abspath(os.path.join(scriptDir, 'create_cluster.py'))
            try:
                # Python 2x
                execfile(scriptfile)
            except:
                # Python 3x
                exec(open(scriptfile).read())
        finally:
            tmp.close()  # deletes the file
