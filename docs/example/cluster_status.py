#!/usr/bin/env python3

import os
import sys
from ibm_analytics_engine import CloudFoundryAPI, IAE

# set the iae modules to debug level output
os.environ["LOG_LEVEL"] = "DEBUG"

# This script needs the cluster_instance_id
script_name = sys.argv[0]
if len(sys.argv) != 3:
    print("Usage: {} cf_api_key_filename cluster_instance_id".format(script_name))
    sys.exit(-1)

cf_api_key_filename = sys.argv[1]
cluster_instance_id = sys.argv[2]

cf = CloudFoundryAPI(api_key_filename=cf_api_key_filename)

iae = IAE(cf_client=cf)
status = iae.status(cluster_instance_id)

print(status)
