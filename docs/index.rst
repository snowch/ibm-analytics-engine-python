.. IBM Analyics Engine documentation master file, created by
   sphinx-quickstart on Fri Nov 17 06:46:19 2017.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to IBM Analyics Engine's documentation!
===============================================

.. toctree::
   :maxdepth: 2
   :caption: Contents:

NOTE: This documentation is a work-in-progress.  Please come back soon ...

.. automodule:: ibm_analytics_engine

Example:

.. code-block:: python

   from ibm_analytics_engine import CloudFoundryAPI, IAE, IAEServicePlanGuid

   os.environ["LOG_LEVEL"] = "DEBUG"
   
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
       }
   )
   print('>> IAE cluster instance id: {}'.format(cluster_instance_id))
   status = iae.get_cluster_status(cluster_instance_id)
   if status == 'succeeded':
      credentials_json = iae.create_credentials(cluster_instance_id)
      vcap_json = credentials_json['entity']['credentials']
      print('>> VCAP:\n' + json.dumps(vcap_json, indent=4, separators=(',', ': ')))
   else:
      print('>> Cluster status: {}'.format(status))

.. autoclass:: IAE
    :members: __init__, clusters

.. autoclass:: IAEServicePlanGuid
    :members:

.. autoclass:: CloudFoundryAPI 
    :members: __init__

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
