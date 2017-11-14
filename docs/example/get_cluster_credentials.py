#!/usr/bin/env python3

import os
import sys
import json
from ibm_analytics_engine import CloudFoundryAPI

os.environ["LOG_LEVEL"] = "DEBUG"

script = sys.argv[0]

if len(sys.argv) >= 3:
    cf_api_key_filename = sys.argv[1]
    cluster_instance_guid = sys.argv[2]

    if len(sys.argv) == 4:
        credentials_name = sys.argv[3]
else:
    print(
        "Usage: {} cf_api_key_filename cluster_instance_guid [credentials_name]".format(script))
    print("       --------")
    print("       Example:")
    print("       {} ./apiKey.json 12345-67890 Credentials-1".format(script))
    sys.exit(-1)


cf = CloudFoundryAPI(api_key_filename=cf_api_key_filename)

try:
    credential_json = cf.service_keys.get_service_keys(
        service_instance_guid=cluster_instance_guid, name=credentials_name)
except NameError:
    credential_json = cf.service_keys.get_service_keys(
        service_instance_guid=cluster_instance_guid)

if credential_json['total_results'] == 0:
    print('Credentials not found for this cluster')
    sys.exit(-1)
elif credential_json['total_results'] >= 1:
    print('More than one credentials were found for this cluster, try running with "credentials_name" parameter')

    vcap_json = credential_json['resources'][0]['entity']['credentials']
    print(json.dumps(vcap_json, indent=4, separators=(',', ': ')))
