"""
Created on 18 May 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import sys

from scs_dfe.gas.afe_conf import AFEConf
from scs_host.bus.i2c import I2C
from scs_host.sys.host import Host
from scs_mfr.test.test import Test


# --------------------------------------------------------------------------------------------------------------------

class AFETest(Test):
    """
    test script
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, verbose):
        Test.__init__(self, verbose)


    # ----------------------------------------------------------------------------------------------------------------

    def conduct(self):
        if self.verbose:
            print("AFE...", file=sys.stderr)

        try:
            I2C.open(Host.I2C_SENSORS)

            # AFE...
            afe_conf = AFEConf.load_from_host(Host)
            afe = afe_conf.afe(Host)

            # test...
            self.datum = afe.sample()

            if self.verbose:
                print(self.datum, file=sys.stderr)

            ok = True

            # test criterion...
            for gas, sensor in self.datum.sns.items():
                sensor_ok = 0.9 < sensor.we_v < 1.1 and 0.9 < sensor.ae_v < 1.1

                if not sensor_ok:
                    ok = False

            return ok

        finally:
            I2C.close()
