"""
Created on 20 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from serial import Serial

from scs_mfr.power.power_datum import PowerDatum


# TODO: put device references in Host

# --------------------------------------------------------------------------------------------------------------------

class PowerMeter(object):
    """
    classdocs
    """
    __MAX_CURR = 969.0

    __DEVICE = '/dev/ttyUSB0'           # hard-coded path '/dev/tty.usbserial-A4014EG7'


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        """
        Constructor
        """
        self.__ser = Serial(PowerMeter.__DEVICE, 115200, timeout=1.0)


    # ----------------------------------------------------------------------------------------------------------------

    def reset(self):
        while True:
            if self.sample is not None:
                return


    @property
    def sample(self):
        line = self.__ser.readline().decode("utf-8")

        if len(line) < 1:
            return None

        if len(line) > 2:
            line = line[:-2]

        values = line.split(',')

        if len(values) < 2:
            return None

        try:
            raw_current = float(values[0])
            raw_voltage = float(values[1])
        except RuntimeError:
            return None

        amps = (PowerMeter.__MAX_CURR - raw_current) * 0.0067
        volts = raw_voltage * 11.0 / 200.0

        return PowerDatum(amps, volts)


    def close(self):
        self.__ser.close()


    # ----------------------------------------------------------------------------------------------------------------

    def __str__(self, *args, **kwargs):
        return "PowerMeter:{ser:%s}" % self.__ser
