import time
from ibm_analytics_engine.cf.client import CloudFoundryAPI
from ibm_analytics_engine import IAE

cf = CloudFoundryAPI(api_key_filename='your_api_key_filename')
iae = IAE(cf_client=cf)

while True:
    status = iae.status(cluster_instance_guid='12345-12345-12345-12345')
    if status == 'succeeded' or status == 'failed': break
    time.sleep(60)

print(status)
