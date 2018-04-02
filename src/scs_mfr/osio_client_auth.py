#!/usr/bin/env python3

"""
Created on 18 Feb 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Part 3 of 3: Communication:

    1: ./shared_secret.py -g
    2: ./system_id.py -d VENDOR_ID -m MODEL_ID -n MODEL_NAME -c CONFIG -s SYSTEM_SERIAL_NUMBER -v
    3: ./osio_api_auth.py -s ORG_ID API_KEY
  > 4: ./osio_client_auth.py -u USER_ID -l LAT LNG POSTCODE
    5: ./osio_host_project.py -v -s GROUP LOCATION_ID

Requires APIAuth and SystemID documents.

Creates ClientAuth document.

document example:
{"user_id": "southcoastscience-dev", "client-id": "5403", "client-password": "rtxSrK2f"}

command line example:
./osio_client_auth.py -u south-coast-science-test-user -l 50.823130 -0.122922 "BN2 0DF" -v
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

from scs_mfr.cmd.cmd_osio_client_auth import CmdOSIOClientAuth


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdOSIOClientAuth()

    if cmd.verbose:
        print(cmd, file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # OPCConf...
    opc_conf = OPCConf.load(Host)

    if cmd.verbose:
        print(opc_conf, file=sys.stderr)

    # APIAuth...
    api_auth = APIAuth.load(Host)

    if api_auth is None:
        print("APIAuth not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print(api_auth, file=sys.stderr)

    # SystemID...
    system_id = SystemID.load(Host)

    if system_id is None:
        print("SystemID not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print(system_id, file=sys.stderr)

    # AFECalib...
    afe_calib = AFECalib.load(Host)

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

    # TODO: check whether remote device and local client auth match

    if device is None:
        if cmd.set() and not cmd.is_complete():
            print("No device is registered. osio_host_client must therefore set a user and location:", file=sys.stderr)
            cmd.print_help(sys.stderr)
            exit(1)

        if not cmd.set():
            exit(0)


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
        include_particulates = False if opc_conf is None else opc_conf.has_monitor()
        tags = ProjectSource.tags(afe_calib, include_particulates)

        if device:
            if cmd.user_id:
                print("Device owner-id cannot be updated.", file=sys.stderr)
                exit(1)

            # find ClientAuth...
            client_auth = ClientAuth.load(Host)

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
        client_auth = ClientAuth.load(Host)

    if cmd.verbose:
        print(client_auth, file=sys.stderr)

    print(JSONify.dumps(device))
