############################################################
# -*- coding: utf-8 -*-
#
# Python-based Tool for interaction with the 10micron mounts
# GUI with PyQT5 for python
# Python  v3.5
#
# Michael Würtenberger
# (c) 2016, 2017, 2018
#
# Licence APL2.0
#
############################################################
# standard libraries
from threading import Lock
# external packages
# noinspection PyProtectedMember
from astropy import _erfa as ERFA
import skyfield.api
# local import

_lock = Lock()


def JNowToJ2000(ra, dec, timeJD):
    with _lock:
        jdtt = timeJD.tt
        jd = timeJD.ut1

        ra = ra.radians
        dec = dec.radians

        delta = ERFA.eo06a(jdtt, 0.0)
        ra = ERFA.anp(ra + delta)

        raConv, decConv, _ = ERFA.atic13(ra, dec, jd, 0.0)

        ra = skyfield.api.Angle(radians=raConv, preference='hours')
        dec = skyfield.api.Angle(radians=decConv, preference='degrees')
        return ra, dec


def J2000ToJNow(ra, dec, timeJD):
    with _lock:

        jd = timeJD.ut1

        ra = ra.radians
        dec = dec.radians

        raConv, decConv, eo = ERFA.atci13(ra, dec, 0, 0, 0, 0, jd, 0)

        raConv = ERFA.anp(raConv - eo)
        ra = skyfield.api.Angle(radians=raConv, preference='hours')
        dec = skyfield.api.Angle(radians=decConv, preference='degrees')
        return ra, dec

