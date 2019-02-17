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
# Python  v3.6.7
#
# Michael Würtenberger
# (c) 2018
#
# Licence APL2.0
#
###########################################################
# standard libraries
import unittest.mock as mock
import pytest
# external packages
import PyQt5.QtWidgets
import PyQt5.QtTest
import PyQt5.QtCore
# local import
from mw4 import mainApp
from mw4.test.test_setupQt import setupQt
app, spy, mwGlob, test = setupQt()


def test_storeConfig_1():
    app.imageW.storeConfig()


def test_initConfig_1():
    app.config['imageW'] = {}
    suc = app.imageW.initConfig()
    assert suc


def test_initConfig_2():
    del app.config['imageW']
    suc = app.imageW.initConfig()
    assert not suc


def test_initConfig_3():
    app.config['imageW'] = {}
    app.config['imageW']['winPosX'] = 10000
    app.config['imageW']['winPosY'] = 10000
    suc = app.imageW.initConfig()
    assert suc


def test_resizeEvent(qtbot):
    app.imageW.resizeEvent(None)


def test_closeEvent(qtbot):
    app.imageW.closeEvent(None)


def test_showWindow_1(qtbot):
    app.imageW.showStatus = False
    app.mainW.ui.checkMeasurement.setChecked(True)
    with mock.patch.object(app.imageW,
                           'show',
                           return_value=None):
        suc = app.imageW.showWindow()
        assert suc
        assert app.imageW.showStatus


def test_showWindow_2(qtbot):
    app.imageW.showStatus = False
    app.mainW.ui.checkMeasurement.setChecked(False)
    with mock.patch.object(app.imageW,
                           'show',
                           return_value=None):
        suc = app.imageW.showWindow()
        assert not suc
        assert not app.imageW.showStatus
