#!/usr/bin/env python3

"""
Created on 27 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Act II of III: Calibration workflow:

    1: ./rtc.py -i -s -v
    2: ./pt1000_calib.py -s -v
  > 3: ./afe_calib -s AFE_SERIAL_NUMBER
    4: ./afe_baseline.py -v -1 SN1_OFFSET -2 SN2_OFFSET -3 SN3_OFFSET -4 SN3_OFFSET

Creates AFECalib document.

command line example:
./afe_calib.py -v -s 15-000064
"""

import json
import sys
from collections import OrderedDict

from scs_core.data.json import JSONify
from scs_core.gas.afe_calib import AFECalib
from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host
from scs_mfr.cmd.cmd_afe_calib import CmdAFECalib


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAFECalib()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if cmd.test:
            jstr = AFECalib.TEST_JSON

        else:
            client = HTTPClient()
            client.connect(AFECalib.HOST)

            try:
                path = AFECalib.PATH + cmd.serial_number
                jstr = client.get(path, None, AFECalib.HEADER)

            finally:
                client.close()

        jdict = json.loads(jstr, object_pairs_hook=OrderedDict)

        calib = AFECalib.construct_from_jdict(jdict)

        if calib is not None:
            calib.save(Host)

    calib = AFECalib.load_from_host(Host)

    print(JSONify.dumps(calib))
