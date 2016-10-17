import sys, os, warnings
import requests
import json
import uuid

class apigee_management_helper(object):

    def __init__(self, config):
        self.mgmt_url          = config.get('mgmt_url', 'https://api.enterprise.apigee.com') # Apigee mgmt url
        self.apigee_version    = config.get('apigee_version', 'v1')   # API version, i.e. 'v1'
        self.organization      = config['organization']               # Name of user's organization
        self.environment       = config['environment']                # Name of user's environment
        self.config            = config

        # Instantiate a session with some default configuration params
        self.session           = requests.Session()
        self.session.timeout   = 10.0
        self.session.verify    = True

        # setup the client authentication method
        self.set_client_auth()

    # Client authentication settings
    def set_client_auth(self):
        self.session.headers   = {}
        self.username          = self.config['username']
        self.password          = self.config['password']
        self.session.auth      = requests.auth.HTTPBasicAuth(self.username, self.password)

    # Create nicely-formatted string UUIDs
    def get_uuid_string(self):
        # Create the UUID object
        uuid_var = uuid.uuid4()
        uuid_str = uuid_var.urn

        # Strip off the pre-pended part of the urn output (8 chars)
        nice_uuid = uuid_str[9:]
        return nice_uuid

    # Debug session url
    def create_debug_session_url(self, sessionid, apiname, revision, timeout):
        return "%s/%s/organizations/%s/environments/%s/apis/%s/revisions/%s/debugsessions?session=%s&timeout=%s" % \
               (self.mgmt_url, self.apigee_version, self.organization, self.environment, apiname,
                revision, sessionid, timeout)

    # Create debug session
    def create_debug_session(self, apiname, revision, timeout):
        # Create a UUID to use as a debug session id
        sessionid = self.get_uuid_string()

        # Set request headers
        request_headers = {
            "Content-Type": "application/x-www-url-form-encoded"
        }

        # Create url
        debug_session_url = self.create_debug_session_url(sessionid, apiname, revision, timeout)

        response = self.session.post(debug_session_url, data={}, headers=request_headers)
        if response.status_code != 201:
            warnings.warn("Error creating Debug session for Revision %s of %s in Environment %s" % (revision, apiname,
                self.environment))
        else:
            print "Created Debug session %s for Revision %s of %s in Environment %s" % (sessionid, revision, apiname,
                self.environment)
        return sessionid

    # Trace list url
    def create_trace_list_url(self, apiname, revision, sessionid):
        return "%s/%s/organizations/%s/environments/%s/apis/%s/revisions/%s/debugsessions/%s/data" % \
               (self.mgmt_url, self.apigee_version, self.organization, self.environment, apiname, revision,
                sessionid)

    # Get list of traces
    def get_trace_list(self, apiname, revision, sessionid):
        trace_list_url = self.create_trace_list_url(apiname, revision, sessionid)

        # Request headers
        request_headers = {
            "Accept": "application/xml"
        }

        trace_list_response = self.session.get(trace_list_url)
        traces_dict = json.loads(trace_list_response.text, 'utf-8')
        return traces_dict

    # Create trace data url
    def create_trace_data_url(self, apiname, revision, sessionid, traceid):
        return "%s/%s/organizations/%s/environments/%s/apis/%s/revisions/%s/debugsessions/%s/data/%s" % \
               (self.mgmt_url, self.apigee_version, self.organization, self.environment, apiname, revision,
                sessionid, traceid)

    # Get the trace data for a single trace
    def get_trace_data(self, apiname, revision, sessionid, traceid):
        trace_data_url = self.create_trace_data_url(apiname, revision, sessionid, traceid)

        # Request headers
        request_headers = {
            "Accept": "application/xml"
        }

        trace_response = self.session.get(trace_data_url, headers=request_headers)
        return trace_response.content

    # Loop through list of traces and iteratively retrieve trace data
    def get_all_trace_data(self, apiname, revision, sessionid):
        # First get trace list
        trace_list = self.get_trace_list(apiname, revision, sessionid)

        traces_array = []

        for trace_id in trace_list:
            trace_data = self.get_trace_data(apiname, revision, sessionid, trace_id)
            traces_array.append({"trace_id":trace_id, "trace_data":trace_data})

        return traces_array