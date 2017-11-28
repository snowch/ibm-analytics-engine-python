from ibm_analytics_engine.cf.client import CloudFoundryAPI
from ibm_analytics_engine import IAE, IAEServicePlanGuid

cf = CloudFoundryAPI(api_key_filename='your_api_key_filename')

space_guid = cf.space_guid(org_name='your_org_name', space_name='your_space_name')

iae = IAE(cf_client=cf)

cluster_instance_id = iae.create_cluster(
    service_instance_name='SPARK_CLUSTER',
    service_plan_guid=IAEServicePlanGuid.LITE,
    space_guid=space_guid,
    cluster_creation_parameters={
        "hardware_config": "default",
        "num_compute_nodes": 1,
        "software_package": "ae-1.0-spark",
    }
)
print('>> IAE cluster instance id: {}'.format(cluster_instance_id))

# This call blocks for several minutes.  See the Get Cluster Status example
# for alternative options.

status = iae.status(
    cluster_instance_id=cluster_instance_id,
    poll_while_in_progress=True)

print('>> Cluster status: {}'.format(status))
