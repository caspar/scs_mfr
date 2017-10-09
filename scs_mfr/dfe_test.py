#!/usr/bin/env python3

# noinspection PyUnboundLocalVariable
"""
Created on 29 Jan 2017

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

A standard load should be connected to the DFE's AFE port before this test is run.

command line example:
./dfe_test.py 123 -g -v
"""

import sys

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.sys.system_id import SystemID

from scs_dfe.climate.sht_conf import SHTConf

from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_dfe_test import CmdDFETest

from scs_mfr.report.dfe_test_datum import DFETestDatum
from scs_mfr.report.dfe_test_reporter import DFETestReporter

from scs_mfr.test.afe_test import AFETest
from scs_mfr.test.board_temp_test import BoardTempTest
from scs_mfr.test.eeprom_test import EEPROMTest
from scs_mfr.test.gps_test import GPSTest
from scs_mfr.test.opc_test import OPCTest
from scs_mfr.test.pt1000_test import Pt1000Test
from scs_mfr.test.rtc_test import RTCTest
from scs_mfr.test.sht_test import SHTTest


# TODO: add UUID read

# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    # ----------------------------------------------------------------------------------------------------------------
    # cmd...

    cmd = CmdDFETest()

    if not cmd.is_valid():
        cmd.print_help(sys.stderr)
        exit(2)


    # ----------------------------------------------------------------------------------------------------------------
    # resources...

    # SystemID...
    system_id = SystemID.load(Host)

    if system_id is None:
        print("SystemID not available.", file=sys.stderr)
        exit(1)

    if cmd.verbose:
        print(system_id, file=sys.stderr)
        sys.stderr.flush()

    reporter = DFETestReporter(cmd.verbose)


    # ----------------------------------------------------------------------------------------------------------------
    # run...

    afe_datum = None


    # ----------------------------------------------------------------------------------------------------------------
    # UUID...


    # ----------------------------------------------------------------------------------------------------------------
    # RTC...

    if cmd.ignore_rtc:
        reporter.report_ignore("RTC")

    else:
        try:
            test = RTCTest(cmd.verbose)

            test_ok = test.conduct()
            reporter.report_test("RTC", test_ok)

        except Exception as ex:
            reporter.report_exception("RTC", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # Board temp...

    try:
        test = BoardTempTest(cmd.verbose)

        test_ok = test.conduct()
        reporter.report_test("BoardTemp", test_ok)

    except Exception as ex:
        reporter.report_exception("BoardTemp", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # OPC...

    try:
        test = OPCTest(cmd.verbose)

        test_ok = test.conduct()
        reporter.report_test("OPC", test_ok)

    except Exception as ex:
        reporter.report_exception("OPC", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # GPS...

    if cmd.ignore_gps:
        reporter.report_ignore("GPS")

    else:
        try:
            test = GPSTest(cmd.verbose)

            test_ok = test.conduct()
            reporter.report_test("GPS", test_ok)

        except Exception as ex:
            reporter.report_exception("GPS", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # NDIR...


    # ----------------------------------------------------------------------------------------------------------------
    # Int SHT...

    try:
        sht_conf = SHTConf.load(Host)
        sht = sht_conf.int_sht()

        test = SHTTest("Int SHT", sht, cmd.verbose)

        test_ok = test.conduct()
        reporter.report_test("Int SHT", test_ok)

    except Exception as ex:
        reporter.report_exception("Int SHT", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # Ext SHT...

    try:
        sht_conf = SHTConf.load(Host)
        sht = sht_conf.ext_sht()

        test = SHTTest("Ext SHT", sht, cmd.verbose)

        test_ok = test.conduct()
        reporter.report_test("Ext SHT", test_ok)

    except Exception as ex:
        reporter.report_exception("Ext SHT", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # Pt1000...

    try:
        test = Pt1000Test(cmd.verbose)

        test_ok = test.conduct()
        reporter.report_test("Pt1000", test_ok)

    except Exception as ex:
        reporter.report_exception("Pt1000", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # AFE...

    try:
        test = AFETest(cmd.verbose)

        test_ok = test.conduct()
        reporter.report_test("AFE", test_ok)

        afe_datum = test.datum

    except Exception as ex:
        reporter.report_exception("AFE", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # EEPROM...

    if cmd.ignore_eeprom:
        reporter.report_ignore("EEPROM")

    else:
        try:
            test = EEPROMTest(cmd.verbose)

            test_ok = test.conduct()
            reporter.report_test("EEPROM", test_ok)

        except Exception as ex:
            reporter.report_exception("EEPROM", ex)


    # ----------------------------------------------------------------------------------------------------------------
    # result...

    if cmd.verbose:
        print(reporter, file=sys.stderr)
        print(reporter.result, file=sys.stderr)
        print("-", file=sys.stderr)


    # ----------------------------------------------------------------------------------------------------------------
    # report...

    recorded = LocalizedDatetime.now()
    datum = DFETestDatum(system_id.message_tag(), recorded, Host.serial_number(), cmd.dfe_serial_number,
                         reporter.subjects, afe_datum, reporter.result)

    print(JSONify.dumps(datum))
