from ibm_analytics_engine.cf.client import CloudFoundryAPI, CloudFoundryException
from ibm_analytics_engine import IAE

cf = CloudFoundryAPI(api_key_filename='your_api_key_filename')

iae = IAE(cf_client=cf)
try:
    iae.delete_cluster(
        cluster_instance_guid='12345-12345-12345-12345', 
        recursive=True)

    print('Cluster deleted.')
except CloudFoundryException as e:
    print('Unable to delete cluster: ' + str(e))
    
