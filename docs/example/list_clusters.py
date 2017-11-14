#!/usr/bin/env python3

import json
import os
import sys
from ibm_analytics_engine import CloudFoundryAPI, IAE

os.environ["LOG_LEVEL"] = "INFO"

script_name = sys.argv[0]
if len(sys.argv) != 3:
    print("Usage: {} cf_api_key_filename space_guid".format(script_name))
    sys.exit(-1)

cf_api_key_filename = sys.argv[1]
space_guid = sys.argv[2]

cf_client = CloudFoundryAPI(api_key_filename=cf_api_key_filename)
iae = IAE(cf_client=cf_client)

for i in iae.clusters(space_guid):
    print(i)
