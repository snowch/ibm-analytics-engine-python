from ibm_analytics_engine.cf.client import CloudFoundryAPI
from ibm_analytics_engine import IAE

cf = CloudFoundryAPI(api_key_filename='your_api_key_filename')

iae = IAE(cf_client=cf)

vcap = iae.get_or_create_credentials(cluster_instance_guid='12345-12345-12345-12345')

status = iae.dataplatform_status(vcap)

print(status)
