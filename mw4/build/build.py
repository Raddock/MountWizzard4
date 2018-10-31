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
import numpy as np
# local imports


class DataPoint(object):
    """
    The class Data inherits all information and handling of build data and other
    attributes. this includes horizon data, model points data and their persistence

        >>> fw = DataPoint(
        >>>           lat=48
        >>>              )
    """

    __all__ = ['DataPoint',
               ]
    version = '0.1'
    logger = logging.getLogger(__name__)

    # data for generating greater circles, dec and step only for east, west is reversed
    DEC = {'min': [-15, 0, 15, 30, 45, 60, 75],
           'norm': [-15, 0, 15, 30, 45, 60, 75],
           'med': [-15, -5, 5, 15, 25, 40, 55, 70, 85],
           'max': [-15, -5, 5, 15, 25, 35, 45, 55, 65, 75, 85],
           }
    STEP = {'min': [15, -15, 15, -15, 15, -30, 30],
            'norm': [10, -10, 10, -10, 10, -20, 20],
            'med': [10, -10, 10, -10, 10, -10, 10, -30, 30],
            'max': [10, -10, 10, -10, 10, -10, 10, -10, 10, -30, 30],
            }
    START = [-120, -5, -120, -5, -120, -5, -120, -5, -120, -5, -120,
             5, 120, 5, 120, 5, 120, 5, 120, 5, 120, 5, 120, 5, 120]
    STOP = [0, -120, 0, -120, 0, -120, 0, -120, 0, -120, 0,
            120, 0, 120, 0, 120, 0, 120, 0, 120, 0, 120, 0]

    def __init__(self,
                 lat=48,
                 ):

        self.lat = lat
        self._horizonPFile = None
        self._buildPFile = None
        self._horizonP = list()
        self._buildP = list()

    @property
    def lat(self):
        return self._lat

    @lat.setter
    def lat(self, value):
        self._lat = value

    @property
    def horizonPFile(self):
        return self._horizonPFile

    @horizonPFile.setter
    def horizonPFile(self, value):
        self._horizonPFile = value

    @property
    def buildPFile(self):
        return self._buildPFile

    @buildPFile.setter
    def buildPFile(self, value):
        self._buildPFile = value

    @staticmethod
    def topoToAzAlt(ha, dec, lat):
        ha = (ha * 360 / 24 + 360.0) % 360.0
        dec = np.radians(dec)
        ha = np.radians(ha)
        lat = np.radians(lat)
        alt = np.arcsin(np.sin(dec) * np.sin(lat) + np.cos(dec) * np.cos(lat) * np.cos(ha))
        value = (np.sin(dec) - np.sin(alt) * np.sin(lat)) / (np.cos(alt) * np.cos(lat))
        # value = np.clip(value, -1.0, 1.0)
        A = np.arccos(value)
        if np.sin(ha) >= 0.0:
            az = 2*np.pi - A
        else:
            az = A
        az = np.degrees(az)
        alt = np.degrees(alt)
        return alt, az

    @property
    def buildP(self):
        return self._buildP

    @buildP.setter
    def buildP(self, value):
        if not isinstance(value, list):
            self._buildP = list()
            return
        if not all([isinstance(x, tuple) for x in value]):
            self.logger.error('malformed value: {0}'.format(value))
            self._buildP = list()
            return
        self._buildP = value

    def addBuildP(self, value):
        if not isinstance(value, tuple):
            self.logger.error('malformed value: {0}'.format(value))
            return False
        if len(value) != 2:
            self.logger.error('malformed value: {0}'.format(value))
            return False
        self._buildP.insert(len(self._buildP), value)
        return True

    def delBuildP(self, value):
        if not isinstance(value, (int, float)):
            self.logger.error('malformed value: {0}'.format(value))
            return False
        value = int(value)
        if value < 0 or value > len(self._buildP) - 1:
            self.logger.error('invalid value: {0}'.format(value))
            return False
        self._buildP.pop(value)
        return True

    def clearBuildP(self):
        self._buildP = list()

    @property
    def horizonP(self):
        return self._horizonP

    @horizonP.setter
    def horizonP(self, value):
        if not isinstance(value, list):
            self._horizonP = list()
            return
        if not all([isinstance(x, tuple) for x in value]):
            self.logger.error('malformed value: {0}'.format(value))
            self._horizonP = list()
            return
        self._horizonP = value

    def addHorizonP(self, value):
        if not isinstance(value, list):
            self.logger.error('malformed value: {0}'.format(value))
            return False
        if len(value) != 2:
            self.logger.error('malformed value: {0}'.format(value))
            return False
        self._horizonP.insert(len(self._horizonP), value)
        return True

    def delHorizonP(self, value):
        if not isinstance(value, (int, float)):
            self.logger.error('malformed value: {0}'.format(value))
            return False
        value = int(value)
        if value < 0 or value > len(self._horizonP) - 1:
            self.logger.error('invalid value: {0}'.format(value))
            return False
        self._horizonP.pop(value)
        return True

    def clearHorizonP(self):
        self._horizonP = list()

    def genHaDecParams(self, selection):
        """
        genHaDecParams selects the parameters for generating the boundaries for next
        step processing greater circles. the parameters are sorted for different targets
        actually for minimum slew distance between the points. defined is only the east
        side of data, the west side will be mirrored to the east one.

        :param selection: type of model we would like to use
        :return: yield tuple of dec value and step, start and stop for range
        """

        if selection not in self.DEC or selection not in self.STEP:
            return
        eastDec = self.DEC[selection]
        westDec = list(reversed(eastDec))
        decL = eastDec + westDec

        eastL = self.STEP[selection]
        westL = list(reversed(eastL))
        stepL = eastL + westL

        for dec, step, start, stop in zip(decL, stepL, self.START, self.STOP):
            yield dec, step, start, stop

    def genGreaterCircle(self, selection='norm'):
        """
        genGreaterCircle takes the generated boundaries for the rang routine and
        transforms ha, dec to alt az. reasonable values for the alt az values
        are 5 to 85 degrees.

        :param selection:
        :return: yields alt, az tuples which are above horizon
        """

        for dec, step, start, stop in self.genHaDecParams(selection):
            for ha in range(start, stop, step):
                alt, az = self.topoToAzAlt(ha/10, dec, self.lat)
                # only values with above horizon = 0
                if 5 <= alt <= 85 and az < 360:
                    yield alt, az

    @staticmethod
    def genGrid(minAlt=5, maxAlt=85, numbRows=5, numbCols=6):
        """
        genGrid generates a grid of points and transforms ha, dec to alt az. with given
        limits in alt, the min and max will be used as a hard condition. on az there is
        not given limit, therefore a split over the whole space (omitting the meridian)
        is done. the simplest way to avoid hitting the meridian is to enforce the number
        of cols to be a factor of 2. reasonable values for the grid are 5 to 85 degrees.
        defined is only the east side of data, the west side will be mirrored to the
        east one.

        :param minAlt: altitude min
        :param maxAlt: altitude max
        :param numbRows: numbRows
        :param numbCols: numbCols
        :return: yields alt, az tuples which are above horizon
        """

        if not 5 <= minAlt <= 85:
            return
        if not 5 <= maxAlt <= 85:
            return
        if not maxAlt > minAlt:
            return
        if numbCols % 2:
            return

        stepAlt = int((maxAlt - minAlt) / (numbRows - 1))
        eastAlt = list(range(minAlt, maxAlt, stepAlt))
        westAlt = list(reversed(eastAlt))

        stepAz = int(360 / numbCols)
        minAz = int(180 / numbCols)
        maxAz = 360 - minAz

        for i, alt in enumerate(eastAlt):
            if i % 2:
                for az in range(minAz, 180, stepAz):
                    yield alt, az
            else:
                for az in range(180 - minAz, 0, -stepAz):
                    yield alt, az
        for i, alt in enumerate(westAlt):
            if i % 2:
                for az in range(180 + minAz, 360, stepAz):
                    yield alt, az
            else:
                for az in range(maxAz, 180, -stepAz):
                    yield alt, az