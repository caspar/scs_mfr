#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Act III of III: Deployment workflow:

    1: ./host_id.py
    2: ./system_id.py -d VENDOR_ID -m MODEL_ID -n MODEL_NAME -c CONFIG -s SYSTEM_SERIAL_NUMBER -v
    3: ./api_auth.py -s ORG_ID API_KEY
(   4: ./host_organisation.py -o ORG_ID -n NAME -w WEB -d DESCRIPTION -e EMAIL -v )
  > 5: ./host_client.py -u USER_ID -l LAT LNG POSTCODE
    6: ./host_project.py -s GROUP LOCATION_ID
    7: ./timezone.py -v -s ZONE

Requires APIAuth and SystemID documents.

Creates ClientAuth document.

document example:
{"user_id": "southcoastscience-dev", "client-id": "5403", "client-password": "rtxSrK2f"}

command line examples:
./host_client.py -u south-coast-science-test-user -l 50.823130 -0.122922 "BN2 0DF" -v
./host_client.py -u southcoastscience-dev -l 51.865448 0.521049 CM77 7AA -v
./host_client.py -u southcoastscience-dev -l 52.197832 0.125050 CB2 1EW -v
"""

import sys

from scs_core.data.json import JSONify

from scs_core.gas.afe_calib import AFECalib

from scs_core.osio.client.api_auth import APIAuth
from scs_core.osio.client.client_auth import ClientAuth
from scs_core.osio.config.project_source import ProjectSource
from scs_core.osio.manager.device_manager import DeviceManager
from scs_core.osio.manager.user_manager import UserManager

from scs_core.sys.system_id import SystemID

from scs_dfe.particulate.opc_conf import OPCConf

from scs_host.client.http_client import HTTPClient
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_host_client import CmdHostClient


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdHostClient()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # OPCConf...
    opc_conf = OPCConf.load_from_host(Host)

    if cmd.verbose:
        print(opc_conf, file=sys.stderr)

    # APIAuth...
    api_auth = APIAuth.load_from_host(Host)

    if api_auth is None:
        print("APIAuth not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print(api_auth, file=sys.stderr)

    # SystemID...
    system_id = SystemID.load_from_host(Host)

    if system_id is None:
        print("SystemID not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print(system_id, file=sys.stderr)

    # AFECalib...
    afe_calib = AFECalib.load_from_host(Host)

    if afe_calib is None:
        print("AFECalib not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print(afe_calib, file=sys.stderr)
        sys.stderr.flush()

    # User manager...
    user_manager = UserManager(HTTPClient(), api_auth.api_key)

    # Device manager...
    device_manager = DeviceManager(HTTPClient(), api_auth.api_key)

    # check for existing registration...
    device = device_manager.find_for_name(api_auth.org_id, system_id.box_label())


    # ----------------------------------------------------------------------------------------------------------------
    # validate...

    if device is None and not cmd.is_complete():
        print("No device is registered. host_client must therefore set a user and location:", file=sys.stderr)
        cmd.print_help(sys.stderr)
        exit(1)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    if cmd.set():
        # User...
        if cmd.user_id:
            user = user_manager.find_public(cmd.user_id)

            if user is None:
                print("User not available.", file=sys.stderr)
                exit(1)

        # tags...
        tags = ProjectSource.tags(afe_calib, opc_conf.has_monitor())

        if device:
            if cmd.user_id:
                print("Device owner-id cannot be updated.", file=sys.stderr)
                exit(1)

            # find ClientAuth...
            client_auth = ClientAuth.load_from_host(Host)

            # update Device...
            updated = ProjectSource.update(device, cmd.lat, cmd.lng, cmd.postcode, cmd.description, tags)
            device_manager.update(api_auth.org_id, device.client_id, updated)

            # find updated device...
            device = device_manager.find(api_auth.org_id, device.client_id)

        else:
            # create Device...
            device = ProjectSource.create(system_id, api_auth, cmd.lat, cmd.lng, cmd.postcode, cmd.description, tags)
            device = device_manager.create(cmd.user_id, device)

            # create ClientAuth...
            client_auth = ClientAuth(cmd.user_id, device.client_id, device.password)
            client_auth.save(Host)

    else:
        # find ClientAuth...
        client_auth = ClientAuth.load_from_host(Host)

    if cmd.verbose:
        print(client_auth, file=sys.stderr)

    print(JSONify.dumps(device))
