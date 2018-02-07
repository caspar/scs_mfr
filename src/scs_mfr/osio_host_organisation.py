#!/usr/bin/env python3

"""
Created on 8 Mar 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Requires APIAuth document.

command line example:
./osio_host_organisation.py \
-o south-coast-science-dev \
-n 'South Coast Science (Dev)' \
-w https://www.southcoastscience.com \
-d 'development operations for South Coast Science air quality monitoring instruments' \
-e bruno.beloff@southcoastscience.com
"""

import sys

from scs_core.data.json import JSONify

from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.data.organisation import Organisation
from scs_core.osio.manager.organisation_manager import OrganisationManager

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_osio_host_organisation import CmdOSIOHostOrganisation


# TODO: rename as osio_organisation

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOHostOrganisation()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # APIAuth...
    api_auth = APIAuth.load(Host)

    if api_auth is None:
        print("APIAuth not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print(api_auth, file=sys.stderr)
        sys.stderr.flush()

    # manager...
    manager = OrganisationManager(HTTPClient(), api_auth.api_key)

    # check for existing registration...
    org = manager.find(api_auth.org_id)


    # ----------------------------------------------------------------------------------------------------------------
    # validate...

    if org is None and not cmd.is_complete():
        print("No organisation is registered. host_organisation must therefore set all fields:", file=sys.stderr)
        cmd.print_help(sys.stderr)
        exit(1)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        if org:
            name = org.name if cmd.name is None else cmd.name
            website = org.website if cmd.website is None else cmd.website
            description = org.description if cmd.description is None else cmd.description
            email = org.email if cmd.email is None else cmd.email

            # update Organisation...
            updated = Organisation(None, name, website, description, email)
            manager.update(org.id, updated)

            org = manager.find(org.id)

        else:
            if not cmd.is_complete():
                cmd.print_help(sys.stderr)
                exit(1)

            # create Organisation...
            org = Organisation(cmd.org_id, cmd.name, cmd.website, cmd.description, cmd.email)
            manager.create(org)

    else:
        # find self...
        org = manager.find(api_auth.org_id)

    print(JSONify.dumps(org))
