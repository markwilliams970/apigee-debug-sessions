# apigee-debug-sessions
=======================

## Description:
This is a simple python script that will create a Debug Session in Apigee for a given API Proxy and Revision,
and outputs a debug session file in a format that can be imported into the Edge UI for review

# Pre-requisites
* Python ~= v2.7.10
* Python [requests](http://docs.python-requests.org/en/master/) ~= 2.11.1
* xml.etree.ElementTree (Standard python library)
 
# Load pre-requisites using pip
<pre>
pip install requests
</pre>

# Authentication Environment variables
The script expects environment variables for the credentials of an Apigee organization admin to be set as follows:
<pre>
export APIGEE_USER=user@company.com
export APIGEE_PASSWORD=t0ps3cr3t
</pre>

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

# Usage Example:
<pre>
python apigee_debug_session.py --organization 'myorg' --environment 'test' --timeout 300 --proxy 'helloworld_markw_20161013' --revision 2
Creating the debug session...
Created Debug session 1b6043ff-7750-4eb5-bc88-2a365f47f47c for Revision 2 of helloworld_markw_20161013 in Environment test
Debug session 1b6043ff-7750-4eb5-bc88-2a365f47f47c created...
Collecting traces for 270 seconds....
This represents a session length of 300 seconds
_minus_ a pre-defined interval of 30 seconds during which trace data is downloaded and processed
Collecting trace data...
Finished! Debug session written to file: myorg-test-helloworld_markw_20161013-2_1b6043ff-7750-4eb5-bc88-2a365f47f47c.xml
</pre>

# Loading trace file into the Edge UI
* Make note of location and name of file output by the script per usage example above
![Screenshot01](https://raw.githubusercontent.com/markwilliams970/apigee-debug-sessions/master/images/screenshot01.png)
* Login to Apigee, navigate to APIs -> API Proxies; Click "Offline Trace" Button
![Screenshot02](https://raw.githubusercontent.com/markwilliams970/apigee-debug-sessions/master/images/screenshot02.png)
* Navigate to the file output from your trace session and load
![Screenshot03](https://raw.githubusercontent.com/markwilliams970/apigee-debug-sessions/master/images/screenshot03.png)
* Review traces in UI
![Screenshot05](https://raw.githubusercontent.com/markwilliams970/apigee-debug-sessions/master/images/screenshot04.png)