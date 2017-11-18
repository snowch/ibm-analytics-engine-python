import os
from ibm_analytics_engine import CloudFoundryAPI

os.environ["LOG_LEVEL"] = "INFO"

cf = CloudFoundryAPI(api_key_filename=os.environ['API_KEY_FILENAME'])
cf.print_orgs_and_spaces()
