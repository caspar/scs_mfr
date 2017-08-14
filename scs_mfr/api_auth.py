#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Act III of III: Deployment workflow:

    1: ./host_id.py
    2: ./system_id.py -d VENDOR_ID -m MODEL_ID -n MODEL_NAME -c CONFIG -s SYSTEM_SERIAL_NUMBER -v
  > 3: ./api_auth.py -s ORG_ID API_KEY
(   4: ./host_organisation.py -o ORG_ID -n NAME -w WEB -d DESCRIPTION -e EMAIL -v )
    5: ./host_client.py -u USER_ID -l LAT LNG POSTCODE
    6: ./host_project.py -s GROUP LOCATION_ID
    7: ./timezone.py -v -s ZONE

Creates APIAuth document.

document example:
{"org-id": "south-coast-science-test-user", "api-key": "9fdfb841-3433-45b8-b223-3f5a283ceb8e"}

command line example:
./api_auth.py -v -s south-coast-science-test 9fdfb841-3433-45b8-b223-3f5a283ceb8e
"""

import sys

from scs_core.data.json import JSONify

from scs_core.osio.client.api_auth import APIAuth

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_api_auth import CmdAPIAuth


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAPIAuth()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        auth = APIAuth(cmd.org_id, cmd.api_key)
        auth.save(Host)

    else:
        # find self...
        auth = APIAuth.load_from_host(Host)

    print(JSONify.dumps(auth))
