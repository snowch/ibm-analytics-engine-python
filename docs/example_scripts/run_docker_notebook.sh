#!/bin/bash

export VCAP_STR="$(cat vcap.json)"

KG_HTTP_USER=$(python -c "import json, os; print(json.loads(os.environ['VCAP_STR'])['cluster']['user'])")
KG_HTTP_PASS=$(python -c "import json, os; print(json.loads(os.environ['VCAP_STR'])['cluster']['password'])")
KG_HTTP_URL=$(python -c "import json, os; print(json.loads(os.environ['VCAP_STR'])['cluster']['service_endpoints']['notebook_gateway'])")
KG_WS_URL=$(python -c "import json, os; print(json.loads(os.environ['VCAP_STR'])['cluster']['service_endpoints']['notebook_gateway_websocket'])")

# Create a directory for the notebooks so they don't disappear when the docker constainer shuts down 
if [ ! -d notebooks ] 
then
   mkdir notebooks
fi

docker run -it --rm \
	-v $(pwd)/notebooks:/tmp/notebooks \
	-e KG_HTTP_USER=$KG_HTTP_USER \
	-e KG_HTTP_PASS=$KG_HTTP_PASS \
	-e KG_URL=$KG_HTTP_URL \
	-e KG_WS_URL=$KG_WS_URL \
	-p 8888:8888 \
	biginsights/jupyter-nb-nb2kg

# Open a browser window to: http://127.0.0.1:8888

