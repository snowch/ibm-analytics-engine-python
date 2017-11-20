from unittest import TestCase

from mock import Mock, MagicMock

from ibm_analytics_engine.cf.client import CloudFoundryAPI
from ibm_analytics_engine.cf.organizations import Organization

class Organization_Test(TestCase):

    def test(self):
        mock = Mock(spec=CloudFoundryAPI)
        mock._request = MagicMock()
        mock.api_endpoint = 'my_url'

        o = Organization(mock)
        o.get_organizations()

        mock._request.assert_called_once_with(description='get_space', http_method='get', url='my_url/v2/organizations')

    def test_with_name(self):
        mock = Mock(spec=CloudFoundryAPI)
        mock._request = MagicMock()
        mock.api_endpoint = 'my_url'

        o = Organization(mock)
        o.get_organizations('space_name')

        mock._request.assert_called_once_with(description='get_space', http_method='get', url='my_url/v2/organizations?q=name:space_name')

