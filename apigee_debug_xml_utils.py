from datetime import datetime

class apigee_debug_xml_utils(object):

    def get_xml_header(self, organization, environment, proxy, revision):
        datetime_string = self.get_iso_datetime_string()

        xml_header = \
            """<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
            <DebugSession>
            <Retrieved>%s</Retrieved>
            <Organization>%s</Organization>
            <Environment>%s</Environment>
            <API>%s</API>
            <Revision>%s</Revision>
            <SessionId></SessionId>
            <Messages>""" % (datetime_string, organization, environment, proxy, revision)

        return xml_header

    def get_xml_footer(self):
        xml_file_footer = \
            """
            </Messages>
            </DebugSession>"""
        return xml_file_footer

    def get_iso_datetime_string(self):
        # The Edge UI can be a bit finicky about the ISO-8601 datetime string. Python outputs
        # 6 digits after the decimal for the seconds. The Edge UI doesn't like this.
        # This function will output an ISO-8601 string with only 3 significant digits after decimal in seconds

        # current date/time
        now = datetime.utcnow()

        significant_digits = 3
        num_digits = significant_digits - 6
        assert num_digits < 0
        now_rounded = now.replace(microsecond=int(round(now.microsecond, num_digits)))
        now_rounded_string = datetime.strftime(now_rounded, '%Y-%m-%dT%H:%M:%S.%fZ')[:num_digits] + 'Z'
        return now_rounded_string

    def trace_header(self, sessionid):
        trace_header_string = \
            """
            <Message>
            <DebugId>%s</DebugId>
            <Data>
            <Completed>true</Completed>""" % sessionid
        return trace_header_string

    def trace_footer(self):
        trace_footer_string = \
            """
            </Data>
            </Message>
            """
        return trace_footer_string