#!/usr/bin/env python3

"""
Created on 16 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Act I of III: Configuration workflow:

  > 1: ./afe_conf.py -p { 1 | 0 } -v
    2: ./pt1000_conf.py -a ADDR -v
    3: ./sht_conf.py -i INT_ADDR -e EXT_ADDR -v
    4: ./opc_conf.py -s SAMPLE_PERIOD -p { 0 | 1 } -v
    5: ./ndir_conf.py -p { 1 | 0 } -v
    6: ./gps_conf.py -m [MODEL] -v
    7: ./schedule.py [{-s NAME INTERVAL COUNT | -c NAME }] [-v]

Creates AFEConf document.

document example:
{"present": true}

command line example:
./afe_conf.py -p 1 -v
"""

import sys

from scs_core.data.json import JSONify
from scs_dfe.gas.afe_conf import AFEConf
from scs_host.sys.host import Host
from scs_mfr.cmd.cmd_afe_conf import CmdAFEConf


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # SHTConf...
    conf = AFEConf.load_from_host(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdAFEConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit()

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        conf = AFEConf(cmd.pt1000_present)

        conf.save(Host)

    if conf:
        print(JSONify.dumps(conf))
