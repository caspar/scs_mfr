#!/usr/bin/env python3

"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Act I of III: Configuration workflow:

    1: ./afe_conf.py -p { 1 | 0 } -v
    2: ./pt1000_conf.py -a ADDR -v
    3: ./sht_conf.py -i INT_ADDR -e EXT_ADDR -v
    4: ./opc_conf.py -m MODEL -s SAMPLE_PERIOD -p { 0 | 1 } -v
    5: ./psu_conf.py -p { 1 | 0 } -v
    6: ./ndir_conf.py -p { 1 | 0 } -v
  > 7: ./gps_conf.py -m MODEL -v
    8: ./schedule.py [{-s NAME INTERVAL COUNT | -c NAME }] [-v]

Creates GPSConf document.

document example:
{"model": null}

command line example:
./gps_conf.py -m PAM7Q -v
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.gps.gps_conf import GPSConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_gps_conf import CmdGPSConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # GPSConf...
    conf = GPSConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdGPSConf()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        conf = GPSConf(cmd.model)

        conf.save(Host)

    if conf:
        print(JSONify.dumps(conf))
