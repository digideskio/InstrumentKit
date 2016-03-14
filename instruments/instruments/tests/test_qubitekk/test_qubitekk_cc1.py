#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Module containing tests for the Qubitekk CC1
"""

# IMPORTS ####################################################################

from __future__ import absolute_import

from nose.tools import raises
import quantities as pq

import instruments as ik
from instruments.tests import expected_protocol, unit_eq

# TESTS ######################################################################


def test_cc1_count():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "COUN:C1?"
        ],
        [
            "v2.10",
            "20"
        ],
        sep="\n"
    ) as cc:
        assert cc.channel[0].count == 20.0


def test_cc1_window():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "WIND?",
            ":WIND 7"
        ],
        [
            "v2.10",
            "2",
            ""
        ],
        sep="\n"
    ) as cc:
        unit_eq(cc.window, pq.Quantity(2, "ns"))
        cc.window = 7


@raises(ValueError)
def test_cc1_window_error():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            ":WIND 10"
        ],
        [
            "v2.10"
        ],
        sep="\n"
    ) as cc:
        cc.window = 10


def test_cc1_delay():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "DELA?",
            ":DELA 2"
        ],
        [
            "v2.10",
            "8",
            ""
        ],
        sep="\n"
    ) as cc:
        unit_eq(cc.delay, pq.Quantity(8, "ns"))
        cc.delay = 2


@raises(ValueError)
def test_cc1_delay_error1():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            ":DELA -1"
        ],
        [
            "v2.10"
        ],
        sep="\n"
    ) as cc:
        cc.delay = -1


@raises(ValueError)
def test_cc1_delay_error2():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            ":DELA 1"
        ],
        [
            "v2.10"
        ],
        sep="\n"
    ) as cc:
        cc.delay = 1


def test_cc1_dwell():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "DWEL?",
            ":DWEL 2"
        ],
        [
            "v2.01",
            "8",
            ""
        ],
        sep="\n"
    ) as cc:
        unit_eq(cc.dwell_time, pq.Quantity(8, "s"))
        cc.dwell_time = 2


@raises(ValueError)
def test_cc1_dwell_time_error():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            ":DWEL -1"
        ],
        [
            "v2.10"
        ],
        sep="\n"
    ) as cc:
        cc.dwell_time = -1


def test_cc1_firmware():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?"
        ],
        [
            "1.2.3"
        ],
        sep="\n"
    ) as cc:
        assert cc.firmware == (1, 2, 3)


def test_cc1_firmware_2():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?"
        ],
        [
            "v1"
        ],
        sep="\n"
    ) as cc:
        assert cc.firmware == (1, 0, 0)


def test_cc1_gate_new_firmware():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "GATE?",
            ":GATE:ON",
            ":GATE:OFF"

        ],
        [
            "v2.10",
            "ON",
            "",
            ""
        ],
        sep="\n"
    ) as cc:
        assert cc.gate is True
        cc.gate = True
        cc.gate = False


def test_cc1_gate_old_firmware():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "GATE?",
            ":GATE 1",
            ":GATE 0"

        ],
        [
            "v2.001",
            "1",
            "",
            ""
        ],
        sep="\n"
    ) as cc:
        assert cc.gate is True
        cc.gate = True
        cc.gate = False


@raises(TypeError)
def test_cc1_gate_error():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            ":GATE blo"
        ],
        [
            "v2.10"
        ],
        sep="\n"
    ) as cc:
        cc.gate = "blo"


def test_cc1_subtract_new_firmware():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "SUBT?",
            ":SUBT:ON",
            ":SUBT:OFF"

        ],
        [
            "v2.010",
            "ON",
            "",
            ""
        ],
        sep="\n"
    ) as cc:
        assert cc.subtract is True
        cc.subtract = True
        cc.subtract = False


@raises(TypeError)
def test_cc1_subtract_error():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            ":SUBT blo"

        ],
        [
            "v2.10"
        ],
        sep="\n"
    ) as cc:
        cc.subtract = "blo"


def test_cc1_trigger():  # pylint: disable=redefined-variable-type
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "TRIG?",
            ":TRIG:MODE CONT",
            ":TRIG:MODE STOP"
        ],
        [
            "v2.10",
            "MODE STOP",
            "",
            ""
        ],
        sep="\n"
    ) as cc:
        assert cc.trigger == cc.TriggerMode.start_stop
        cc.trigger = cc.TriggerMode.continuous
        cc.trigger = cc.TriggerMode.start_stop


def test_cc1_trigger_old_firmware():  # pylint: disable=redefined-variable-type
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "TRIG?",
            ":TRIG 0",
            ":TRIG 1"
        ],
        [
            "v2.001",
            "1",
            "",
            ""
        ],
        sep="\n"
    ) as cc:
        assert cc.trigger == cc.TriggerMode.start_stop
        cc.trigger = cc.TriggerMode.continuous
        cc.trigger = cc.TriggerMode.start_stop


@raises(ValueError)
def test_cc1_trigger_error():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?"
        ],
        [
            "v2.10"
        ],
        sep="\n"
    ) as cc:
        cc.trigger = "blo"


def test_cc1_clear():
    with expected_protocol(
        ik.qubitekk.CC1,
        [
            "FIRM?",
            "CLEA"
        ],
        [
            "v2.10"
        ],
        sep="\n"
    ) as cc:
        cc.clear_counts()
