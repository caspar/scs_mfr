"""
Created on 19 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

import optparse


# --------------------------------------------------------------------------------------------------------------------

class CmdHostClient(object):
    """
    unix command line handler
    """

    def __init__(self):
        """
        Constructor
        """
        self.__parser = optparse.OptionParser(usage="%prog [-s [-u USER_ID] [-l LAT LNG POSTCODE] [-d DESCRIPTION] "
                                                    "[-p]] [-v]", version="%prog 1.0")

        # optional...
        self.__parser.add_option("--set", "-s", action="store_true", dest="set", default=False,
                                 help="create or update device")

        self.__parser.add_option("--user", "-u", type="string", nargs=1, action="store", dest="user_id",
                                 help="set user-id (only if device has not yet been registered)")

        self.__parser.add_option("--loc", "-l", type="string", nargs=3, action="store", dest="lat_lng_postcode",
                                 help="set device location (required if device has not yet been registered)")

        self.__parser.add_option("--desc", "-d", type="string", nargs=1, action="store", dest="description",
                                 help="set optional device description")

        self.__parser.add_option("--particulates", "-p", action="store_true", dest="particulates",
                                 help="include particulates tags")

        self.__parser.add_option("--verbose", "-v", action="store_true", dest="verbose", default=False,
                                 help="report narrative to stderr")

        self.__opts, self.__args = self.__parser.parse_args()


    # ----------------------------------------------------------------------------------------------------------------

    def is_complete(self):
        if self.user_id is None or self.__opts.lat_lng_postcode is None:
            return False

        return True


    def set(self):
        return self.__opts.set


    # ----------------------------------------------------------------------------------------------------------------

    @property
    def user_id(self):
        return self.__opts.user_id


    @property
    def lat(self):
        return self.__opts.lat_lng_postcode[0] if self.__opts.lat_lng_postcode else None


    @property
    def lng(self):
        return self.__opts.lat_lng_postcode[1] if self.__opts.lat_lng_postcode else None


    @property
    def postcode(self):
        return self.__opts.lat_lng_postcode[2] if self.__opts.lat_lng_postcode else None


    @property
    def description(self):
        return self.__opts.description


    @property
    def particulates(self):
        return self.__opts.particulates


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
        return "CmdHostClient:{set:%s, user_id:%s, lat:%s, lng:%s, postcode:%s, description:%s, particulates:%s, " \
               "verbose:%s, args:%s}" % \
               (self.set(), self.user_id, self.lat, self.lng, self.postcode, self.description, self.particulates,
                self.verbose, self.args)
