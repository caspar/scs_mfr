#!/usr/bin/env python3

"""
Created on 26 Sep 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)
"""

from scs_core.data.json import JSONify

from scs_dfe.board.dfe_product_id import DFEProductID


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ------------------------------------------------------------------------------------------------------------
    # resources...

    product_id = DFEProductID()

    # ------------------------------------------------------------------------------------------------------------
    # run...

    jstr = JSONify.dumps(product_id)
    print(jstr)
