"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdOPCConf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [-m MODEL] [-s SAMPLE_PERIOD] [-p { 0 | 1 }] [-v]",
                                              version="%prog 1.0")

        # optional...
        self.__parser.add_option("--model", "-m", type="string", nargs=1, action="store", dest="model",
                                 help="set MODEL (required if conf has not yet been set)")

        self.__parser.add_option("--sample-period", "-s", type="int", nargs=1, action="store", dest="sample_period",
                                 help="set SAMPLE_PERIOD (required if conf has not yet been set)")

        self.__parser.add_option("--power-saving", "-p", type="int", nargs=1, action="store", dest="power_saving",
                                 help="set power saving mode (required if conf has not yet been set)")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__opts.power_saving is None or self.__opts.power_saving == 0 or self.__opts.power_saving == 1:
            return True

        return False


    def is_complete(self):
        if self.model is None or self.sample_period is None or self.power_saving is None:
            return False

        return True


    def set(self):
        return self.model is not None or self.sample_period is not None or self.power_saving is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def model(self):
        return self.__opts.model


    @property
    def sample_period(self):
        return self.__opts.sample_period


    @property
    def power_saving(self):
        return bool(self.__opts.power_saving) if self.__opts.power_saving is not None else None


    @property
    def verbose(self):
        return self.__opts.verbose


    @property
    def args(self):
        return self.__args


    # ----------------------------------------------------------------------------------------------------------------

    def print_help(self, file):
        self.__parser.print_help(file)


    def __str__(self, *args, **kwargs):
        return "CmdOPCConf:{model:%s, sample_period:%s, ext_addr:%s, verbose:%s, args:%s}" % \
               (self.model, self.sample_period, self.power_saving, self.verbose, self.args)
