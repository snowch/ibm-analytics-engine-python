import os
from ibm_analytics_engine import CloudFoundryAPI, IAE

# set the iae modules to debug level output
os.environ["LOG_LEVEL"] = "DEBUG"

cf_api_key_filename = os.environ['API_KEY_FILENAME']
cluster_instance_guid = os.environ['CLUSTER_INSTANCE_GUID']

cf = CloudFoundryAPI(api_key_filename=cf_api_key_filename)

iae = IAE(cf_client=cf)
success = iae.delete_cluster(cluster_instance_guid, recursive=True)

if success:
    print('Cluster deleted.')
else:
    print('Unable to delete cluster - unknown issue.')
