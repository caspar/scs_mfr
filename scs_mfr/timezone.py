#!/usr/bin/env python3

"""
Created on 12 Aug 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Act III of III: Deployment workflow:

    1: ./host_id.py
    2: ./system_id.py -d VENDOR_ID -m MODEL_ID -n MODEL_NAME -c CONFIG -s SYSTEM_SERIAL_NUMBER -v
    3: ./osio_api_auth.py -s ORG_ID API_KEY
(   4: ./osio_host_organisation.py -o ORG_ID -n NAME -w WEB -d DESCRIPTION -e EMAIL -v )
    5: ./osio_host_client.py -u USER_ID -l LAT LNG POSTCODE
    6: ./osio_host_project.py -s GROUP LOCATION_ID
  > 7: ./timezone.py -v -s ZONE

Creates TimezoneConf document.

document example:
{"set-on": "2017-08-12T11:20:28.740+00:00", "name": "Europe/London"}

command line example:
./timezone.py -s Europe/London -v
"""

import sys

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.location.timezone import Timezone
from scs_core.location.timezone_conf import TimezoneConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_timezone import CmdTimezone


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdTimezone()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    conf = TimezoneConf.load_from_host(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    now = LocalizedDatetime.now()

    if cmd.list:
        for zone in Timezone.zones():
            print(zone, file=sys.stderr)
        exit(0)

    elif cmd.set():
        if not Timezone.is_valid(cmd.zone):
            print("zone is not valid: %s" % cmd.zone, file=sys.stderr)
            exit(1)

        if cmd.zone != conf.name:
            conf = TimezoneConf(now, cmd.zone)
            conf.save(Host)

    elif cmd.link:
        if not conf.uses_system_name() or conf.set_on is None:
            conf = TimezoneConf(now, None)
            conf.save(Host)

    print(JSONify.dumps(conf))

    if cmd.verbose:
        print(JSONify.dumps(conf.timezone()), file=sys.stderr)

