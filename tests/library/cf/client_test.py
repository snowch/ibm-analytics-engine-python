from unittest import TestCase
from mock import Mock, patch

import sys
import tempfile
import os
import json
import requests
from requests.exceptions import RequestException
from ibm_analytics_engine import CloudFoundryAPI


class TestCloudFoundryAPI(TestCase):
    def test_invalid_api_key_file(self):
        try:
            error_class = IOError
        except BaseException:
            error_class = FileNotFoundError

        with self.assertRaises(error_class):
            cf = CloudFoundryAPI(api_key_filename='does_not_exist')

    def test_api_key_file(self):
        # delete=True means the file will be deleted on close
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
            cf = CloudFoundryAPI(api_key_filename=tmp.name)
        finally:
            tmp.close()  # deletes the file

class MockResponse:
    def __init__(self, json_data, status_code, raise_for_status_flag=False):
        self.json_data = json_data
        self.status_code = status_code
        self.raise_for_status_flag = raise_for_status_flag
    def raise_for_status(self):
        if self.raise_for_status_flag:
            self.text = 'some error occurred'
            raise requests.exceptions.HTTPError()
        else:
            return
    def json(self):
        return self.json_data

class TestCloudFoundryAPI_Auth(TestCase):

    def mocked_requests_get(*args, **kwargs):
        if args[0] == 'https://api.ng.bluemix.net/v2/info':
            return MockResponse({"authorization_endpoint": "https://login.ng.bluemix.net/UAALoginServerWAR"}, 200)
        raise RuntimeError("Unhandle GET request: " + args[0]) 

    def mocked_requests_post(*args, **kwargs):
        if args[0] == 'https://login.ng.bluemix.net/UAALoginServerWAR/oauth/token':
            return MockResponse(None, None, True)
        raise RuntimeError("Unhandle GET request: " + args[0]) 

    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('requests.post', side_effect=mocked_requests_post)
    def test_auth(self, mock_get, mock_post):

        cf = CloudFoundryAPI(api_key='abcdef')
        with self.assertRaises(RequestException):
            cf.auth()

class TestCloudFoundryAPI_Oidc(TestCase):

    def mocked_requests_get(*args, **kwargs):
        if args[0] == 'https://api.ng.bluemix.net/v2/info':
            return MockResponse({"authorization_endpoint": "https://login.ng.bluemix.net/UAALoginServerWAR"}, 200)
        raise RuntimeError("Unhandle GET request: " + args[0]) 

    def mocked_requests_post(*args, **kwargs):
        if args[0] == 'https://login.ng.bluemix.net/UAALoginServerWAR/oauth/token':
            return MockResponse({'access_token': 'aaaaa', 'token_type': 'bearer', 'refresh_token': 'aaaaa', 'expires_in': 1209599}, 200)
        if args[0] == 'https://iam.bluemix.net/identity/token':
            return MockResponse(None, None, True)

        raise RuntimeError("Unhandle GET request: " + args[0]) 

    @patch('requests.get', side_effect=mocked_requests_get)
    @patch('requests.post', side_effect=mocked_requests_post)
    def test_auth(self, mock_get, mock_post):

        cf = CloudFoundryAPI(api_key='abcdef')
        with self.assertRaises(RequestException):
            cf.oidc_token()
