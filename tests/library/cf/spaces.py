from unittest import TestCase

from mock import Mock, MagicMock

from ibm_analytics_engine.cf.client import CloudFoundryAPI
from ibm_analytics_engine.cf.spaces import Space

class Space_Test(TestCase):

    def test(self):
        mock = Mock(spec=CloudFoundryAPI)
        mock._request = MagicMock()
        mock.api_endpoint = 'my_url'

        s = Space(mock)
        s.get_spaces()

        mock._request.assert_called_once_with(description='get_space', http_method='get', url='my_url/v2/spaces')

    def test_with_name(self):
        mock = Mock(spec=CloudFoundryAPI)
        mock._request = MagicMock()
        mock.api_endpoint = 'my_url'

        s = Space(mock)
        s.get_spaces('space_name')

        mock._request.assert_called_once_with(description='get_space', http_method='get', url='my_url/v2/spaces?q=name:space_name')

