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
import json
# external packages
import PyQt5.QtWidgets
import PyQt5.QtTest
import PyQt5.QtCore
import skyfield.api as api
import matplotlib.path
# local import
from mw4 import mainApp

test = PyQt5.QtWidgets.QApplication([])

mwGlob = {'workDir': '.',
          'configDir': './mw4/test/config/',
          'build': 'test',
          }

'''
@pytest.fixture(autouse=True, scope='function')
def module_setup_teardown():
    global spy
    global app
    app = mainApp.MountWizzard4(mwGlob=mwGlob)
    spy = PyQt5.QtTest.QSignalSpy(app.message)
    yield
    spy = None
    app = None
'''

app = mainApp.MountWizzard4(mwGlob=mwGlob)
spy = PyQt5.QtTest.QSignalSpy(app.message)


#
#
# testing mainW gui booting shutdown
#
#

def test_config_0():
    app.hemisphereW.storeConfig()


def test_initConfig_1():
    app.config['hemisphereW'] = {}
    suc = app.hemisphereW.initConfig()
    assert suc


def test_initConfig_2():
    del app.config['hemisphereW']
    suc = app.hemisphereW.initConfig()
    assert not suc


def test_initConfig_3():
    app.config['hemisphereW'] = {}
    app.config['hemisphereW']['winPosX'] = 10000
    app.config['hemisphereW']['winPosY'] = 10000
    suc = app.hemisphereW.initConfig()
    assert suc


def test_resizeEvent(qtbot):
    app.hemisphereW.resizeEvent(None)


def test_closeEvent(qtbot):
    app.hemisphereW.closeEvent(None)


def test_toggleWindow1(qtbot):
    app.hemisphereW.showStatus = True
    with mock.patch.object(app.hemisphereW,
                           'close',
                           return_value=None):
        app.hemisphereW.toggleWindow()
        assert not app.hemisphereW.showStatus


def test_toggleWindow2(qtbot):
    app.hemisphereW.showStatus = False
    with mock.patch.object(app.hemisphereW,
                           'showWindow',
                           return_value=None):
        app.hemisphereW.toggleWindow()
        assert app.hemisphereW.showStatus


def test_showWindow1(qtbot):
    app.hemisphereW.showStatus = False
    app.hemisphereW.showWindow()
    assert app.hemisphereW.showStatus


def test_clearAxes1(qtbot):
    app.hemisphereW.drawHemisphere()
    axes = app.hemisphereW.hemisphereMat.figure.axes[0]
    suc = app.hemisphereW.clearAxes(axes, True)
    assert suc


def test_clearAxes2(qtbot):
    app.hemisphereW.drawHemisphere()
    axes = app.hemisphereW.hemisphereMat.figure.axes[0]
    suc = app.hemisphereW.clearAxes(axes, False)
    assert not suc


def test_drawCanvas(qtbot):
    app.hemisphereW.drawHemisphere()
    suc = app.hemisphereW.drawCanvas()
    assert suc


def test_drawCanvasMoving(qtbot):
    app.hemisphereW.drawHemisphere()
    suc = app.hemisphereW.drawCanvasMoving()
    assert suc


def test_drawCanvasStar(qtbot):
    app.hemisphereW.drawHemisphere()
    suc = app.hemisphereW.drawCanvasStar()
    assert suc


