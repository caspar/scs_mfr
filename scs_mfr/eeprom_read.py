#!/usr/bin/env python3

"""
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import subprocess
import sys

from scs_core.data.json import JSONify
from scs_core.sys.exception_report import ExceptionReport

from scs_dfe.board.cat24c32 import CAT24C32
from scs_dfe.bus.i2c import I2C

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

Host.enable_eeprom_write()


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    try:
        I2C.open(Host.I2C_EEPROM)


        # ------------------------------------------------------------------------------------------------------------
        # resource...

        eeprom = CAT24C32()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        eeprom.image.formatted(32)


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    # except Exception as ex:
    #     print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        I2C.close()
