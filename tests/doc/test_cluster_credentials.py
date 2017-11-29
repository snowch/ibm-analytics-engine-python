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
    """ Test getting credentials when credentials exist on the cluster """

    def mocked_requests_get(*args, **kwargs):
        if args[0] == 'https://api.ng.bluemix.net/v2/info':
            return MockResponse({"authorization_endpoint": "https://login.ng.bluemix.net/UAALoginServerWAR"}, 200)
        if args[0] == 'https://api.ng.bluemix.net/v2/service_keys?q=service_instance_guid:12345-12345-12345-12345':
            return MockResponse(
                {"total_results": 1, "resources": [{"metadata": {"guid": "1234567890"}, "entity": {"name": "Credentials-1", "service_instance_guid": "1234567890", "credentials": {"cluster_management": {"api_url": "https://api.dataplatform.ibm.com/v2/analytics_engines/1234567890", "instance_id": "1234567890"}, "cluster": {"cluster_id": "20171117-222539-855-AibSBgvm", "user": "clsadmin", "password": "XXXXXXX", "service_endpoints": {"ambari_console": "https://testhostname:9443", "livy": "https://testhostname:8443/gateway/default/livy/v1/batches", "spark_history_server": "https://testhostname:8443/gateway/default/sparkhistory", "oozie_rest": "https://testhostname:8443/gateway/default/oozie", "hive_jdbc": "jdbc:hive2://testhostname:8443/;ssl=true;transportMode=http;httpPath=gateway/default/hive", "notebook_gateway_websocket": "wss://testhostname:8443/gateway/default/jkgws/", "notebook_gateway": "https://testhostname:8443/gateway/default/jkg/", "webhdfs": "https://testhostname:8443/gateway/default/webhdfs/v1/", "ssh": "ssh clsadmin@testhostname", "spark_sql": "jdbc:hive2://testhostname:8443/;ssl=true;transportMode=http;httpPath=gateway/default/spark"}, "service_endpoints_ip": {"ambari_console": "https://1.1.1.1:9443", "livy": "https://1.1.1.1:8443/gateway/default/livy/v1/batches", "spark_history_server": "https://1.1.1.1:8443/gateway/default/sparkhistory", "oozie_rest": "https://1.1.1.1:8443/gateway/default/oozie", "hive_jdbc": "jdbc:hive2://1.1.1.1:8443/;ssl=true;transportMode=http;httpPath=gateway/default/hive", "notebook_gateway_websocket": "wss://1.1.1.1:8443/gateway/default/jkgws/", "notebook_gateway": "https://1.1.1.1:8443/gateway/default/jkg/", "webhdfs": "https://1.1.1.1:8443/gateway/default/webhdfs/v1/", "ssh": "ssh clsadmin@1.1.1.1", "spark_sql": "jdbc:hive2://1.1.1.1:8443/;ssl=true;transportMode=http;httpPath=gateway/default/spark"}}}}}]}, 200)
        raise RuntimeError("Unhandle GET request: " + args[0]) 

    def mocked_requests_post(*args, **kwargs):
        if args[0] == 'https://login.ng.bluemix.net/UAALoginServerWAR/oauth/token':
            return MockResponse({'access_token': 'aaaaa', 'token_type': 'bearer', 'refresh_token': 'aaaaa', 'expires_in': 1209599}, 200)
        if args[0] == 'https://api.ng.bluemix.net/v2/service_keys?q=service_instance_guid:12345-12345-12345-12345':
            return MockResponse(
                {"metadata": {"guid": "1234567890", "url": "/v2/service_keys/1234567890", "created_at": "2017-11-17T22:48:03Z", "updated_at": "2017-11-17T22:48:03Z"}, "entity": {"name": "Credentials-1", "service_instance_guid": "1234567890", "credentials": {"cluster_management": {"api_url": "https://api.dataplatform.ibm.com/v2/analytics_engines/1234567890", "instance_id": "1234567890"}, "cluster": {"cluster_id": "1234567890", "user": "clsadmin", "password": "XXXXXXXX", "service_endpoints": {"ambari_console": "https://testhost:9443", "livy": "https://testhost:8443/gateway/default/livy/v1/batches", "spark_history_server": "https://testhost:8443/gateway/default/sparkhistory", "oozie_rest": "https://testhost:8443/gateway/default/oozie", "hive_jdbc": "jdbc:hive2://testhost:8443/;ssl=true;transportMode=http;httpPath=gateway/default/hive", "notebook_gateway_websocket": "wss://testhost:8443/gateway/default/jkgws/", "notebook_gateway": "https://testhost:8443/gateway/default/jkg/", "webhdfs": "https://testhost:8443/gateway/default/webhdfs/v1/", "ssh": "ssh clsadmin@testhost", "spark_sql": "jdbc:hive2://testhost:8443/;ssl=true;transportMode=http;httpPath=gateway/default/spark"}, "service_endpoints_ip": {"ambari_console": "https://1.1.1.1:9443", "livy": "https://1.1.1.1:8443/gateway/default/livy/v1/batches", "spark_history_server": "https://1.1.1.1:8443/gateway/default/sparkhistory", "oozie_rest": "https://1.1.1.1:8443/gateway/default/oozie", "hive_jdbc": "jdbc:hive2://1.1.1.1:8443/;ssl=true;transportMode=http;httpPath=gateway/default/hive", "notebook_gateway_websocket": "wss://1.1.1.1:8443/gateway/default/jkgws/", "notebook_gateway": "https://1.1.1.1:8443/gateway/default/jkg/", "webhdfs": "https://1.1.1.1:8443/gateway/default/webhdfs/v1/", "ssh": "ssh clsadmin@1.1.1.1", "spark_sql": "jdbc:hive2://1.1.1.1:8443/;ssl=true;transportMode=http;httpPath=gateway/default/spark"}}}, "service_instance_url": "/v2/service_instances/1234567890"}}, 200)

        raise RuntimeError("Unhandle POST request: " + args[0]) 

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
        
            from ibm_analytics_engine import CloudFoundryAPI
            CloudFoundryAPI.api_key_filename = tmp.name

            sys.path.append(os.path.abspath(os.path.join(scriptDir)))
            import cluster_credentials
            
        finally:
            tmp.close()  # deletes the file
            if hasattr(CloudFoundryAPI, 'api_key_filename'):
                del CloudFoundryAPI.api_key_filename

