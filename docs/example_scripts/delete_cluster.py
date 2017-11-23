import os
from ibm_analytics_engine import CloudFoundryAPI, CloudFoundryException, IAE

# set the iae modules to debug level output
os.environ["LOG_LEVEL"] = "DEBUG"

cf_api_key_filename = os.environ['API_KEY_FILENAME']
cluster_instance_guid = os.environ['CLUSTER_INSTANCE_GUID']

cf = CloudFoundryAPI(api_key_filename=cf_api_key_filename)

iae = IAE(cf_client=cf)

try:
    iae.delete_cluster(cluster_instance_guid, recursive=True)
    print('Cluster deleted.')
except CloudFoundryException as e:
    print('Unable to delete cluster: ' + str(e))
    
