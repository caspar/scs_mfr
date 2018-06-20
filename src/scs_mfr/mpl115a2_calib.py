#!/usr/bin/env python3

"""
Created on 20 Jun 2018

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
text

SYNOPSIS
pt1000_calib [-s] [-v]

EXAMPLES
./mpl115a2_calib.py -s

DOCUMENT EXAMPLE
{"calibrated-on": "2018-06-20T10:25:39.045+00:00", "c25": 511}

FILES
~/SCS/conf/mpl115a2_calib.json

SEE ALSO
scs_dev/gases_sampler
"""

import sys

from scs_core.data.json import JSONify

from scs_core.pressure.mpl115a2_calib import MPL115A2Calib

from scs_dfe.climate.sht_conf import SHTConf
from scs_dfe.pressure.mpl115a2 import MPL115A2

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_mpl115a2_calib import CmdMPL115A2Calib


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        I2C.open(Host.I2C_SENSORS)

        # ----------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdMPL115A2Calib()

        if cmd.verbose:
            print("mpl115a2_calib: %s" % cmd, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # SHT...
        sht_conf = SHTConf.load(Host)
        sht = sht_conf.int_sht()

        # MPL115A2...
        calib = MPL115A2Calib(None, MPL115A2Calib.DEFAULT_C25)
        barometer = MPL115A2(calib)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        barometer.init()

        # SHT...
        sht_datum = sht.sample()

        if cmd.verbose:
            print(sht_datum, file=sys.stderr)

        # MPL115A2 initial...
        datum = barometer.sample()

        if cmd.set:
            # MPL115A2 correction...
            c25 = datum.c25(sht_datum.temp)

            calib = MPL115A2Calib(None, c25)
            calib.save(Host)

            calib = MPL115A2Calib.load(Host)

        print(JSONify.dumps(calib))

        if cmd.verbose:
            barometer = MPL115A2(calib)
            barometer.init()

            datum = barometer.sample()

            print(datum, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    finally:
        I2C.close()