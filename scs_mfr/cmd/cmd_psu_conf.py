"""
Created on 21 Jun 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdPSUConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-p { 1 | 0 }] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--present", "-p", type="int", nargs=1, action="store", dest="present",
                                 help="set PSU as present or absent")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__opts.present is None or self.__opts.present == 0 or self.__opts.present == 1:
            return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.present is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def present(self):
        return bool(self.__opts.present) if self.__opts.present is not None else None


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
        return "CmdPSUConf:{present:%s, verbose:%s, args:%s}" % \
                    (self.present, self.verbose, self.args)
