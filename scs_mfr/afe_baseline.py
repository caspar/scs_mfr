#!/usr/bin/env python3

"""
Created on 1 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Act II of III: Calibration workflow:

(   1: ./rtc.py -i -s -v )
    2: ./afe_calib -s AFE_SERIAL_NUMBER
    3: ./pt1000_calib.py -s -v
  > 4: ./afe_baseline.py -v -1 SN1_OFFSET -2 SN2_OFFSET -3 SN3_OFFSET -4 SN3_OFFSET

Creates AFEBaseline document.

document example:
{"sn1": {"calibrated_on": "2017-06-20T00:00:00.000+01:00", "offset": 0},
"sn2": {"calibrated_on": "2017-06-20T00:00:00.000+01:00", "offset": 0},
"sn3": {"calibrated_on": "2017-06-20T00:00:00.000+01:00", "offset": 0},
"sn4": {"calibrated_on": "2017-06-20T00:00:00.000+01:00", "offset": 30}}

command line example:
./afe_baseline.py -v -4 30
"""

import sys

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.gas.afe_baseline import AFEBaseline
from scs_core.gas.sensor_baseline import SensorBaseline

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_afe_baseline import CmdAFEBaseline


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAFEBaseline()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    baseline = AFEBaseline.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        now = LocalizedDatetime.now()

        for i, offset in cmd.offsets.items():
            if offset is not None:
                baseline.set_sensor_baseline(i, SensorBaseline(now, offset))

        baseline.save(Host)

    print(JSONify.dumps(baseline))
