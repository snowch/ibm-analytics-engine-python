from ibm_analytics_engine import CloudFoundryAPI

cf = CloudFoundryAPI(api_key_filename=your_api_key_filename)
cf.print_orgs_and_spaces()
