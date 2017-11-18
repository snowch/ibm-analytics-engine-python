import os
from ibm_analytics_engine import CloudFoundryAPI, IAE

os.environ["LOG_LEVEL"] = "INFO"

CF_API_KEY_FILENAME=os.environ['API_KEY_FILENAME']
SPACE_GUID=os.environ['SPACE_GUID']

cf = CloudFoundryAPI(api_key_filename=CF_API_KEY_FILENAME)
iae = IAE(cf_client=cf)

for i in iae.clusters(SPACE_GUID):
    print(i)
