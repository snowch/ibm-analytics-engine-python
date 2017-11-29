from ibm_analytics_engine.cf.client import CloudFoundryAPI
from ibm_analytics_engine import IAE

cf = CloudFoundryAPI(api_key_filename='your_api_key_filename')
iae = IAE(cf_client=cf)

status = iae.status(
    cluster_instance_guid='12345-12345-12345-12345',
    poll_while_in_progress=True)

print(status)
