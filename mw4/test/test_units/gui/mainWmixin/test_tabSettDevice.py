############################################################
# -*- coding: utf-8 -*-
#
#       #   #  #   #   #    #
#      ##  ##  #  ##  #    #
#     # # # #  # # # #    #  #
#    #  ##  #  ##  ##    ######
#   #   #   #  #   #       #
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.7.5
#
# Michael Würtenberger
# (c) 2019
#
# Licence APL2.0
#
###########################################################
# standard libraries
import unittest.mock as mock
import pytest
# external packages
# local import
from mw4.test.test_units.setupQt import setupQt


@pytest.fixture(autouse=True, scope='module')
def module_setup_teardown():
    global app, spy, mwGlob, test
    app, spy, mwGlob, test = setupQt()
    yield


def test_initConfig_1():
    app.config['mainW'] = {}
    suc = app.mainW.initConfig()
    assert suc


def test_initConfig_2():
    del app.config['mainW']
    suc = app.mainW.initConfig()
    assert suc


def test_storeConfig_1():
    suc = app.storeConfig()
    assert suc


def test_setupIcons():
    suc = app.mainW.setupIcons()
    assert suc


def test_setupDeviceGui_1():
    suc = app.mainW.setupDeviceGui()
    assert suc


def test_enableRelay_1(qtbot):
    app.mainW.ui.relayDevice.setCurrentIndex(0)
    with mock.patch.object(app.relay,
                           'stopTimers',
                           return_value=None):
        with qtbot.waitSignal(app.message) as blocker:
            suc = app.mainW.relayDispatch()
            assert suc
        assert ['Relay disabled', 0] == blocker.args


def test_enableRelay_2(qtbot):
    app.mainW.ui.relayDevice.setCurrentIndex(1)
    with mock.patch.object(app.relay,
                           'startTimers',
                           return_value=None):
        with qtbot.waitSignal(app.message) as blocker:
            suc = app.mainW.relayDispatch()
            assert suc
        assert ['Relay enabled', 0] == blocker.args


def test_enableRemote_1(qtbot):
    app.mainW.ui.remoteDevice.setCurrentIndex(0)
    with mock.patch.object(app.remote,
                           'startRemote',
                           return_value=None):
        with qtbot.waitSignal(app.message) as blocker:
            suc = app.mainW.remoteDispatch()
            assert suc
        assert ['Remote disabled', 0] == blocker.args


def test_enableRemote_2(qtbot):
    app.mainW.ui.remoteDevice.setCurrentIndex(1)
    with mock.patch.object(app.remote,
                           'stopRemote',
                           return_value=None):
        with qtbot.waitSignal(app.message) as blocker:
            suc = app.mainW.remoteDispatch()
            assert suc
        assert ['Remote enabled', 0] == blocker.args


def test_enableMeasure_1(qtbot):
    app.mainW.ui.measureDevice.setCurrentIndex(1)
    with mock.patch.object(app.measure,
                           'startMeasurement',
                           return_value=None):
        with qtbot.waitSignal(app.message) as blocker:
            suc = app.mainW.measureDispatch()
            assert suc
        assert ['Measurement enabled', 0] == blocker.args


def test_enableMeasure_2(qtbot):
    app.mainW.ui.measureDevice.setCurrentIndex(0)
    with mock.patch.object(app.measure,
                           'stopMeasurement',
                           return_value=None):
        with qtbot.waitSignal(app.message) as blocker:
            suc = app.mainW.measureDispatch()
            assert suc
        assert ['Measurement disabled', 0] == blocker.args


def test_sensorWeatherDispatch_1():
    app.mainW.ui.sensorWeatherDevice.setCurrentIndex(0)
    suc = app.mainW.sensorWeatherDispatch()
    assert suc


def test_sensorWeatherDispatch_2():
    app.mainW.ui.sensorWeatherDevice.setCurrentIndex(1)
    suc = app.mainW.sensorWeatherDispatch()
    assert suc


def test_skymeterDispatch_1():
    app.mainW.ui.skymeterDevice.setCurrentIndex(0)
    suc = app.mainW.skymeterDispatch()
    assert suc


def test_skymeterDispatch_2():
    app.mainW.ui.skymeterDevice.setCurrentIndex(1)
    suc = app.mainW.skymeterDispatch()
    assert suc


def test_powerDispatch_1():
    app.mainW.ui.powerDevice.setCurrentIndex(0)
    suc = app.mainW.powerDispatch()
    assert suc


def test_powerDispatch_2():
    app.mainW.ui.powerDevice.setCurrentIndex(1)
    suc = app.mainW.powerDispatch()
    assert suc


def test_astrometryDispatch_1():
    app.mainW.ui.astrometryDevice.setCurrentIndex(0)
    suc = app.mainW.astrometryDispatch()
    assert suc


def test_astrometryDispatch_2():
    app.mainW.ui.astrometryDevice.setCurrentIndex(1)
    suc = app.mainW.astrometryDispatch()
    assert suc
