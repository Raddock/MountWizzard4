# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'message.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MessageDialog(object):
    def setupUi(self, MessageDialog):
        MessageDialog.setObjectName("MessageDialog")
        MessageDialog.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MessageDialog.sizePolicy().hasHeightForWidth())
        MessageDialog.setSizePolicy(sizePolicy)
        MessageDialog.setMinimumSize(QtCore.QSize(800, 200))
        MessageDialog.setMaximumSize(QtCore.QSize(800, 1200))
        MessageDialog.setSizeIncrement(QtCore.QSize(10, 10))
        MessageDialog.setBaseSize(QtCore.QSize(10, 10))
        font = QtGui.QFont()
        font.setFamily("Arial")
        MessageDialog.setFont(font)
        self.message = QtWidgets.QTextBrowser(MessageDialog)
        self.message.setGeometry(QtCore.QRect(5, 5, 790, 591))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.message.sizePolicy().hasHeightForWidth())
        self.message.setSizePolicy(sizePolicy)
        self.message.setMinimumSize(QtCore.QSize(790, 190))
        self.message.setMaximumSize(QtCore.QSize(790, 1190))
        self.message.setSizeIncrement(QtCore.QSize(10, 10))
        self.message.setBaseSize(QtCore.QSize(10, 10))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.message.setFont(font)
        self.message.setAcceptDrops(False)
        self.message.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.message.setFrameShadow(QtWidgets.QFrame.Plain)
        self.message.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.message.setHtml("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Arial\'; font-size:10pt; font-weight:600; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>")
        self.message.setAcceptRichText(False)
        self.message.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.message.setPlaceholderText("")
        self.message.setSearchPaths([])
        self.message.setOpenLinks(False)
        self.message.setObjectName("message")

        self.retranslateUi(MessageDialog)
        QtCore.QMetaObject.connectSlotsByName(MessageDialog)

    def retranslateUi(self, MessageDialog):
        _translate = QtCore.QCoreApplication.translate
        MessageDialog.setWindowTitle(_translate("MessageDialog", "Messages"))
        self.message.setToolTip(_translate("MessageDialog", "Error Messages from Tool"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MessageDialog = QtWidgets.QWidget()
    ui = Ui_MessageDialog()
    ui.setupUi(MessageDialog)
    MessageDialog.show()
    sys.exit(app.exec_())
