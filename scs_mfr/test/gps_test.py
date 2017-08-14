"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_core.position.gprmc import GPRMC

from scs_dfe.gps.pam7q import PAM7Q

from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host

from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class GPSTest(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose):
        Test.__init__(self, verbose)


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self):
        if self.verbose:
            print("GPS...", file=sys.stderr)

        gps = None

        try:
            I2C.open(Host.I2C_SENSORS)

            # GPS...
            gps = PAM7Q()

            gps.power_on()
            gps.open()

            # test...
            self.datum = gps.report(GPRMC)

            if self.verbose:
                print(self.datum, file=sys.stderr)

            # criterion...
            return self.datum is not None

        finally:
            if gps:
                gps.close()
                gps.power_off()

            I2C.close()
