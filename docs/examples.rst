********
Examples
********

This section shows example code snippets for working with this library.

=============
Prerequisites
=============

**API Key**

The lifecycle of an IBM Analytics Engine cluster is controlled through Cloud Foundry (e.g. create, delete, status operations).  This python library requires an API key to work with the Cloud Foundry APIs.  For more information on IBM Cloud API Keys including how to create and download an API Key, see https://console.bluemix.net/docs/iam/userid_keys.html#userapikey

**Installation**

Ensure you have installed this library.

Install with:

.. code-block:: python

   pip install --upgrade git+https://github.com/snowch/ibm-analytics-engine-python@master

=======================
Finding your space guid
=======================

Many operations in this library require you to specify a space guid.  You can list the spaces guids for your account using this example:

.. literalinclude:: example_scripts/list_orgs_and_spaces.py

Alternatively, if you know your organisation name and space name, you can use the following:

.. literalinclude:: example_scripts/find_space_guid.py

==============
Create Cluster
==============

.. literalinclude:: example_scripts/create_cluster.py

==============
Delete Cluster
==============

.. literalinclude:: example_scripts/delete_cluster.py

==============================
Get or Create Credentials
==============================

.. literalinclude:: example_scripts/cluster_credentials.py

===================
Get Clusters Status
===================

To return the Cloud Foundry status:

.. literalinclude:: example_scripts/cluster_status.py

Alternative option to poll for the Cloud Foundry status until it is 'succeeded' or 'failed':

.. literalinclude:: example_scripts/cluster_status_poll.py

To return the Data Platform API status:

.. literalinclude:: example_scripts/cluster_dp_api_status.py

=============
List Clusters
=============

.. literalinclude:: example_scripts/clusters.py

========================
Jupyter Notebook Gateway
========================

This is an example script for running a docker notebook that connects to the cluster using the JNBG protocol and the credentials in your vcap.json file.

.. literalinclude:: example_scripts/run_docker_notebook.sh

