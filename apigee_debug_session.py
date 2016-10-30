import argparse
import os, sys, time
from datetime import datetime

# XML Libs
from xml.etree.ElementTree import XML
from xml.etree.ElementTree import dump as XMLDump

from apigee_management_helper import apigee_management_helper
from apigee_debug_xml_utils import apigee_debug_xml_utils

def main(args):

    # Check for apigee credentials in environment
    try:
        apigee_username       = os.environ['APIGEE_USER']
        apigee_password       = os.environ['APIGEE_PASSWORD']
    except Exception, e:
        print "Please set APIGEE_USER, APIGEE_PASSWORD credentials as environment variables"
        sys.exit(1)

    apigee_config = {
        "mgmt_url"        : args['mgmt_url'],
        "apigee_version"  : "v1",
        "username"        : apigee_username,
        "password"        : apigee_password,
        "organization"    : args['organization'],
        "environment"     : args['environment']
    }

    my_apigee_connection  = apigee_management_helper(apigee_config)
    my_debug_xml_utils        = apigee_debug_xml_utils()

    # Name of Proxy
    proxy                 = args['proxy']

    # Proxy Revision Number (make sure this is the one that is deployed!)
    revision              = args['revision']

    # Length of debug session in seconds
    timeout               = args['timeout']

    # Time in seconds before end of session to start retrieving traces from session
    epsilon               = 30

    # Sleep interval
    sleep                 = timeout - epsilon

    # Start the debug session
    print "Creating the debug session..."
    debug_session_id      = my_apigee_connection.create_debug_session(proxy, revision, timeout)

    print "Debug session %s created..." % debug_session_id

    # Wait for session traces to collect
    print "Collecting traces for %s seconds...." % sleep
    print "This represents a session length of %s seconds" % timeout
    print "_minus_ a pre-defined interval of %s seconds during which trace data is downloaded and processed" % epsilon
    time.sleep(sleep)

    # Collect trace data
    print "Collecting trace data..."
    trace_data            = my_apigee_connection.get_all_trace_data(proxy, revision, debug_session_id)

    if len(trace_data) == 0:
        print "No traces collected!"
        print "This could be because there was no traffic to the proxy %s during the debug session." % proxy
    else:
        # Process trace data
        # Parse xml
        # Output trace data

        xml_file_header = my_debug_xml_utils.get_xml_header(apigee_config['organization'], apigee_config['environment'], proxy, revision)

        # Re-direct stdout to file
        orig_stdout = sys.stdout
        filename    = "%s-%s-%s-%s_%s.xml" % (apigee_config['organization'], apigee_config['environment'], proxy,
                                              revision, debug_session_id)
        output_file = file(filename, 'wb')
        sys.stdout = output_file

        # Output XML File header
        print xml_file_header

        for trace in trace_data:
            trace_id          = trace['trace_id']
            trace_xml_text    = trace['trace_xml']

            trace_xml         = XML(trace_xml_text)

            # Output trace header, including the trace_id
            print my_debug_xml_utils.trace_header(trace_id)

            # Output each trace, omitting trace-by-trace <?xml/> tag
            for elem in trace_xml:
                if len(elem) > 0 and elem is not None:
                    XMLDump(elem)

            # For each trace output the trace footer
            print my_debug_xml_utils.trace_footer()

        # Finally output the XML File footer
        print my_debug_xml_utils.get_xml_footer()

        # Close the output file
        output_file.close()

        # Re-direct stdout back to stdout
        sys.stdout = orig_stdout

        print "Finished! Debug session written to file: %s" % filename

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--management-host', nargs=1, help="The hostname of the management server. Defaults to api.enterprise.apigee.com.",
                                             default="api.enterprise.apigee.com")
    parser.add_argument('--organization',    nargs=1, help="The Apigee organization name, e.g. 'mycompany'")
    parser.add_argument('--environment',     nargs=1, help="The Apigee environment name, e.g. 'test'")
    parser.add_argument('--timeout',         nargs=1, help="The time in seconds during which to collect traces via debugsession. --timeout 300 will run traces for 5 minutes.")
    parser.add_argument('--proxy',           nargs=1, help="The name of the proxy to run traces on, e.g. 'orders'")
    parser.add_argument('--revision',        nargs=1, help="The revision number of the (deployed) proxy to debug, e.g. 2")
    parser.parse_args()

    missing_args = []
    opts = parser.parse_args()

    # Check for needed arguments
    if opts.organization is None:
        missing_args.append('organization')
    if opts.environment is None:
        missing_args.append('environment')
    if opts.timeout is None:
        missing_args.append('timeout')
    if opts.proxy is None:
        missing_args.append('proxy')
    if opts.revision is None:
        missing_args.append('revision')

    if len(missing_args) > 0:
        missing_args_warning = 'Please include all of these arguments: '
        missing_args_list = ', '.join(missing_args)
        print "===================================================="
        print missing_args_warning
        print missing_args_list
        print "===================================================="
        parser.print_help()
        sys.exit(1)

    # De-construct opts array
    try:
        timeout_int = int(opts.timeout[0])
    except Exception, e:
        print "Please use an integer value for timeout."
        sys.exit(1)

    processed_opts = {
        "mgmt_url"     : "https://%s" % (opts.management_host),
        "organization" : opts.organization[0],
        "environment"  : opts.environment[0],
        "timeout"      : timeout_int,
        "proxy"        : opts.proxy[0],
        "revision"     : opts.revision[0]
    }

    main(processed_opts)