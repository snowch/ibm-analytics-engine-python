#!/usr/bin/env python3

import sys
import os

from ibm_analytics_engine import CloudFoundryAPI

os.environ["LOG_LEVEL"] = "INFO"

cf = CloudFoundryAPI(api_key_filename=os.environ['API_KEY_FILENAME'])

spaces_json = cf.spaces.get_spaces()
organizations_json = cf.organizations.get_organizations()

def get_spaces(organization_guid, spaces_json):
    spaces = []
    for spc in spaces_json['resources']:
        if spc['entity']['organization_guid'] == organization_guid:
            spaces.append(spc)
    return spaces

for organization in organizations_json['resources']:
    print('name:{} organization_guid:{}'.format(organization['entity']['name'], organization['metadata']['guid']))
    for space in get_spaces(organization['metadata']['guid'], spaces_json):
        print('\tname:{} space_guid:{}'.format(space['entity']['name'], space['metadata']['guid']))
    print()
