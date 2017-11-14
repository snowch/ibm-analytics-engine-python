#!/usr/bin/env python3

import sys
import os

from ibm_analytics_engine import CloudFoundryAPI

os.environ["LOG_LEVEL"] = "INFO"

script = sys.argv[0]
if len(sys.argv) >= 2:
    cf_api_key_filename = sys.argv[1]

    if len(sys.argv) == 3:
        org_name = sys.argv[2]

    if len(sys.argv) == 4:
        space_name = sys.argv[3]
else:
    print("Usage: {} cf_key_api_filename [org_name] [space_name]".format(script))
    print("------")
    print("Example:")
    print("       {} ./apiKey.json me@test.com dev".format(script))
    sys.exit(-1)


cf = CloudFoundryAPI(api_key_filename=cf_api_key_filename)

try:
    spaces_json = cf.spaces.get_spaces(name=space_name)
except NameError:
    spaces_json = cf.spaces.get_spaces()

def get_spaces(organization_guid):
    spaces = []
    for spc in spaces_json['resources']:
        if spc['entity']['organization_guid'] == organization_guid:
            spaces.append(spc)
    return spaces

try:
    organizations_json = cf.organizations.get_organizations(name=org_name)
except NameError:
    organizations_json = cf.organizations.get_organizations()


for organization in organizations_json['resources']:
    print('name:{} organization_guid:{}'.format(organization['entity']['name'], organization['metadata']['guid']))
    for space in get_spaces(organization['metadata']['guid']):
        print('\tname:{} space_guid:{}'.format(space['entity']['name'], space['metadata']['guid']))
    print()
