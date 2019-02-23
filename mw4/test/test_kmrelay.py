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
from unittest import mock
import time
# external packages
import PyQt5.QtWidgets
# local import
from mw4.relay import kmRelay
from mw4.test.test_setupQt import setupQt

app, spy, mwGlob, test = setupQt()


host_ip = '192.168.2.14'
host = (host_ip, 80)


def test_host_1():
    app.relay.host = 0.0
    assert app.relay.host is None


def test_host_2():
    app.relay.host = host
    assert app.relay.host == host


def test_user():
    app.relay.user = 'astro'
    assert app.relay.user == 'astro'


def test_password():
    app.relay.password = 'astro'
    assert app.relay.password == 'astro'


def test_timers():
    app.relay.startTimers()
    app.relay.stopTimers()


def test_status1(qtbot):
    returnValue = """<response>
                     <relay0>0</relay0>
                     <relay1>0</relay1>
                     <relay2>0</relay2>
                     <relay3>0</relay3>
                     <relay4>0</relay4>
                     <relay5>0</relay5>
                     <relay6>0</relay6>
                     <relay7>0</relay7>
                     <relay8>0</relay8>
                     </response>"""

    class Test:
        pass
    ret = Test()
    ret.text = returnValue
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):

        for i in range(0, 9):
            app.relay.set(i, 0)

        with qtbot.waitSignal(app.relay.statusReady):
            app.relay.cyclePolling()
        assert [0, 0, 0, 0, 0, 0, 0, 0] == app.relay.status


def test_status2(qtbot):
    returnValue = """<response>
                     <relay0>1</relay0>
                     <relay1>1</relay1>
                     <relay2>1</relay2>
                     <relay3>1</relay3>
                     <relay4>1</relay4>
                     <relay5>1</relay5>
                     <relay6>1</relay6>
                     <relay7>1</relay7>
                     <relay8>1</relay8>
                     </response>"""

    class Test:
        pass
    ret = Test()
    ret.text = returnValue
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):

        for i in range(0, 9):
            app.relay.set(i, 1)

        with qtbot.waitSignal(app.relay.statusReady):
            app.relay.cyclePolling()
        assert [1, 1, 1, 1, 1, 1, 1, 1] == app.relay.status


def test_status3(qtbot):
    returnValue = """<response>
                     <relay0>1</relay0>
                     <relay1>1</relay1>
                     <relay2>1</relay2>
                     <relay3>1</relay3>
                     <relay4>1</relay4>
                     <relay5>1</relay5>
                     <relay6>1</relay6>
                     <relay7>1</relay7>
                     <relay8>1</relay8>
                     </response>"""

    class Test:
        pass
    ret = Test()
    ret.text = returnValue
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):

        for i in range(0, 9):
            app.relay.switch(i)

        with qtbot.waitSignal(app.relay.statusReady):
            app.relay.cyclePolling()
        assert [1, 1, 1, 1, 1, 1, 1, 1] == app.relay.status


def test_status4(qtbot):
    returnValue = """<response>
                     <relay0>0</relay0>
                     <relay1>0</relay1>
                     <relay2>0</relay2>
                     <relay3>0</relay3>
                     <relay4>0</relay4>
                     <relay5>0</relay5>
                     <relay6>0</relay6>
                     <relay7>0</relay7>
                     <relay8>0</relay8>
                     </response>"""

    class Test:
        pass
    ret = Test()
    ret.text = returnValue
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):
        with mock.patch.object(time,
                               'sleep'):
            for i in range(0, 9):
                app.relay.pulse(i)

            with qtbot.waitSignal(app.relay.statusReady):
                app.relay.cyclePolling()
            assert [0, 0, 0, 0, 0, 0, 0, 0] == app.relay.status


def test_getRelay_1(qtbot):
    app.relay.mutexPoll.lock()
    suc = app.relay.getRelay()
    app.relay.mutexPoll.unlock()
    assert not suc


def test_cyclePolling_1():
    class Test:
        pass
    ret = Test()
    ret.reason = 'False'
    ret.status_code = 200

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):
        suc = app.relay.cyclePolling()
        assert not suc


def test_pulse_1(qtbot):
    ret = None

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):
        suc = app.relay.pulse(7)
        assert not suc


def test_pulse_2(qtbot):
    class Test:
        pass
    ret = Test()
    ret.reason = 'False'
    ret.status_code = 200

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):
        suc = app.relay.pulse(7)
        assert not suc


def test_pulse_3(qtbot):
    class Test:
        pass
    ret = Test()
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):
        suc = app.relay.pulse(7)
        assert suc


def test_switch_1(qtbot):
    ret = None

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):
        suc = app.relay.switch(7)
        assert not suc


def test_switch_2(qtbot):
    class Test:
        pass
    ret = Test()
    ret.reason = 'False'
    ret.status_code = 200

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):
        suc = app.relay.switch(7)
        assert not suc


def test_switch_3(qtbot):
    class Test:
        pass
    ret = Test()
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):
        suc = app.relay.switch(7)
        assert suc


def test_set_1(qtbot):
    ret = None

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):
        suc = app.relay.set(7, True)
        assert not suc


def test_set_2(qtbot):
    class Test:
        pass
    ret = Test()
    ret.reason = 'False'
    ret.status_code = 200

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):
        suc = app.relay.set(7, True)
        assert not suc


def test_set_3(qtbot):
    class Test:
        pass
    ret = Test()
    ret.reason = 'OK'
    ret.status_code = 200

    with mock.patch.object(app.relay,
                           'getRelay',
                           return_value=ret):
        suc = app.relay.set(7, False)
        assert suc
