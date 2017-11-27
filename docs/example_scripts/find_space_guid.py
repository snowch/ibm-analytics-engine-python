import os
from ibm_analytics_engine import CloudFoundryAPI

os.environ["LOG_LEVEL"] = "INFO"

cf = CloudFoundryAPI(api_key_filename=os.environ['API_KEY_FILENAME'])

space_guid = cf.space_guid(org_name='my_org_name', space_name='my_space_name')
