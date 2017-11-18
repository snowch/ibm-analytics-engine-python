import os
import json
from ibm_analytics_engine import CloudFoundryAPI, IAE

os.environ["LOG_LEVEL"] = "DEBUG"

cf_api_key_filename = os.environ['API_KEY_FILENAME']
cluster_instance_guid = os.environ['CLUSTER_INSTANCE_GUID']

cf = CloudFoundryAPI(api_key_filename=cf_api_key_filename)
iae = IAE(cf_client=cf)

vcap_json = iae.get_or_create_credentials(cluster_instance_guid)

# pretty print json
print(json.dumps(vcap_json, indent=4, separators=(',', ': ')))

