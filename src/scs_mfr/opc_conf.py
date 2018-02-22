#!/usr/bin/env python3

"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Part 1 of 3: Configuration:

    1: ./afe_conf.py -p { 1 | 0 } -v
    2: ./pt1000_conf.py -a ADDR -v
    3: ./sht_conf.py -i INT_ADDR -e EXT_ADDR -v
  > 4: ./opc_conf.py -m MODEL -s SAMPLE_PERIOD -p { 0 | 1 } -v
    5: ./psu_conf.py -m { PrototypeV1 | OsloV1 } -v
    6: ./ndir_conf.py -p { 1 | 0 } -v
    7: ./gps_conf.py -m MODEL -v
    8: ./schedule.py [{-s NAME INTERVAL COUNT | -c NAME }] [-v]

Creates OPCConf document.

document example:
{"model": "N2", "sample-period": 10, "power-saving": false}

command line example:
./opc_conf.py -m N2 -s 10 -p 0 -v
"""

import sys

from scs_core.data.json import JSONify

from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_opc_conf import CmdOPCConf


# TODO: needs a way of indicating "no OPC"

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOPCConf()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)

    if cmd.verbose:
        print(cmd, file=sys.stderr)
        sys.stderr.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # OPCConf...
    conf = OPCConf.load(Host)


    # ----------------------------------------------------------------------------------------------------------------
    # validate...

    if conf is None and cmd.set() and not cmd.is_complete():
        print("No configuration is stored. opc_conf must therefore set all fields:", file=sys.stderr)
        cmd.print_help(sys.stderr)
        exit(1)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if conf is None and not cmd.is_complete():
            cmd.print_help(sys.stderr)
            exit(1)

        model = cmd.model if cmd.model else conf.model
        sample_period = cmd.sample_period if cmd.sample_period else conf.sample_period
        power_saving = cmd.power_saving if cmd.power_saving is not None else conf.power_saving

        conf = OPCConf(model, sample_period, power_saving)

        conf.save(Host)

    if conf:
        print(JSONify.dumps(conf))
