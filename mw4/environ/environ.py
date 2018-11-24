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
# Python  v3.6.5
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
from indibase import indiBase
# local imports


class Environment(PyQt5.QtWidgets.QWidget):
    """
    the class Environ inherits all information and handling of environment devices

        >>> fw = Environment(
        >>>                  host=host
        >>>                  localWeatherName='MBox'
        >>>                  sqmName='SQM'
        >>>                  globalWeatherName='OpenWeather'
        >>>                 )
    """

    __all__ = ['Environment',
               ]

    version = '0.1'
    logger = logging.getLogger(__name__)

    def __init__(self,
                 host=None,
                 localWeatherName='',
                 sqmName='',
                 globalWeatherName='',
                 ):
        super().__init__()

        self.client = indiBase.Client(host=host)

        self.localWeatherName = localWeatherName
        self.sqmName = sqmName
        self.globalWeatherName = globalWeatherName

        self.localWeatherDevice = None
        self.sqmDevice = None
        self.globalWeatherDevice = None

        # link signals
        self.client.signals.newEnvironDevice.connect(self.newDevice)
        self.client.signals.removeDevice.connect(self.removeDevice)
        self.client.signals.newProperty.connect(self.connectDevice)
        self.client.signals.newNumber.connect(self.updateData)


    @property
    def localWeatherName(self):
        return self._localWeatherName

    @localWeatherName.setter
    def localWeatherName(self, value):
        self._localWeatherName = value

    @property
    def sqmName(self):
        return self._sqmName

    @sqmName.setter
    def sqmName(self, value):
        self._sqmName = value

    @property
    def globalWeatherName(self):
        return self._globalWeatherName

    @globalWeatherName.setter
    def globalWeatherName(self, value):
        self._globalWeatherName = value

    def newDevice(self, deviceName):
        """

        :param deviceName:
        :return:
        """

        if not self.client.isServerConnected():
            return False
        if deviceName == self.localWeatherName:
            self.localWeatherDevice = self.client.getDevice(deviceName)
        elif deviceName == self.sqmName:
            self.sqmDevice = self.client.getDevice(self.sqmName)
        elif deviceName == self.globalWeatherName:
            self.globalWeatherDevice = self.client.getDevice(deviceName)

    def removeDevice(self, deviceName):
        """

        :param deviceName:
        :return:
        """

        if not self.client.isServerConnected():
            return False
        if deviceName == self.localWeatherName:
            self.localWeatherDevice = None
        elif deviceName == self.sqmName:
            self.sqmDevice = None
        elif deviceName == self.globalWeatherName:
            self.globalWeatherDevice = None

    def startCommunication(self):
        suc = self.client.connectServer()
        if self.localWeatherName:
            self.client.watchDevice(self.localWeatherName)
        if self.globalWeatherName:
            self.client.watchDevice(self.globalWeatherName)
        if self.sqmName:
            self.client.watchDevice(self.sqmName)
        return suc

    def reconnectIndiServer(self):
        if self.client.isServerConnected():
            self.client.disconnectServer()
        suc = self.startCommunication()
        return suc

    def connectDevice(self, deviceName, propertyName):
        if propertyName != 'CONNECTION':
            return
        deviceList = [self.localWeatherName,
                      self.globalWeatherName,
                      self.sqmName
                      ]
        if deviceName in deviceList:
            self.client.connectDevice(deviceName=deviceName)

    def getStatus(self):
        deviceNameList = {'local': self.localWeatherName,
                          'global': self.globalWeatherName,
                          'sqm': self.sqmName,
                          }

        for deviceKey, deviceName in deviceNameList.items():
            if deviceName not in self.client.devices:
                yield deviceKey, 0
                continue
            device = self.client.getDevice(deviceName)
            status = device.getSwitch('CONNECTION')['CONNECT']
            if status:
                yield deviceKey, 1
            else:
                yield deviceKey, 3

    def updateData(self, deviceName, propertyName):
        print(deviceName, propertyName)
