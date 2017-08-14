#!/usr/bin/env python3

"""
Created on 17 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Warning: changing system ID components can cause host client access to fail.

Act III of III: Deployment workflow:

    1: ./host_id.py
  > 2: ./system_id.py -d VENDOR_ID -m MODEL_ID -n MODEL_NAME -c CONFIG -s SYSTEM_SERIAL_NUMBER -v
    3: ./api_auth.py -s ORG_ID API_KEY
(   4: ./host_organisation.py -o ORG_ID -n NAME -w WEB -d DESCRIPTION -e EMAIL -v )
    5: ./host_client.py -u USER_ID -l LAT LNG POSTCODE
    6: ./host_project.py -s GROUP LOCATION_ID
    7: ./timezone.py -v -s ZONE

Creates SystemID document.

document example:
{"vendor-id": "scs", "model-id": "ap1", "model": "Alpha Pi Eng", "config": "V1", "system-sn": 6}

command line example:
./system_id.py -v -d SCS -m BGX -n Praxis -c BGX -s 111
"""

import sys

from scs_core.data.json import JSONify
from scs_core.sys.system_id import SystemID

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_system_id import CmdSystemID


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdSystemID()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # check for existing document...
    system_id = SystemID.load_from_host(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if system_id is None and not cmd.is_complete():
            cmd.print_help(sys.stderr)
            exit()

        vendor_id = system_id.vendor_id if cmd.vendor_id is None else cmd.vendor_id
        model_id = system_id.model_id if cmd.model_id is None else cmd.model_id
        model_name = system_id.model_name if cmd.model_name is None else cmd.model_name
        configuration = system_id.configuration if cmd.configuration is None else cmd.configuration
        serial_number = system_id.system_serial_number if cmd.serial_number is None else cmd.serial_number

        system_id = SystemID(vendor_id, model_id, model_name, configuration, serial_number)
        system_id.save(Host)

    print(JSONify.dumps(system_id))

    if cmd.verbose and system_id is not None:
        print("-", file=sys.stderr)
        print("box:   %s" % system_id.box_label(), file=sys.stderr)
        print("topic: %s" % system_id.topic_label(), file=sys.stderr)
        print("tag:   %s" % system_id.message_tag(), file=sys.stderr)
