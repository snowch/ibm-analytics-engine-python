from __future__ import absolute_import
from __future__ import print_function

from .logger import Logger

"""
.. module:: iae
   :platform: Unix, Windows
   :synopsis: Classes for working with IBM Analytics Engine

.. moduleauthor:: Chris Snow <chsnow123@gmail.com>


"""

class IAEServicePlanGuid:
    """Service Plan Guid for IBM Analytics Engine."""

    LITE = 'acb06a56-fab1-4cb1-a178-c811bc676164'
    """IBM Analytics Engine 'Lite' plan."""

    STD_HOURLY = '9ba7e645-fce1-46ad-90dc-12655bc45f9e'
    """IBM Analytics Engine 'Standard Hourly' plan."""

    STD_MONTHLY = 'f801e166-2c73-4189-8ebb-ef7c1b586709'
    """IBM Analytics Engine 'Standard Monthly' plan."""

    def guids():
        return [
            IAEServicePlanGuid.LITE,
            IAEServicePlanGuid.STD_HOURLY,
            IAEServicePlanGuid.STD_MONTHLY
        ]



class IAE:
    """
    This class provides methods for working with IBM Analytics Engine (IAE) deployment operations.  
    Many of the methods in this calls are performed by calling the Cloud Foundry Rest API (https://apidocs.cloudfoundry.org/272/).
    The Cloud Foundry API is quite abstract, so this class provides methods names that are more meaningful for those just wanting to work with IAE.

    This class does not save the state from the Cloud Foundry operations - it retrieve all state from Cloud Foundry as required.
    """

    def __init__(self, cf_client):
        """
        Create a new instance of the IAE client.

        Args:
            cf_client (CloudFoundryAPI): The object that makes the Cloud Foundry rest API calls.
        """

        assert cf_client is not None, "This action requires a CloudFoundryAPI instance"

        if cf_client:
            self.cf_client = cf_client

        self.log = Logger().get_logger(self.__class__.__name__)

    #
    # generic cluster operations
    #

    # TODO create an class for the last_operation_status
    def clusters(self, space_guid, short=True, status=None):
        """
        Returns a list of clusters in the `space_guid`

        Args:
            space_guid (:obj:`str`): The space_guid to query for IAE clusters.
            short (:obj:`bool`, optional): Whether to return short (brief) output.  If false, returns the full Cloud Foundry API output.
            status (:obj:`str`, optional): Filter the return only the provided status values.

        Returns:
            :obj:`list`: If the `short=True`, this method returns: `[ (cluster_name, cluster_guid, last_operation_state), ...  ]`

                | The `last_operation_status` may be:
                | 
                | - `in progress`
                | - `succeeded`
                | - `failed`

        """

        # TODO pass IAEServicePlanGuid.guids() to the filter parameter in the
        # cf api call
        iae_instances = self.cf_client.service_instances.get_service_instances(
            space_guid)

        clusters = []
        for i in iae_instances:
            try:
                if i['service_plan']['guid'] in IAEServicePlanGuid.guids():
                    if status is None or status == i['last_operation']['state']:
                        if short:
                            clusters.append(
                                (i['name'], i['guid'], i['last_operation']['state']))
                        else:
                            clusters.append(i)
            except KeyError:
                pass
        return clusters

    def create_cluster(
            self,
            service_instance_name,
            service_plan_guid,
            space_guid,
            customization_script):

        # Create instance
        response = self.cf_client.service_instances.provision(
            service_instance_name,
            service_plan_guid,
            space_guid,
            customization_script,
            poll_for_completion=False)
        cluster_instance_id = response['metadata']['guid']

        return cluster_instance_id
    #
    # operations on a specific cluster - requires cluster_instance_id
    #

    # TODO rename to cloud foundry status
    def status(self, cluster_instance_id):
        response = self.cf_client.service_instances.status(
                service_instance_id=cluster_instance_id)
        return response

    # move method to vcap object?
    def status2(self, vcap_json):
        iam_token = self.cf_client.get_oidc_token()['access_token']
        headers = {
                'Authorization': 'Bearer {}'.format(iam_token)
                }
        api_url = vcap_json['cluster_management']['api_url'] + '/state'

        import requests
        response = requests.get(api_url, headers=headers) 

        print(response.text)

    def delete_cluster(self, cluster_instance_id, recursive=False):
        try:
            self.cf_client.service_instances.delete_service_instance(
                service_instance_id=cluster_instance_id, recursive=recursive)
            return True
        except Exception:
            self.log.exception('Unable to delete')
            return False

    def create_credentials(
            self,
            cluster_instance_id,
            credentials_name=None,
            allow_multiple_credentials=False):

        # TODO check if credentials exist and allow_multiple_credentails=False
        # return None

        if credentials_name:
            vcap = self.cf_client.service_keys.create_service_key(
                cluster_instance_id, credentials_name)
        else:
            vcap = self.cf_client.service_keys.create_service_key(
                cluster_instance_id)
        return vcap

    # TODO add parameter poll=True and parameter for callback method
    def get_cluster_status(self, cluster_instance_id):
        return self.cf_client.service_instances.poll_for_completion(
            cluster_instance_id)
