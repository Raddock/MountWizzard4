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
import PyQt5.QtCore
# local import
import mw4_global
import mountcontrol.qtmount
import gui.mainW
import gui.messageW


class MountWizzard4(object):
    """
    MountWizzard4 class is the main class for the application. it loads all windows and
    classes needed to fulfil the work of mountwizzard. any gui work should be handled
    through the window classes. main class is for setup, config, start, persist and
    shutdown the application.
    """

    __all__ = ['MountWizzard4',
               ]
    version = '0.1'
    logger = logging.getLogger(__name__)

    def __init__(self):
        super().__init__()
        # get the working horses up
        pathToTs = mw4_global.work_dir + '/config'
        self.mount = mountcontrol.qtmount.Mount(host='192.168.2.15',
                                                MAC='00.c0.08.87.35.db',
                                                pathToTS=pathToTs,
                                                expire=False,
                                                verbose=False,
                                                )
        # get the window widgets up
        self.mainW = gui.mainW.MainWindow(self)
        self.messageW = gui.messageW.MessageWindow(self)
        # starting cyclic polling of mount data
        self.mount.startTimers()
        # managing data
        self.mount.signals.mountUp.connect(self.loadMountData)

    def quit(self):
        self.mount.stopTimers()
        PyQt5.QtCore.QCoreApplication.quit()

    def loadMountData(self, status):
        if status:
            self.mount.workaround()
            self.mount.getFW()
            self.mount.getLocation()
            self.mount.cycleSetting()
            self.mount.getNames()
            self.mount.getAlign()
        else:
            self.mount.resetData()
