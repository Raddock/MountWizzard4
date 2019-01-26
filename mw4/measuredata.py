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
import logging
# external packages
import PyQt5
import numpy as np
# local imports


class MeasureData(PyQt5.QtCore.QObject):
    """
    the class MeasureData inherits all information and handling of data management and
    storage

        >>> mData = MeasureData(
        >>>                 )
    """

    __all__ = ['MeasureData',
               ]

    version = '0.1'
    logger = logging.getLogger(__name__)

    # update rate to 1 seconds for setting indi server
    CYCLE_UPDATE_TASK = 1000

    def __init__(self,
                 app,
                 ):
        super().__init__()
        self.app = app
        self.raRef = None
        self.decRef = None
        self.mData = {
            'time': np.empty(shape=[0, 1], dtype='datetime64'),
            'temp': np.empty(shape=[0, 1]),
            'hum': np.empty(shape=[0, 1]),
            'press': np.empty(shape=[0, 1]),
            'dew': np.empty(shape=[0, 1]),
            'sqr': np.empty(shape=[0, 1]),
            'raJNow': np.empty(shape=[0, 1]),
            'decJNow': np.empty(shape=[0, 1]),
        }

        self.timerTask = PyQt5.QtCore.QTimer()
        self.timerTask.setSingleShot(False)
        self.timerTask.timeout.connect(self.measureTask)
        self.timerTask.start(self.CYCLE_UPDATE_TASK)

    def measureTask(self):
        """

        :return: success
        """

        obs = self.app.mount.obsSite
        envTemp = self.app.environment.wDevice['local']['data'].get('WEATHER_TEMPERATURE', -99)
        envPress = self.app.environment.wDevice['local']['data'].get('WEATHER_BAROMETER', 0)
        envPress = round(envPress, 1)
        envDew = self.app.environment.wDevice['local']['data'].get('WEATHER_DEWPOINT', 0)
        envHum = self.app.environment.wDevice['local']['data'].get('WEATHER_HUMIDITY', 0)
        envSQR = self.app.environment.wDevice['sqm']['data'].get('SKY_BRIGHTNESS', 0)
        envSQR = round(envSQR, 2)
        if envTemp == -99:
            return False
        dat = self.mData
        dat['time'] = np.append(dat['time'], np.datetime64(obs.timeJD.utc_datetime()))
        dat['temp'] = np.append(dat['temp'], envTemp)
        dat['hum'] = np.append(dat['hum'], envHum)
        dat['press'] = np.append(dat['press'], envPress)
        dat['dew'] = np.append(dat['dew'], envDew)
        dat['sqr'] = np.append(dat['sqr'], envSQR)
        if obs.raJNow is not None:
            if obs.status == 0:
                if self.raRef is None:
                    self.raRef = obs.raJNow.hours * 3600
                if self.decRef is None:
                    self.decRef = obs.decJNow.degrees * 3600
                dat['raJNow'] = np.append(dat['raJNow'], obs.raJNow.hours * 3600 - self.raRef)
                dat['decJNow'] = np.append(dat['decJNow'], obs.decJNow.degrees * 3600 - self.decRef)
            else:
                self.raRef = None
                self.decRef = None
                dat['raJNow'] = np.append(dat['raJNow'], 0)
                dat['decJNow'] = np.append(dat['decJNow'], 0)
        else:
            dat['raJNow'] = np.append(dat['raJNow'], 0)
            dat['decJNow'] = np.append(dat['decJNow'], 0)
        return True
