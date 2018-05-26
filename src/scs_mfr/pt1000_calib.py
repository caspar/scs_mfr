#!/usr/bin/env python3

"""
Created on 1 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

DESCRIPTION
The pt1000_calib utility is used to determine and save the voltage offset for each Pt1000 sensor.

The utility operates by measuring the temperature using a Sensirion SHT sensor, measuring the voltage output of the
Pt1000 sensor, and back-calculating the voltage offset.

Note that the scs_analysis/gases_sampler process must be restarted for changes to take effect.

SYNOPSIS
pt1000_calib.py [-s] [-v]

EXAMPLES
./pt1000_calib.py -s

DOCUMENT EXAMPLE
{"calibrated-on": "2018-02-27T12:50:28.028+00:00", "v20": 0.321605}

FILES
~/SCS/conf/pt1000_calib.json

SEE ALSO
scs_dev/gases_sampler
scs_mfr/dfe_conf
"""

import sys

from scs_core.data.json import JSONify

from scs_core.gas.pt1000_calib import Pt1000Calib

from scs_dfe.board.dfe_conf import DFEConf
from scs_dfe.climate.sht_conf import SHTConf

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
            print("pt1000_calib: %s" % cmd, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # SHT...
        sht_conf = SHTConf.load(Host)
        sht = sht_conf.int_sht()

        # AFE...
        dfe_conf = DFEConf.load(Host)
        afe = dfe_conf.afe(Host)


        # ------------------------------------------------------------------------------------------------------------
        # run...

        # SHT...
        sht_datum = sht.sample()

        if cmd.verbose:
            print(sht_datum, file=sys.stderr)

        # Pt1000 initial...
        pt1000_datum = afe.sample_pt1000()

        if cmd.set:
            # Pt1000 correction...
            v20 = pt1000_datum.v20(sht_datum.temp)

            pt1000_calib = Pt1000Calib(None, v20)
            pt1000_calib.save(Host)

        # calibrated...
        pt1000_calib = Pt1000Calib.load(Host)

        print(JSONify.dumps(pt1000_calib))

        if cmd.verbose:
            afe = dfe_conf.afe(Host)
            pt1000_datum = afe.sample_pt1000()

            print(pt1000_datum, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    finally:
        I2C.close()
