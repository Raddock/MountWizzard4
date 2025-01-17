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
import logging
import time
import json
import pkg_resources
import base64
# external packages
import PyQt5.QtCore
import PyQt5.QtWidgets
import PyQt5.uic
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEngineScript
# local import
import mw4
from mw4.gui import widget
from mw4.gui.widgets import keypad_ui


class KeypadWindow(widget.MWidget):
    """
    the KeypadWindow window class handles

    """

    __all__ = ['KeypadWindow',
               ]

    logger = logging.getLogger(__name__)

    def __init__(self, app):
        super().__init__()
        self.app = app

        self.ui = keypad_ui.Ui_KeypadDialog()
        self.ui.setupUi(self)
        self.initUI()

        # getting a new browser object
        self.browser = PyQt5.QtWebEngineWidgets.QWebEngineView()

        # adding it to window widget
        self.ui.keypad.addWidget(self.browser)

        # avoid flickering in white
        self.browser.setVisible(False)
        self.browser.page().setBackgroundColor(PyQt5.QtCore.Qt.transparent)

        self.initConfig()
        self.showWindow()

    def initConfig(self):
        """
        initConfig read the key out of the configuration dict and stores it to the gui
        elements. if some initialisations have to be proceeded with the loaded persistent
        data, they will be launched as well in this method.

        :return: True for test purpose
        """

        if 'keypadW' not in self.app.config:
            self.app.config['keypadW'] = {}

        config = self.app.config['keypadW']
        x = config.get('winPosX', 100)
        y = config.get('winPosY', 100)
        if x > self.screenSizeX:
            x = 0
        if y > self.screenSizeY:
            y = 0
        self.move(x, y)
        height = config.get('height', 500)
        width = config.get('width', 260)
        self.resize(width, height)
        return True

    def storeConfig(self):
        """
        storeConfig writes the keys to the configuration dict and stores. if some
        saving has to be proceeded to persistent data, they will be launched as
        well in this method.

        :return: True for test purpose
        """
        if 'keypadW' not in self.app.config:
            self.app.config['keypadW'] = {}
        config = self.app.config['keypadW']
        config['winPosX'] = self.pos().x()
        config['winPosY'] = self.pos().y()
        config['height'] = self.height()
        config['width'] = self.width()

        return True

    def closeEvent(self, closeEvent):
        """

        :param closeEvent:
        :return:
        """

        # save config
        self.storeConfig()

        # gui signals
        self.browser.loadFinished.disconnect(self.loadFinished)

        # remove big object
        self.browser = None

        super().closeEvent(closeEvent)

    def showWindow(self):
        """

        :return:
        """

        self.browser.loadFinished.connect(self.loadFinished)
        self.showUrl()
        self.show()

    def loadFinished(self):
        """

        :return:
        """

        self.browser.setVisible(True)

    def showUrl(self):
        """

        :return: success
        """

        host = self.app.mainW.ui.mountHost.text()

        if not host:
            return False

        file = f'qrc:/webif/virtkeypad.html?host={host}'
        self.browser.load(PyQt5.QtCore.QUrl(file))

        return True
