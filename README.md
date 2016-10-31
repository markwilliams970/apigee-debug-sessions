# apigee-debug-sessions
=======================

## Description:
This is a simple python script that will create a Debug Session using the Apigee Mangement API, for a given API Proxy and Revision.
If traces are collected during the session, the script will output a debug session file in a format that can be imported into the Edge UI for
visual review and inspection.

This can be a convenient way to facilitate a bit more extensive session tracing than the Edge UI permits, as the Edge UI will only allow collection
of a maximum of 20 traces at a time.

See http://docs.apigee.com/api/debug-sessions for more information on the Management API involved.

# Pre-requisites
* Python ~= v2.7.10
* Python [requests](http://docs.python-requests.org/en/master/) ~= 2.11.1
* xml.etree.ElementTree (Standard python library)
 
# Load pre-requisites using pip
<pre>
pip install requests
</pre>

# Authentication Environment variables
The script expects environment variables for the credentials of an Apigee organization admin to be set as follows (substituting actual credentials, of course):
<pre>
export APIGEE_USER=user@company.com
export APIGEE_PASSWORD=t0ps3cr3t
</pre>

# Usage: 
<pre>
usage: apigee_debug_session.py [-h] [--management-host MANAGEMENT_HOST]
                               [--organization ORGANIZATION]
                               [--environment ENVIRONMENT] [--proxy PROXY]
                               [--revision REVISION] [--timeout TIMEOUT]
                               [--sessions SESSIONS]
                               
required arguments:

  --organization ORGANIZATION
                        The Apigee organization name, e.g. 'mycompany'
 
  --environment ENVIRONMENT
                        The Apigee environment name, e.g. 'test'
  
  --proxy PROXY         The name of the proxy to run traces on, e.g. 'orders'
 
  --revision REVISION   The revision number of the (deployed) proxy to debug,
                        e.g. 2
 
  --timeout TIMEOUT     The time in seconds to collect traces via
                        debugsession. --timeout 90 will run traces for 90
                        seconds. The maximumn is 120, or 20 traces, whichever
                        comes first.

optional arguments:

  -h, --help            show this help message and exit
 
  --management-host MANAGEMENT_HOST
                        The hostname of the management server. Defaults to
                        api.enterprise.apigee.com.
 
  --sessions SESSIONS   The number of times to iteratively collect
                        debugsessions. Maximum of 50. Defaults to 1.
                                                                        
</pre>

# Usage Example:
<pre>
$ python apigee_debug_session.py --organization "gsc" --environment "test" \
    --proxy "helloworld_markw_20161013" --revision 2 --timeout 40 --sessions 20
Collecting session: 1 of 20...
Creating the debug session...
Created Debug session 1b6043ff-7750-4eb5-bc88-2a365f47f47c for Revision 2 of helloworld_markw_20161013 in Environment test
Debug session 1b6043ff-7750-4eb5-bc88-2a365f47f47c created...
Collecting traces for 120 seconds....
This represents a session length of 180 seconds
_minus_ a pre-defined interval of 30 seconds during which trace data is downloaded and processed
Collecting trace data...
Finished! Debug session written to file: myorg-test-helloworld_markw_20161013-2_1b6043ff-7750-4eb5-bc88-2a365f47f47c.xml
</pre>

# Usage Notes:
The script collects traces for a maximum of 120 seconds, or 20 traces per session, whichever comes first. Any traces
collected must be downloaded before the session timeout. As a result, by default, the script  is configured to allow 30 
seconds for collecting/downloading traces.

For example, if you specify a timeout of 120 seconds, the script will specify a timeout of 120
seconds when making the management API call. However, the tool  will collect traces for only 90 seconds, allowing as
much as 30 seconds to collect and download trace data.

See http://docs.apigee.com/api/debug-sessions for more information.

Depending on how active your proxy is in terms of transactions per second, you may need to run 
the script a few times to get a feel for the timeout parameter. For a busy
proxy, the maximum 20 traces/session could be reached very quickly, so a timeout value of as low
as 31 seconds could realistically be used as the desired value. This would allow trace collection
for 1 second, with 30 seconds to collect and download trace data.

# Loading trace file into the Edge UI
* Make note of location and name of file output by the script per usage example above
![Screenshot01](https://raw.githubusercontent.com/markwilliams970/apigee-debug-sessions/master/images/screenshot01.png)
* Login to Apigee, navigate to APIs -> API Proxies; Click "Offline Trace" Button
![Screenshot02](https://raw.githubusercontent.com/markwilliams970/apigee-debug-sessions/master/images/screenshot02.png)
* Navigate to the file output from your trace session and load
![Screenshot03](https://raw.githubusercontent.com/markwilliams970/apigee-debug-sessions/master/images/screenshot03.png)
* Review traces in UI
![Screenshot05](https://raw.githubusercontent.com/markwilliams970/apigee-debug-sessions/master/images/screenshot04.png)