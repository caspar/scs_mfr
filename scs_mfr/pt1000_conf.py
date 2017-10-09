#!/usr/bin/env python3

"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Act I of III: Configuration workflow:

    1: ./afe_conf.py -p { 1 | 0 } -v
  > 2: ./pt1000_conf.py -a ADDR -v
    3: ./sht_conf.py -i INT_ADDR -e EXT_ADDR -v
    4: ./opc_conf.py -m MODEL -s SAMPLE_PERIOD -p { 0 | 1 } -v
    5: ./psu_conf.py -p { 1 | 0 } -v
    6: ./ndir_conf.py -p { 1 | 0 } -v
    7: ./gps_conf.py -m MODEL -v
    8: ./schedule.py [{-s NAME INTERVAL COUNT | -c NAME }] [-v]

Creates Pt1000Conf document.

document example:
{"addr": "0x69"}

command line example:
./pt1000_conf.py -a 0x69 -v
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.gas.pt1000_conf import Pt1000Conf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_pt1000_conf import CmdPt1000Conf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdPt1000Conf()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # Pt1000Conf...
    conf = Pt1000Conf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # validate...

    if conf is None and cmd.set() and not cmd.is_complete():
        print("No configuration is stored. pt1000_conf must therefore set an I2C address:", file=sys.stderr)
        cmd.print_help(sys.stderr)
        exit(1)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            cmd.print_help(sys.stderr)
            exit(1)

        conf = Pt1000Conf(cmd.addr)
        conf.save(Host)

    if conf:
        print(JSONify.dumps(conf))
