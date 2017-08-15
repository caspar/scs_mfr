# scs_mfr
High-level scripts and command-line applications for South Coast Science environmental monitor manufacturing, test and calibration.

**Required libraries:** 

* Third party: paho-mqtt, pyserial
* SCS root:  scs_core
* SCS host:  scs_host_bbe or scs_host_rpi
* SCS dfe:   scs_dfe_eng
* SCS NDIR:  scs_ndir_alphasense
* SCS PSU:   scs_psu


**Example PYTHONPATH:**

**Raspberry Pi, in /home/pi/.bashrc:**

export \\
PYTHONPATH=\~/SCS/scs_analysis:\~/SCS/scs_dev:\~/SCS/scs_osio:\~/SCS/scs_mfr:\~/SCS/scs_dfe_eng:\~/SCS/scs_ndir_alphasense:\~/SCS/scs_host_rpi:\~/SCS/scs_core:$PYTHONPATH


**Beaglebone, in /root/.bashrc:**

export \\
PYTHONPATH=/home/debian/SCS/scs_dev:/home/debian/SCS/scs_osio:/home/debian/SCS/scs_mfr:/home/debian/SCS/scs_psu:/home/debian/SCS/scs_comms_ge910:/home/debian/SCS/scs_dfe_eng:/home/debian/SCS/scs_ndir_alphasense:/home/debian/SCS/scs_host_bbe:/home/debian/SCS/scs_core:$PYTHONPATH


**Beaglebone, in /home/debian/.bashrc:**

export \\
PYTHONPATH=\~/SCS/scs_dev:\~/SCS/scs_osio:\~/SCS/scs_mfr:\~/SCS/scs_psu:\~/SCS/scs_comms_ge910:\~/SCS/scs_dfe_eng:\~/SCS/scs_ndir_alphasense:\~/SCS/scs_host_bbe:\~/SCS/scs_core:$PYTHONPATH



Act I: Configuration workflow:

    1: ./afe_conf.py -p { 1 | 0 } -v
    2: ./pt1000_conf.py -a ADDR -v
    3: ./sht_conf.py -i INT_ADDR -e EXT_ADDR -v
    4: ./opc_conf.py -m MODEL -s SAMPLE_PERIOD -p { 0 | 1 } -v
    5: ./psu_conf.py -p { 1 | 0 } -v
    6: ./ndir_conf.py -p { 1 | 0 } -v
    7: ./gps_conf.py -m MODEL -v
    8: ./schedule.py [{-s NAME INTERVAL COUNT | -c NAME }] [-v]


Act II: Calibration workflow:

    1: ./rtc.py -i -s -v 
    2: ./afe_calib -s AFE_SERIAL_NUMBER
    3: ./pt1000_calib.py -s -v
    4: ./afe_baseline.py -v -1 SN1_OFFSET -2 SN2_OFFSET -3 SN3_OFFSET -4 SN3_OFFSET


Act III: Deployment workflow:

    1: ./host_id.py
    2: ./system_id.py -d VENDOR_ID -m MODEL_ID -n MODEL_NAME -c CONFIG -s SYSTEM_SERIAL_NUMBER -v
    3: ./api_auth.py -s ORG_ID API_KEY
    4: ./host_organisation.py -o ORG_ID -n NAME -w WEB -d DESCRIPTION -e EMAIL -v  
    5: ./host_client.py -u USER_ID -l LAT LNG POSTCODE
    6: ./host_project.py -s GROUP LOCATION_ID
    7: ./timezone.py -v -s ZONE

