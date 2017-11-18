import os
from ibm_analytics_engine import CloudFoundryAPI, IAE, IAEServicePlanGuid

os.environ["LOG_LEVEL"] = "DEBUG"

# This example gets its parameters from environment variables
cf_api_key_filename = os.environ['API_KEY_FILENAME']
new_cluster_name = os.environ['CLUSTER_NAME']
space_guid = os.environ['SPACE_GUID']

cf = CloudFoundryAPI(api_key_filename=cf_api_key_filename)
iae = IAE(cf_client=cf)

cluster_instance_id = iae.create_cluster(
    service_instance_name=new_cluster_name,
    service_plan_guid=IAEServicePlanGuid.LITE,
    space_guid=space_guid,
    customization_script={
        "hardware_config": "default",
        "num_compute_nodes": 1,
        "software_package": "ae-1.0-spark",
    }
)
print('>> IAE cluster instance id: {}'.format(cluster_instance_id))
status = iae.get_cluster_status(cluster_instance_id)
if status == 'succeeded':
   credentials_json = iae.create_credentials(cluster_instance_id)
   vcap_json = credentials_json['entity']['credentials']
   print('>> VCAP:\n' + json.dumps(vcap_json, indent=4, separators=(',', ': ')))
else:
   print('>> Cluster status: {}'.format(status))
