
[![Build Status](https://travis-ci.org/snowch/ibm-analytics-engine-python.svg?branch=master)](https://travis-ci.org/snowch/ibm-analytics-engine-python)
----

### Overview

This project is a python library for working with [IBM Analytics Engine (IAE)](https://console.bluemix.net/docs/services/AnalyticsEngine/index.html).  This project is an early prototype - consider this project to be 'alpha' or 'beta' quality.

### Install

```
pip3 install git+https://github.com/snowch/ibm-analytics-engine-python
```

### Usage

The lifecycle of an IBM Analytics Engine cluster is controller through Cloud Foundry (e.g. create, delete, status operations).  This python library requires an API key to work with the Cloud Foundry APIs.  For more information on IBM Cloud API Keys including how to create and download an API Key, see [here](https://console.bluemix.net/docs/iam/userid_keys.html#userapikey)

#### Create Cluster

This example script creates a new cluster instance:

```python
import os
import json
from ibm_analytics_engine import CloudFoundryAPI, IAE, IAEServicePlanGuid

os.environ["LOG_LEVEL"] = "DEBUG"

# The path to your API key
cf_api_key_filename = './yourApiKey.json'

# The name of the cluster in your IBM Cloud space
new_cluster_name = 'My Analytics Engine'

# You can find your space guid with the script docs/example/list_orgs_and_spaces.py
space_guid = 'my_space_guid'

cf = CloudFoundryAPI(api_key_filename=cf_api_key_filename)
iae = IAE(cf_client=cf)

cluster_instance_id = iae.create_cluster(
    service_instance_name=new_cluster_name,
    service_plan_guid=IAEServicePlanGuid.LITE,
    space_guid=space_guid,
    customization_script={
        "hardware_config": "default",
        "num_compute_nodes": 1,
        "software_package": "ae-1.0-spark"
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
```

See more example scripts in [docs/example/](docs/example/)

### Contributing

Please create an [issue](https://github.com/snowch/ibm-analytics-engine-python/issues) for questions, bugs and feature requests.

Pull requests are welcome!

### Related Projects

This [project](https://git.ng.bluemix.net/chris.snow/iae-spark-package-customization-example/tree/master) uses the ibm-analytics-engine-python library to configure a cluster with a bootstrap customization script and then sets up a local jupyter notebook environment in docker to connect to the cluster.