def test_updateCelestialPath_1(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = True
    suc = app.hemisphereW.updateCelestialPath()
    assert suc


def test_updateCelestialPath_2(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = False
    suc = app.hemisphereW.updateCelestialPath()
    assert not suc


def test_updateCelestialPath_3(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = True
    app.hemisphereW.celestialPath = None
    suc = app.hemisphereW.updateCelestialPath()
    assert not suc


def test_updateMeridian_1(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = True
    app.mount.sett.meridianLimitSlew = 3
    app.mount.sett.meridianLimitTrack = 3
    suc = app.hemisphereW.updateMeridian()
    assert suc


def test_updateMeridian_2(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = False
    app.mount.sett.meridianLimitSlew = 3
    app.mount.sett.meridianLimitTrack = 3
    suc = app.hemisphereW.updateMeridian()
    assert not suc


def test_updateMeridian_3(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = True
    app.mount.sett.meridianLimitSlew = None
    app.mount.sett.meridianLimitTrack = 3
    suc = app.hemisphereW.updateMeridian()
    assert not suc


def test_updateMeridian_4(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = True
    app.mount.sett.meridianLimitSlew = 3
    app.mount.sett.meridianLimitTrack = None
    suc = app.hemisphereW.updateMeridian()
    assert not suc


def test_updatePointerAltAz_1(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = True
    app.mount.obsSite.Alt = api.Angle(degrees=5)
    app.mount.obsSite.Az = api.Angle(degrees=5)
    suc = app.hemisphereW.updatePointerAltAz()
    assert suc


def test_updatePointerAltAz_2(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = False
    suc = app.hemisphereW.updatePointerAltAz()
    assert not suc


def test_updatePointerAltAz_3(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = True
    app.mount.obsSite.Az = None
    suc = app.hemisphereW.updatePointerAltAz()
    assert not suc


def test_updatePointerAltAz_4(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = True
    app.mount.obsSite.Alt = None
    suc = app.hemisphereW.updatePointerAltAz()
    assert not suc


def test_updateDome_1(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = True
    app.mount.obsSite.Az = api.Angle(degrees=5)
    suc = app.hemisphereW.updateDome()
    assert suc


def test_updateDome_2(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = False
    app.mount.obsSite.Az = api.Angle(degrees=5)
    suc = app.hemisphereW.updateDome()
    assert not suc


def test_updateDome_3(qtbot):
    app.hemisphereW.drawHemisphere()
    app.hemisphereW.showStatus = True
    app.mount.obsSite.Az = None
    suc = app.hemisphereW.updateDome()
    assert not suc


def test_markerPoint():
    val = app.hemisphereW.markerPoint()
    assert isinstance(val, matplotlib.path.Path)


def test_markerAltAz():
    val = app.hemisphereW.markerAltAz()
    assert isinstance(val, matplotlib.path.Path)


def test_markerStar():
    val = app.hemisphereW.markerStar()
    assert isinstance(val, matplotlib.path.Path)


def test_clearHemisphere(qtbot):
    app.data.buildP = [(0, 0), (1, 0)]
    app.hemisphereW.clearHemisphere()
    assert app.data.buildP == []


def test_setOperationMode_1():
    assert app.hemisphereW.MODE is not None
    assert 'normal' in app.hemisphereW.MODE
    assert 'build' in app.hemisphereW.MODE
    assert 'horizon' in app.hemisphereW.MODE
    assert 'star' in app.hemisphereW.MODE


def test_setOperationMode_2():
    class Test:
        def set_marker(self, test):
            pass

        def set_color(self, test):
            pass

    app.hemisphereW.horizonMarker = Test()
    app.hemisphereW.pointsBuild = Test()
    suc = app.hemisphereW.setOperationMode('normal')
    assert suc


def test_setOperationMode_3():
    class Test:
        def set_marker(self, test):
            pass

        def set_color(self, test):
            pass

    app.hemisphereW.horizonMarker = Test()
    app.hemisphereW.pointsBuild = Test()
    suc = app.hemisphereW.setOperationMode('star')
    assert suc


def test_setOperationMode_4():
    class Test:
        def set_marker(self, test):
            pass

        def set_color(self, test):
            pass

    app.hemisphereW.horizonMarker = Test()
    app.hemisphereW.pointsBuild = Test()
    suc = app.hemisphereW.setOperationMode('build')
    assert suc


def test_getIndexPoint_0():
    class Test:
        pass
    event = Test()
    event.xdata = 180
    event.ydata = 45
    plane = []
    epsilon = 0
    index = app.hemisphereW.getIndexPoint(event=event,
                                          plane=plane,
                                          epsilon=epsilon,
                                          )
    assert not index


def test_getIndexPoint_1():
    event = None
    plane = None
    epsilon = 0
    index = app.hemisphereW.getIndexPoint(event=event,
                                          plane=plane,
                                          epsilon=epsilon,
                                          )
    assert not index


def test_getIndexPoint_2():
    class Test:
        pass
    event = Test()
    event.xdata = 180
    event.ydata = 45
    plane = None
    epsilon = 0
    index = app.hemisphereW.getIndexPoint(event=event,
                                          plane=plane,
                                          epsilon=epsilon,
                                          )
    assert not index


def test_getIndexPoint_3():
    class Test:
        pass
    event = Test()
    event.xdata = 180
    event.ydata = 45
    plane = [(45, 0), (45, 360)]
    epsilon = 0
    index = app.hemisphereW.getIndexPoint(event=event,
                                          plane=plane,
                                          epsilon=epsilon,
                                          )
    assert not index


def test_getIndexPoint_4():
    class Test:
        pass
    event = Test()
    event.xdata = 180
    event.ydata = 45
    plane = [(45, 0), (45, 360)]
    epsilon = 200
    index = app.hemisphereW.getIndexPoint(event=event,
                                          plane=plane,
                                          epsilon=epsilon,
                                          )
    assert index == 0


def test_getIndexPoint_5():
    class Test:
        pass
    event = Test()
    event.xdata = 182
    event.ydata = 45
    plane = [(45, 0), (45, 360)]
    epsilon = 200
    index = app.hemisphereW.getIndexPoint(event=event,
                                          plane=plane,
                                          epsilon=epsilon,
                                          )
    assert index == 1


def test_getIndexPointX_1():
    event = None
    plane = None
    index = app.hemisphereW.getIndexPointX(event=event,
                                           plane=plane,
                                           )
    assert not index


def test_getIndexPointX_2():
    class Test:
        pass
    event = Test()
    event.xdata = 182
    event.ydata = 45
    plane = None
    index = app.hemisphereW.getIndexPointX(event=event,
                                           plane=plane,
                                           )
    assert not index


def test_getIndexPointX_3():
    class Test:
        pass
    event = Test()
    event.xdata = 180
    event.ydata = 45
    plane = [(45, 0), (45, 360)]
    index = app.hemisphereW.getIndexPointX(event=event,
                                           plane=plane,
                                           )
    assert index == 0


def test_getIndexPointX_4():
    class Test:
        pass
    event = Test()
    event.xdata = 182
    event.ydata = 45
    plane = [(45, 0), (45, 360)]
    index = app.hemisphereW.getIndexPointX(event=event,
                                           plane=plane,
                                           )
    assert index == 0


def test_getIndexPointX_5():
    class Test:
        pass
    event = Test()
    event.xdata = 182
    event.ydata = 45
    plane = [(45, 0), (45, 180), (45, 360)]
    index = app.hemisphereW.getIndexPointX(event=event,
                                           plane=plane,
                                           )
    assert index == 1


def test_getIndexPointX_6():
    class Test:
        pass
    event = Test()
    event.xdata = 182
    event.ydata = 45
    plane = [(45, 0)]
    index = app.hemisphereW.getIndexPointX(event=event,
                                           plane=plane,
                                           )
    assert not index


def test_onMouseNormal_1():
    class Test:
        pass
    event = Test()
    event.inaxes = False
    suc = app.hemisphereW.onMouseNormal(event=event)
    assert not suc


def test_onMouseNormal_2():
    class Test:
        pass
    event = Test()
    event.inaxes = True
    event.button = 0
    event.dblclick = False
    suc = app.hemisphereW.onMouseNormal(event=event)
    assert not suc


def test_onMouseNormal_3():
    class Test:
        pass
    event = Test()
    event.inaxes = True
    event.button = 1
    event.dblclick = False
    suc = app.hemisphereW.onMouseNormal(event=event)
    assert not suc


def test_onMouseNormal_4():
    class Test:
        pass
    event = Test()
    event.inaxes = True
    event.button = 0
    event.dblclick = True
    suc = app.hemisphereW.onMouseNormal(event=event)
    assert not suc


def test_onMouseNormal_5():
    class Test:
        pass
    event = Test()
    event.inaxes = True
    event.button = 1
    event.dblclick = True
    event.xdata = 180
    event.ydata = 45
    with mock.patch.object(PyQt5.QtWidgets.QMessageBox,
                           'question',
                           return_value=PyQt5.QtWidgets.QMessageBox.No):
        suc = app.hemisphereW.onMouseNormal(event=event)
        assert not suc


def test_onMouseNormal_6():
    class Test:
        pass
    event = Test()
    event.inaxes = True
    event.button = 1
    event.dblclick = True
    event.xdata = 180
    event.ydata = 45
    with mock.patch.object(PyQt5.QtWidgets.QMessageBox,
                           'question',
                           return_value=PyQt5.QtWidgets.QMessageBox.Yes):
        suc = app.hemisphereW.onMouseNormal(event=event)
        assert suc


def test_addHorizonPoint_1():
    class Test:
        pass
    event = Test()
    event.xdata = 180
    event.ydata = 45
    app.data.horizonP = [(0, 0), (10, 10), (0, 360)]
    suc = app.hemisphereW.addHorizonPoint(data=app.data, event=event)
    assert suc


def test_addHorizonPoint_2():
    class Test:
        pass
    event = Test()
    event.xdata = 180
    event.ydata = 45
    app.data.horizonP = [(0, 0)]
    suc = app.hemisphereW.addHorizonPoint(data=app.data, event=event)
    assert suc


def test_addHorizonPoint_3():
    class Test:
        pass
    event = Test()
    event.xdata = 180
    event.ydata = 45
    suc = app.hemisphereW.addHorizonPoint(data=app.data, event=event)
    assert suc


def test_deleteHorizonPoint_1():
    class Test:
        pass
    event = Test()
    event.xdata = 10
    event.ydata = 10
    app.data.horizonP = [(0, 0), (10, 10), (0, 360)]
    suc = app.hemisphereW.deleteHorizonPoint(data=app.data, event=event)
    assert suc


def test_deleteHorizonPoint_2():
    class Test:
        pass
    event = Test()
    event.xdata = 180
    event.ydata = 45
    app.data.horizonP = [(0, 0), (10, 10), (0, 360)]
    suc = app.hemisphereW.deleteHorizonPoint(data=app.data, event=event)
    assert not suc


def test_deleteHorizonPoint_3():
    class Test:
        pass
    event = Test()
    event.xdata = 180
    event.ydata = 45
    app.data.horizonP = [(0, 0)]
    suc = app.hemisphereW.deleteHorizonPoint(data=app.data, event=event)
    assert not suc


def test_editHorizonMask_1():
    class Test:
        def set_data(self, test, test1):
            pass

        def set_xy(self, test):
            pass

    event = Test()
    event.xdata = 180
    event.ydata = 45
    event.button = 1
    app.hemisphereW.horizonMarker = Test()
    app.hemisphereW.horizonFill = Test()
    suc = app.hemisphereW.editHorizonMask(data=app.data, event=event)
    assert suc


def test_editHorizonMask_2():
    class Test:
        def set_data(self, test, test1):
            pass

        def set_xy(self, test):
            pass

    event = Test()
    event.xdata = 180
    event.ydata = 45
    event.button = 3
    app.hemisphereW.horizonMarker = Test()
    app.hemisphereW.horizonFill = Test()
    suc = app.hemisphereW.editHorizonMask(data=app.data, event=event)
    assert suc


def test_editHorizonMask_3():
    class Test:
        def set_data(self, test, test1):
            pass

        def set_xy(self, test):
            pass

    event = Test()
    event.xdata = 180
    event.ydata = 45
    event.button = 2
    app.hemisphereW.horizonMarker = Test()
    app.hemisphereW.horizonFill = Test()
    suc = app.hemisphereW.editHorizonMask(data=app.data, event=event)
    assert not suc


def test_deleteBuildPointPoint_1():
    axes = app.hemisphereW.hemisphereMat.figure.axes[0]
    app.hemisphereW.pointsBuildAnnotate.append(axes.annotate('', xy=(0, 0)))
    app.hemisphereW.pointsBuildAnnotate.append(axes.annotate('', xy=(0, 0)))
    app.hemisphereW.pointsBuildAnnotate.append(axes.annotate('', xy=(0, 0)))

    class Test:
        pass
    event = Test()
    event.xdata = 10
    event.ydata = 10
    app.data.buildP = [(0, 0), (10, 10), (0, 360)]
    suc = app.hemisphereW.deleteBuildPoint(data=app.data, event=event)
    assert suc


def test_deleteBuildPointPoint_2():
    class Test:
        pass
    event = Test()
    event.xdata = 180
    event.ydata = 45
    app.data.buildP = [(0, 0), (10, 10), (0, 360)]
    suc = app.hemisphereW.deleteBuildPoint(data=app.data, event=event)
    assert not suc


def test_editBuildPoints_1():
    axes = app.hemisphereW.hemisphereMat.figure.axes[0]
    app.hemisphereW.pointsBuildAnnotate.append(axes.annotate('', xy=(0, 0)))
    app.hemisphereW.pointsBuildAnnotate.append(axes.annotate('', xy=(0, 0)))
    app.hemisphereW.pointsBuildAnnotate.append(axes.annotate('', xy=(0, 0)))

    class Test:
        def set_data(self, test, test1):
            pass

        def set_xy(self, test):
            pass

    event = Test()
    event.xdata = 180
    event.ydata = 45
    event.button = 1
    app.hemisphereW.pointsBuild = Test()
    suc = app.hemisphereW.editBuildPoints(data=app.data, event=event, axes=axes)
    assert suc


def test_editBuildPoints_2():
    axes = app.hemisphereW.hemisphereMat.figure.axes[0]
    app.hemisphereW.pointsBuildAnnotate.append(axes.annotate('', xy=(0, 0)))
    app.hemisphereW.pointsBuildAnnotate.append(axes.annotate('', xy=(0, 0)))
    app.hemisphereW.pointsBuildAnnotate.append(axes.annotate('', xy=(0, 0)))

    class Test:
        def set_data(self, test, test1):
            pass

        def set_xy(self, test):
            pass

    event = Test()
    event.xdata = 180
    event.ydata = 45
    event.button = 3
    app.hemisphereW.pointsBuild = Test()
    suc = app.hemisphereW.editBuildPoints(data=app.data, event=event, axes=axes)
    assert suc


def test_editBuildPoints_3():
    axes = app.hemisphereW.hemisphereMat.figure.axes[0]
    app.hemisphereW.pointsBuildAnnotate.append(axes.annotate('', xy=(0, 0)))
    app.hemisphereW.pointsBuildAnnotate.append(axes.annotate('', xy=(0, 0)))
    app.hemisphereW.pointsBuildAnnotate.append(axes.annotate('', xy=(0, 0)))

    class Test:
        def set_data(self, test, test1):
            pass

        def set_xy(self, test):
            pass

    event = Test()
    event.xdata = 180
    event.ydata = 45
    event.button = 2
    app.hemisphereW.pointsBuild = Test()
    suc = app.hemisphereW.editBuildPoints(data=app.data, event=event, axes=axes)
    assert not suc


def test_onMouseEdit_1():
    class Test:
        pass
    event = Test()
    event.inaxes = False
    suc = app.hemisphereW.onMouseEdit(event=event)
    assert not suc


def test_onMouseEdit_2():
    class Test:
        pass
    event = Test()
    event.inaxes = True
    suc = app.hemisphereW.onMouseEdit(event=event)
    assert not suc


def test_onMouseEdit_3():
    class Test:
        pass
    event = Test()
    event.inaxes = True
    app.hemisphereW.ui.checkEditHorizonMask.setChecked(False)
    app.hemisphereW.ui.checkEditBuildPoints.setChecked(False)
    with mock.patch.object(app.hemisphereW,
                           'editHorizonMask',
                           return_value=True):
        with mock.patch.object(app.hemisphereW,
                               'editBuildPoints',
                               return_value=True):
            suc = app.hemisphereW.onMouseEdit(event=event)
            assert not suc


def test_onMouseEdit_4():
    class Test:
        pass
    event = Test()
    event.inaxes = True
    app.hemisphereW.ui.checkEditHorizonMask.setChecked(True)
    app.hemisphereW.ui.checkEditBuildPoints.setChecked(False)
    with mock.patch.object(app.hemisphereW,
                           'editHorizonMask',
                           return_value=True):
        with mock.patch.object(app.hemisphereW,
                               'editBuildPoints',
                               return_value=True):
            suc = app.hemisphereW.onMouseEdit(event=event)
            assert suc


def test_onMouseEdit_5():
    class Test:
        pass
    event = Test()
    event.inaxes = True
    app.hemisphereW.ui.checkEditHorizonMask.setChecked(False)
    app.hemisphereW.ui.checkEditBuildPoints.setChecked(True)
    with mock.patch.object(app.hemisphereW,
                           'editHorizonMask',
                           return_value=True):
        with mock.patch.object(app.hemisphereW,
                               'editBuildPoints',
                               return_value=True):
            suc = app.hemisphereW.onMouseEdit(event=event)
            assert suc


def test_onMouseEdit_6():
    class Test:
        pass
    event = Test()
    event.inaxes = True
    app.hemisphereW.ui.checkEditHorizonMask.setChecked(True)
    app.hemisphereW.ui.checkEditBuildPoints.setChecked(False)
    with mock.patch.object(app.hemisphereW,
                           'editHorizonMask',
                           return_value=False):
        with mock.patch.object(app.hemisphereW,
                               'editBuildPoints',
                               return_value=True):
            suc = app.hemisphereW.onMouseEdit(event=event)
            assert not suc


def test_onMouseEdit_7():
    class Test:
        pass
    event = Test()
    event.inaxes = True
    app.hemisphereW.ui.checkEditHorizonMask.setChecked(False)
    app.hemisphereW.ui.checkEditBuildPoints.setChecked(True)
    with mock.patch.object(app.hemisphereW,
                           'editHorizonMask',
                           return_value=True):
        with mock.patch.object(app.hemisphereW,
                               'editBuildPoints',
                               return_value=False):
            suc = app.hemisphereW.onMouseEdit(event=event)
            assert not suc


def test_onMouseStar_1():
    class Test:
        pass
    event = Test()
    event.inaxes = False
    suc = app.hemisphereW.onMouseStar(event=event)
    assert not suc


def test_onMouseStar_2():
    class Test:
        pass
    event = Test()
    event.inaxes = True
    suc = app.hemisphereW.onMouseStar(event=event)
    assert suc


def test_drawHemisphere_1():
    app.mainW.genBuildMin()
    app.hemisphereW.drawHemisphere()