class DocExampleScripts2_Test(TestCase):
    """ Test getting credentials when none exist """

    def mocked_requests_get(*args, **kwargs):
        if args[0] == 'https://api.ng.bluemix.net/v2/info':
            return MockResponse({"authorization_endpoint": "https://login.ng.bluemix.net/UAALoginServerWAR"}, 200)
        if args[0] == 'https://api.ng.bluemix.net/v2/service_keys?q=service_instance_guid:12345-12345-12345-12345':
            return MockResponse(
                {"total_results": 0, "total_pages": 1, "prev_url": None, "next_url": None, "resources": []}, 200)
        raise RuntimeError("Unhandle GET request: " + args[0]) 

    def mocked_requests_post(*args, **kwargs):
        if args[0] == 'https://login.ng.bluemix.net/UAALoginServerWAR/oauth/token':
            return MockResponse({'access_token': 'aaaaa', 'token_type': 'bearer', 'refresh_token': 'aaaaa', 'expires_in': 1209599}, 200)
        if args[0] == 'https://api.ng.bluemix.net/v2/service_keys?q=service_instance_guid:1234567890':
            return MockResponse(
                {"metadata": {"guid": "1234567890", "url": "/v2/service_keys/1234567890", "created_at": "2017-11-17T22:48:03Z", "updated_at": "2017-11-17T22:48:03Z"}, "entity": {"name": "Credentials-1", "service_instance_guid": "1234567890", "credentials": {"cluster_management": {"api_url": "https://api.dataplatform.ibm.com/v2/analytics_engines/1234567890", "instance_id": "1234567890"}, "cluster": {"cluster_id": "1234567890", "user": "clsadmin", "password": "XXXXXXXX", "service_endpoints": {"ambari_console": "https://testhost:9443", "livy": "https://testhost:8443/gateway/default/livy/v1/batches", "spark_history_server": "https://testhost:8443/gateway/default/sparkhistory", "oozie_rest": "https://testhost:8443/gateway/default/oozie", "hive_jdbc": "jdbc:hive2://testhost:8443/;ssl=true;transportMode=http;httpPath=gateway/default/hive", "notebook_gateway_websocket": "wss://testhost:8443/gateway/default/jkgws/", "notebook_gateway": "https://testhost:8443/gateway/default/jkg/", "webhdfs": "https://testhost:8443/gateway/default/webhdfs/v1/", "ssh": "ssh clsadmin@testhost", "spark_sql": "jdbc:hive2://testhost:8443/;ssl=true;transportMode=http;httpPath=gateway/default/spark"}, "service_endpoints_ip": {"ambari_console": "https://1.1.1.1:9443", "livy": "https://1.1.1.1:8443/gateway/default/livy/v1/batches", "spark_history_server": "https://1.1.1.1:8443/gateway/default/sparkhistory", "oozie_rest": "https://1.1.1.1:8443/gateway/default/oozie", "hive_jdbc": "jdbc:hive2://1.1.1.1:8443/;ssl=true;transportMode=http;httpPath=gateway/default/hive", "notebook_gateway_websocket": "wss://1.1.1.1:8443/gateway/default/jkgws/", "notebook_gateway": "https://1.1.1.1:8443/gateway/default/jkg/", "webhdfs": "https://1.1.1.1:8443/gateway/default/webhdfs/v1/", "ssh": "ssh clsadmin@1.1.1.1", "spark_sql": "jdbc:hive2://1.1.1.1:8443/;ssl=true;transportMode=http;httpPath=gateway/default/spark"}}}, "service_instance_url": "/v2/service_instances/1234567890"}}, 200)
        if args[0] == 'https://api.ng.bluemix.net/v2/service_keys':
            return MockResponse(
                { "metadata": { "guid": "1234567890", "url": "/v2/service_keys/1234567890", "created_at": "2016-06-08T16:41:22Z", "updated_at": "2016-06-08T16:41:26Z" }, "entity": { "name": "name-127", "service_instance_guid": "1234567890", "credentials": { "creds-key-3": "creds-val-3" }, "service_instance_url": "/v2/service_instances/1234567890" } }, 200)
        raise RuntimeError("Unhandle POST request: " + args[0]) 

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
        
            from ibm_analytics_engine import CloudFoundryAPI
            CloudFoundryAPI.api_key_filename = tmp.name

            sys.path.append(os.path.abspath(os.path.join(scriptDir)))
            import cluster_credentials
            
        finally:
            tmp.close()  # deletes the file
            if hasattr(CloudFoundryAPI, 'api_key_filename'):
                del CloudFoundryAPI.api_key_filename
