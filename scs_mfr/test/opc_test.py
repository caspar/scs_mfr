"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_dfe.particulate.opc_n2 import OPCN2

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class OPCTest(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose):
        Test.__init__(self, verbose)


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self):
        if self.verbose:
            print("OPC...", file=sys.stderr)

        opc = None

        try:
            I2C.open(Host.I2C_SENSORS)

            # resources...
            opc = OPCN2()
            opc.power_on()
            opc.operations_on()

            # test...
            self.datum = opc.firmware()

            if self.verbose:
                print(self.datum, file=sys.stderr)

            # test criterion...
            return len(self.datum) > 0 and self.datum.startswith('OPC')

        finally:
            if opc:
                opc.operations_off()
                opc.power_off()

            I2C.close()
