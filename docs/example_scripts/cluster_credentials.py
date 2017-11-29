import json
from ibm_analytics_engine.cf.client import CloudFoundryAPI
from ibm_analytics_engine import IAE

cf = CloudFoundryAPI(api_key_filename='your_api_key_filename')
iae = IAE(cf_client=cf)

vcap_json = iae.get_or_create_credentials(cluster_instance_guid='12345-12345-12345-12345')

# prettify json
vcap_formatted = json.dumps(vcap_json, indent=4, separators=(',', ': '))

print(vcap_formatted)
