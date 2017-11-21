from unittest import TestCase

from mock import Mock, MagicMock

from ibm_analytics_engine import IAE, CloudFoundryAPI, IAEServicePlanGuid
from ibm_analytics_engine.cf.service_instances import ServiceInstance

class IAE_Test(TestCase):

    def test_provision_without_poll(self):
        mock = Mock(spec=CloudFoundryAPI)
        mock.service_instances = MagicMock()
        iae = IAE(cf_client=mock)
        iae.create_cluster(
            service_instance_name='my_cluster',
            service_plan_guid='my_service_plan',
            space_guid='my_space_guid',
            cluster_creation_parameters={
                "somedata": "default",
            }
        )
        mock.service_instances.provision.assert_called_once_with( 
            'my_cluster', 'my_service_plan', 'my_space_guid', {'somedata': 'default'}, poll_for_completion=False
        )

    def test_list_clusters(self):
        mock = Mock(spec=CloudFoundryAPI)
        service_instances = Mock(spec=ServiceInstance)
        service_instances.get_service_instances.return_value = [
                { 'name':'abc', 'guid':'12345', 'last_operation': {'state': 'failed' }, 'service_plan': { 'guid': IAEServicePlanGuid.LITE} },
                { 'name':'def', 'guid':'01234', 'last_operation': {'state': 'succeeded' }, 'service_plan': { 'guid': IAEServicePlanGuid.LITE} }
                ]
        mock.service_instances = service_instances

        iae = IAE(cf_client=mock)
        clusters = iae.clusters('my_space_guid', status='succeeded')

        mock.service_instances.get_service_instances.assert_called_once_with('my_space_guid')

        assert len(clusters) == 1
        assert clusters[0] == ('def', '01234', 'succeeded')

    def test_list_clusters_with_keyerror(self):
        mock = Mock(spec=CloudFoundryAPI)
        service_instances = Mock(spec=ServiceInstance)
        service_instances.get_service_instances.return_value = [
                { 'non_existent_key': None },
                { 'non_existent_key': None },
                ]
        mock.service_instances = service_instances

        iae = IAE(cf_client=mock)
        clusters = iae.clusters('my_space_guid')
        mock.service_instances.get_service_instances.assert_called_once_with('my_space_guid')
        assert len(clusters) == 0
