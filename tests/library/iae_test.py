from unittest import TestCase

from mock import Mock, MagicMock

from ibm_analytics_engine import IAE, CloudFoundryAPI

class IAE_Test(TestCase):

    def test_provision_without_poll(self):
        mock = Mock(spec=CloudFoundryAPI)
        mock.service_instances = MagicMock()
        iae = IAE(cf_client=mock)
        iae.create_cluster(
            service_instance_name='my_cluster',
            service_plan_guid='my_service_plan',
            space_guid='my_space_guid',
            customization_script={
                "somedata": "default",
            }
        )
        mock.service_instances.provision.assert_called_once_with( 
            'my_cluster', 'my_service_plan', 'my_space_guid', {'somedata': 'default'}, poll_for_completion=False
        )

    #def test_get_cluster_status(self):
    #    mock = Mock(spec=CloudFoundryAPI)
    #    mock.service_instances = MagicMock()
    #    iae = IAE(cf_client=mock)
    #    
    #    mock.service_instances.provision.assert_called_once_with( 
    #curl -i -X GET https://api.dataplatform.ibm.com/v2/analytics_engines/<service_instance_id>/state -H 'Authorization: Bearer <user's IAM access token>'

