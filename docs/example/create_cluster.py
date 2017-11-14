#!/usr/bin/env python3

import os
import sys
import json
from ibm_analytics_engine import CloudFoundryAPI, IAE, IAEServicePlanGuid

os.environ["LOG_LEVEL"] = "DEBUG"

script_name = sys.argv[0]
if len(sys.argv) != 4:
    print("Usage: {} cf_api_key_filename new_cluster_name space_guid".format(script_name))
    sys.exit(-1)

cf_api_key_filename = sys.argv[1]
new_cluster_name = sys.argv[2]
space_guid = sys.argv[3]

cf = CloudFoundryAPI(api_key_filename=cf_api_key_filename)
iae = IAE(cf_client=cf)


cluster_instance_id = iae.create_cluster(
    service_instance_name=new_cluster_name,
    service_plan_guid=IAEServicePlanGuid.LITE,
    space_guid=space_guid,
    customization_script={
        "hardware_config": "default",
        "num_compute_nodes": 1,
        "software_package": "ae-1.0-spark",
        #"customization":[ ]
    }
)

print('>> IAE cluster instance id: {}'.format(cluster_instance_id))

status = iae.get_cluster_status(cluster_instance_id)

if status == 'succeeded':
    credentials_json = iae.create_credentials(cluster_instance_id)
    vcap_json = credentials_json['entity']['credentials']

    print('>> VCAP:')
    print(json.dumps(vcap_json, indent=4, separators=(',', ': ')))
else:
    print('Cluster status: {}'.format(status))
