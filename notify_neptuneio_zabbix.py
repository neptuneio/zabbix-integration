#!/usr/bin/env python

"""
Script to send Zabbix events to Neptune.io

This script is designed to work as an alert media type for Zabbix,
which could be invoked as an action from Zabbix and pass the event
JSON as arguments. To use this script, add this script invocation as
a media type, attach that media type to a user and setup an action
to send message with this media when the alert is triggered or resolved.
Please read the integration guide for more details on how to use this script.
"""

import json
import sys
import time
import urllib2

API_BASE_URL = 'https://www.neptune.io/api/v1/trigger/channel/zabbix/'

if __name__ == "__main__":

    # Get the api key, event subject and body from the arguments.
    (api_key, subject, body) = (sys.argv[1], sys.argv[2], sys.argv[3])

    # Construct full JSON from the body.
    zabbix_event = dict(line.strip().split(':', 1) for line in body.strip().split('\n'))
    zabbix_event['subject'] = subject

    # Send the event to Neptune.
    try:
        for x in range(0, 3):
            try:
                headers = { 'Content-Type': 'application/json' }
                req = urllib2.Request(url=API_BASE_URL + api_key, data=json.dumps(zabbix_event), headers=headers)
                response = urllib2.urlopen(req)
                response = response.read()
                break
            except Exception:
                _, e, _ = sys.exc_info()
                print("Failed to send event to Neptune. Retrying..", repr(e))
                time.sleep(1)
    except Exception:
        _, e, _ = sys.exc_info()
        print("Failed to send the event to Neptune.io; Error: %s", repr(e))
