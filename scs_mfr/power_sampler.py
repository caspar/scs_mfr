#!/usr/bin/env python3

"""
Created on 2 Oct 2016

@author: Bruno Beloff (bruno.beloff@southcoastscience.com)

Requires SystemID document.

command line example:
./power_sampler.py -i 2 -n 10
"""

import sys

from scs_core.data.json import JSONify
from scs_core.data.localized_datetime import LocalizedDatetime

from scs_core.sample.sample_datum import SampleDatum

from scs_core.sync.timed_runner import TimedRunner

from scs_core.sys.system_id import SystemID
from scs_core.sys.exception_report import ExceptionReport

from scs_host.sync.schedule_runner import ScheduleRunner
from scs_host.sys.host import Host

from scs_mfr.cmd.cmd_sampler import CmdSampler
from scs_mfr.sampler.power_sampler import PowerSampler


# --------------------------------------------------------------------------------------------------------------------

if __name__ == '__main__':

    cmd = None
    sampler = None

    try:
        # ------------------------------------------------------------------------------------------------------------
        # cmd...

        cmd = CmdSampler()

        if cmd.verbose:
            print(cmd, file=sys.stderr)


        # ------------------------------------------------------------------------------------------------------------
        # resources...

        # SystemID...
        system_id = SystemID.load_from_host(Host)

        if system_id is None:
            print("SystemID not available.", file=sys.stderr)
            exit()

        if cmd.verbose:
            print(system_id, file=sys.stderr)

        # runner...
        runner = TimedRunner(cmd.interval, cmd.samples) if cmd.semaphore is None \
            else ScheduleRunner(cmd.semaphore, False)

        # sampler...
        sampler = PowerSampler(runner)

        if cmd.verbose:
            print(sampler, file=sys.stderr)
            sys.stderr.flush()


        # ------------------------------------------------------------------------------------------------------------
        # run...

        for power_datum in sampler.samples():
            recorded = LocalizedDatetime.now()
            datum = SampleDatum(system_id.message_tag(), recorded, power_datum)

            print(JSONify.dumps(datum))
            sys.stdout.flush()


    # ----------------------------------------------------------------------------------------------------------------
    # end...

    except KeyboardInterrupt as ex:
        if cmd.verbose:
            print("power_sampler: KeyboardInterrupt", file=sys.stderr)

    except Exception as ex:
        print(JSONify.dumps(ExceptionReport.construct(ex)), file=sys.stderr)

    finally:
        if sampler:
            sampler.close()
