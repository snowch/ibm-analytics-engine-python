from ibm_analytics_engine import CloudFoundryAPI

cf = CloudFoundryAPI(api_key_filename=your_api_key_filename)

try:
    space_guid = cf.space_guid(org_name='my_org_name', space_name='my_space_name')
    print(space_guid)
except ValueError as e:
    # Space not found
    print(e)
