# apigee-debug-sessions
=======================

## Description:
This is a simple python script that will create a Debug Session in Apigee for a given API Proxy and Revision,
and outputs a debug session file in a format that can be imported into the Edge UI for review

# Pre-requisites
* Python ~= v2.7.10
* Python requests ~= 2.11.1
* xml.etree.ElementTree (Standard python library)
 
# Load pre-requisites using pip
<pre>
pip install requests
</pre>

# Authentication Environment variables
The script expects environment variables for the k

# Usage: 
<pre>
usage: apigee_debug_session.py [-h] [--management-host MANAGEMENT_HOST]
                               [--organization ORGANIZATION]
                               [--environment ENVIRONMENT] [--timeout TIMEOUT]
                               [--proxy PROXY] [--revision REVISION]

arguments:
  -h, --help            show this help message and exit
  --management-host MANAGEMENT_HOST
                        The hostname of the management server. Defaults to
                        api.enterprise.apigee.com.
  --organization ORGANIZATION
                        The Apigee organization name, e.g. 'mycompany'
  --environment ENVIRONMENT
                        The Apigee environment name, e.g. 'test'
  --timeout TIMEOUT     The time in seconds during which to collect traces via
                        debugsession. --timeout 300 will run traces for 5
                        minutes.
  --proxy PROXY         The name of the proxy to run traces on, e.g. 'orders'
  --revision REVISION   The revision number of the (deployed) proxy to debug,
                        e.g. 2
</pre>