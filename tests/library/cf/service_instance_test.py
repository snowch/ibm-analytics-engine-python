from unittest import TestCase

from mock import Mock, MagicMock

from ibm_analytics_engine.cf.client import CloudFoundryAPI
from ibm_analytics_engine.cf.service_instances import ServiceInstance

class ServiceInstance_Test(TestCase):

    def test_provision_without_poll(self):
        mock = Mock(spec=CloudFoundryAPI)
        mock._request = MagicMock()
        mock.api_endpoint = 'my_url'

        si = ServiceInstance(mock)
        si.provision(
            service_instance_name='my_cluster',
            service_plan_guid='my_service_plan',
            space_guid='my_space_guid',
            parameters={
                "somedata": "default",
            }
        )
        mock._request.assert_called_once_with( 
            data={'name': 'my_cluster', 'space_guid': 'my_space_guid', 'service_plan_guid': 'my_service_plan', 'parameters': {'somedata': 'default'}}, description='provision', http_method='post', url='my_url/v2/service_instances?accepts_incomplete=true'
            )

