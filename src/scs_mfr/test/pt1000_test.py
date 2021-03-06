"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_dfe.board.dfe_conf import DFEConf

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class Pt1000Test(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose):
        Test.__init__(self, verbose)


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self):
        if self.verbose:
            print("Pt1000...", file=sys.stderr)

        try:
            I2C.open(Host.I2C_SENSORS)

            # AFE...
            dfe_conf = DFEConf.load(Host)
            afe = dfe_conf.afe(Host)

            # test...
            self.datum = afe.sample_pt1000()

            if self.verbose:
                print(self.datum, file=sys.stderr)

            # test criterion...
            return 0.3 < self.datum.v < 0.4

        finally:
            I2C.close()
