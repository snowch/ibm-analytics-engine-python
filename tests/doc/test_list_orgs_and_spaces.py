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
        if args[0] == 'https://api.ng.bluemix.net/v2/spaces':
            return MockResponse(
                    {"total_results": 1, "total_pages": 1, "prev_url": None, "next_url": None, "resources": [{"metadata": {"guid": "1234567890", "url": "/v2/spaces/1234567890", "created_at": "2014-07-21T06:11:34Z", "updated_at": "2017-11-03T18:41:30Z"}, "entity": {"name": "dev", "organization_guid": "1234567890", "space_quota_definition_guid": None, "isolation_segment_guid": None, "allow_ssh": True, "organization_url": "/v2/organizations/1234567890", "developers_url": "/v2/spaces/1234567890/developers", "managers_url": "/v2/spaces/1234567890/managers", "auditors_url": "/v2/spaces/1234567890/auditors", "apps_url": "/v2/spaces/1234567890/apps", "routes_url": "/v2/spaces/1234567890/routes", "domains_url": "/v2/spaces/1234567890/domains", "service_instances_url": "/v2/spaces/1234567890/service_instances", "app_events_url": "/v2/spaces/1234567890/app_events", "events_url": "/v2/spaces/1234567890/events", "security_groups_url": "/v2/spaces/1234567890/security_groups", "staging_security_groups_url": "/v2/spaces/1234567890/staging_security_groups"}}]}, 200)
        if args[0] == 'https://api.ng.bluemix.net/v2/organizations':
            return MockResponse(
                    {"total_results": 1, "total_pages": 1, "prev_url": None, "next_url": None, "resources": [{"metadata": {"guid": "1234567890", "url": "/v2/organizations/1234567890", "created_at": "2014-07-21T06:11:35Z", "updated_at": "2017-11-03T18:41:31Z"}, "entity": {"name": "rvaidya@us.ibm.com", "billing_enabled": True, "quota_definition_guid": "1234567890", "status": "active", "default_isolation_segment_guid": None, "quota_definition_url": "/v2/quota_definitions/1234567890", "spaces_url": "/v2/organizations/1234567890/spaces", "domains_url": "/v2/organizations/9b2/domains", "private_domains_url": "/v2/organizations/9b2/private_domains", "users_url": "/v2/organizations/1234567890/users", "managers_url": "/v2/organizations/1234567890/managers", "billing_managers_url": "/v2/organizations/1234567890/billing_managers", "auditors_url": "/v2/organizations/1234567890/auditors", "app_events_url": "/v2/organizations/1234567890/app_events", "space_quota_definitions_url": "/v2/organizations/1234567890/space_quota_definitions"}}]}, 200)

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

            scriptfile = os.path.abspath(os.path.join(scriptDir, 'list_orgs_and_spaces.py'))
            try:
                # Python 2x
                execfile(scriptfile)
            except:
                # Python 3x
                exec(open(scriptfile).read())
        finally:
            tmp.close()  # deletes the file
