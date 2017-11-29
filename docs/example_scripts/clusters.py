from ibm_analytics_engine.cf.client import CloudFoundryAPI
from ibm_analytics_engine import IAE

cf = CloudFoundryAPI(api_key_filename='your_api_key_filename')

space_guid = cf.space_guid(org_name='your_org_name', space_name='your_space_name')

iae = IAE(cf_client=cf)

for i in iae.clusters(space_guid=space_guid):
    print(i)
