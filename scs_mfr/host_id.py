#!/usr/bin/env python3

"""
Created on 16 Apr 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

WARNING: for Raspberry Pi, the host ID appears to be derrived from the MAC address of the active interface.

Act III of III: Deployment workflow:

  > 1: ./host_id.py
    2: ./system_id.py -d VENDOR_ID -m MODEL_ID -n MODEL_NAME -c CONFIG -s SYSTEM_SERIAL_NUMBER -v
    3: ./osio_api_auth.py -s ORG_ID API_KEY
(   4: ./osio_host_organisation.py -o ORG_ID -n NAME -w WEB -d DESCRIPTION -e EMAIL -v )
    5: ./osio_host_client.py -u USER_ID -l LAT LNG POSTCODE
    6: ./osio_host_project.py -s GROUP LOCATION_ID
    7: ./timezone.py -v -s ZONE

command line example:
./host_id.py
"""

from scs_core.data.json import JSONify

from scs_host.sys.host import Host


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':
    serial_number = Host.serial_number()

    print(JSONify.dumps(serial_number))
