"""
Created on 29 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.sample.sample import Sample


# --------------------------------------------------------------------------------------------------------------------

class DFETestDatum(Sample):
    """
    classdocs
    """

    # ----------------------------------------------------------------------------------------------------------------

    def __init__(self, tag, rec, host_serial_number, dfe_serial_number, subjects, afe, result):
        """
        Constructor
        """
        super().__init__(tag, rec, ('host-sn', host_serial_number), ('dfe-sn', dfe_serial_number), ('result', result),
                         ('subjects', subjects), ('afe', afe))
