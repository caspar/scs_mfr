"""
Created on 16 Jul 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdAFEConf(object):
    """unix command line handler"""

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-p { 1 | 0 }] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--pt1000-present", "-p", type="int", nargs=1, action="store", dest="pt1000_present",
                                 help="set Pt1000 as pt1000_present or absent")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_valid(self):
        if self.__opts.pt1000_present is None or self.__opts.pt1000_present == 0 or self.__opts.pt1000_present == 1:
            return True

        return False


    # ----------------------------------------------------------------------------------------------------------------

    def set(self):
        return self.pt1000_present is not None


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def pt1000_present(self):
        return bool(self.__opts.pt1000_present) if self.__opts.pt1000_present is not None else None


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
        return "CmdAFEConf:{pt1000_present:%s, verbose:%s, args:%s}" % \
                    (self.pt1000_present, self.verbose, self.args)
