import json
import os, sys, time
import pprint

from apigee_management_helper import apigee_management_helper

# Check for apigee credentials in environment
try:
    apigee_username       = os.environ['APIGEE_USER']
    apigee_password       = os.environ['APIGEE_PASSWORD']
except Exception, e:
    print "Please set APIGEE_USER, APIGEE_PASSWORD credential environment variables"
    sys.exit()

apigee_config = {
    "mgmt_url"        : "https://api.enterprise.apigee.com",
    "apigee_version"  : "v1",
    "username"        : apigee_username,
    "password"        : apigee_password,
    "organization"    : "my_organization",
    "environment"     : "test"
}

my_apigee_connection = apigee_management_helper(apigee_config)

# Name of Proxy
apiname               = "my_api_proxy"

# Proxy Revision Number (make sure this is the one that is deployed!)
revision_number       = 2

# Length of debug session in seconds
session_timeout       = 120

# Time in seconds before end of session to start retrieving traces from session
epsilon               = 30

# Sleep interval
sleep                 = session_timeout - epsilon

# Start the debug session
print "Creating the debug session..."
debug_session_id      = my_apigee_connection.create_debug_session(apiname, revision_number, session_timeout)

print "Debug session %s created..." % debug_session_id

# Wait for session traces to collect
print "Collecting traces for %s seconds...." % sleep
time.sleep(epsilon)

# Collect trace data
print "Collecting trace data..."
trace_data            = my_apigee_connection.get_all_trace_data(apiname, revision_number, debug_session_id)

# Output trace data
for trace in trace_data:
   print trace