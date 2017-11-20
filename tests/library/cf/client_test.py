from unittest import TestCase
from mock import Mock, patch

import sys
import tempfile
import os
import json
import requests

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

    @patch('requests.get')
    def test_auth(self, mock_get):
        mock_response = Mock()
        http_error = requests.exceptions.RequestException()
        mock_response.raise_for_status.side_effect = http_error
        mock_get.return_value = mock_response

        with self.assertRaises(requests.exceptions.RequestException):
            cf = CloudFoundryAPI(api_key='abcdef')

