from unittest import TestCase

from mock import Mock, MagicMock

from ibm_analytics_engine.cf.client import CloudFoundryAPI
from ibm_analytics_engine.cf.service_keys import ServiceKey

class ServiceKey_Test(TestCase):

    def test_get_service_keys(self):
        mock = Mock(spec=CloudFoundryAPI)
        mock._request = MagicMock()
        mock.api_endpoint = 'my_url'

        si = ServiceKey(mock)
        si.get_service_keys( service_instance_guid='my_space_guid' )

        mock._request.assert_called_once_with( 
            description='get_service_keys', http_method='get', url='my_url/v2/service_keys?q=service_instance_guid:my_space_guid'
            )

    def test_get_service_keys_with_name(self):
        mock = Mock(spec=CloudFoundryAPI)
        mock._request = MagicMock()
        mock.api_endpoint = 'my_url'

        si = ServiceKey(mock)
        si.get_service_keys( service_instance_guid='my_space_guid', name='my_key_name' )

        mock._request.assert_called_once_with( 
            description='get_service_keys', http_method='get', url='my_url/v2/service_keys?q=service_instance_guid:my_space_guid&q=name:my_key_name'
            )
