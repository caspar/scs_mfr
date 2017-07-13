"""
Created on 13 Jul 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdPt1000Conf(object):
    """
    unix command line handler
    """

    # ----------------------------------------------------------------------------------------------------------------

    @classmethod
    def __addr_str(cls, addr):
        if addr is None:
            return None

        return "0x%02x" % addr


    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self):
        self.__parser = optparse.OptionParser(usage="%prog [-a ADDR] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--addr", "-a", type="int", nargs=1, action="store", dest="addr", default=None,
                                 help="set I2C address of the Pt1000 ADC (required if conf has not yet been set)")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_complete(self):
        if self.addr is None:
            return False

        return True


    def set(self):
        return self.addr is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def addr(self):
        return self.__opts.addr


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
        return "CmdPt1000Conf:{addr:%s, verbose:%s, args:%s}" % \
               (CmdPt1000Conf.__addr_str(self.addr), self.verbose, self.args)
