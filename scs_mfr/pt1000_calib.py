#!/usr/bin/env python3

"""
Created on 1 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Act II of III: Calibration workflow:

    1: ./rtc.py -i -s -v
  > 2: ./pt1000_calib.py -s -v
    3: ./afe_calib -s AFE_SERIAL_NUMBER
    4: ./afe_baseline.py -v -1 SN1_OFFSET -2 SN2_OFFSET -3 SN3_OFFSET -4 SN3_OFFSET

Creates Pt1000Calib document.

document example:
{"calibrated_on": "2017-05-18", "v20": 0.508592}

command line example:
./pt1000_calib.py -v
"""

import sys

from scs_core.data.json import JSONify
from scs_core.gas.pt1000_calib import Pt1000Calib
from scs_core.sys.exception_report import ExceptionReport
from scs_dfe.climate.sht_conf import SHTConf
from scs_dfe.gas.afe import AFE
from scs_dfe.gas.pt1000 import Pt1000
from scs_dfe.gas.pt1000_conf import Pt1000Conf
from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host
from scs_mfr.cmd.cmd_pt1000_calib import CmdPt1000Calib


# --------------------------------------------------------------------------------------------------------------------

v20 = 0.295         # a "representative" v20 - we need this to kick the process off


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        I2C.open(Host.I2C_SENSORS)

        # ----------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdPt1000Calib()

        if cmd.verbose:
            print(cmd, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # SHT...
        sht_conf = SHTConf.load_from_host(Host)
        sht = sht_conf.int_sht()

        # Pt1000...
        pt1000_conf = Pt1000Conf.load_from_host(Host)
        pt1000_calib = Pt1000Calib(None, v20)
        pt1000 = Pt1000(pt1000_calib)

        afe = AFE(pt1000_conf, pt1000, [])


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # SHT...
        sht_datum = sht.sample()

        if cmd.verbose:
            print(sht_datum, file=sys.stderr)

        # Pt1000 initial...
        pt1000_datum = afe.sample_temp()

        if cmd.set:
            # Pt1000 correction...
            v20 = pt1000_datum.v20(sht_datum.temp)

            pt1000_calib = Pt1000Calib(None, v20)
            pt1000_calib.save(Host)

            # Pt1000 final...
            if cmd.verbose:
                pt1000 = Pt1000(pt1000_calib)
                afe = AFE(pt1000_conf, pt1000, [])

                pt1000_datum = afe.sample_temp()

                print(pt1000_datum, file=sys.stderr)

        # calibration...
        pt1000_calib = Pt1000Calib.load_from_host(Host)

        print(JSONify.dumps(pt1000_calib))

        if cmd.verbose:
            pt1000_calib = Pt1000Calib.load_from_host(Host)
            pt1000 = Pt1000(pt1000_calib)

            afe = AFE(pt1000_conf, pt1000, [])

            print(pt1000.sample(afe), file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        I2C.close()
