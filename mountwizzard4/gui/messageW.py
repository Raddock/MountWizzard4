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
import datetime
import time
# external packages
import PyQt5.QtCore
import PyQt5.QtWidgets
import PyQt5.uic
# local import
import mw4_global
import base.widget as mWidget
from gui import message_ui


class MessageWindow(mWidget.MWidget):
    logger = logging.getLogger(__name__)

    def __init__(self, app):
        super(MessageWindow, self).__init__()
        self.app = app
        self.showStatus = False
        self.ui = message_ui.Ui_MessageDialog()
        self.ui.setupUi(self)
        self.initUI()
        # allow sizing of the window
        self.setFixedSize(PyQt5.QtCore.QSize(16777215, 16777215))
        self.setSizePolicy(PyQt5.QtWidgets.QSizePolicy.Ignored,
                           PyQt5.QtWidgets.QSizePolicy.Ignored)
        self.setMinimumSize(800, 200)
        self.setMaximumSize(800, 16777215)

        # link gui blocks
        self.message.connect(self.writeMessage)
        self.showWindow()

    def resizeEvent(self, QResizeEvent):
        super().resizeEvent(QResizeEvent)
        self.ui.message.setGeometry(10, 10, 780, self.height() - 20)

    def closeEvent(self, closeEvent):
        super().closeEvent(closeEvent)
        self.changeStylesheet(self.app.mainW.ui.openMessageW, 'running', 'false')

    def toggleWindow(self):
        self.showStatus = not self.showStatus
        if self.showStatus:
            self.showWindow()
        else:
            self.close()

    def showWindow(self):
        self.showStatus = True
        self.show()
        self.changeStylesheet(self.app.mainW.ui.openMessageW, 'running', 'true')

    def writeMessage(self, message):
        prefix = time.strftime('%H:%M:%S - ', time.localtime())
        message = prefix + message

        self.logger.info('Message window: {0}'.format(message))
        self.ui.message.setTextColor(color)
        self.ui.message.insertPlainText(message + '\n')

