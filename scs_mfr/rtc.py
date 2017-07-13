#!/usr/bin/env python3

"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Act II of III: Calibration workflow:

  > 1: ./rtc.py -i -s -v
    2: ./pt1000_calib.py -s -v
    3: ./afe_calib -s AFE_SERIAL_NUMBER
    4: ./afe_baseline.py -v -1 SN1_OFFSET -2 SN2_OFFSET -3 SN3_OFFSET -4 SN3_OFFSET

command line example:
./rtc.py -v
"""

import sys

import tzlocal

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime
from scs_core.data.rtc_datetime import RTCDatetime
from scs_dfe.time.ds1338 import DS1338
from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host
from scs_mfr.cmd.cmd_rtc import CmdRTC


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdRTC()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    now = LocalizedDatetime.now()

    if cmd.verbose:
        print("system time: %s" % now, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    try:
        I2C.open(Host.I2C_SENSORS)

        if cmd.initialise:
            DS1338.init()

        if cmd.set:
            rtc_datetime = RTCDatetime.construct_from_localized_datetime(now)
            DS1338.set_time(rtc_datetime)

        # get current...
        rtc_datetime = DS1338.get_time()
        localized_datetime = rtc_datetime.as_localized_datetime(tzlocal.get_localzone())

        if cmd.verbose:
            print("rtc datetime: %s" % localized_datetime, file=sys.stderr)
            sys.stderr.flush()

        print(JSONify.dumps(localized_datetime))

    finally:
        I2C.close()
