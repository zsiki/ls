# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'coords.ui'
#
# Created: Sun May 17 09:57:06 2015
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_CoordDialog(object):
    def setupUi(self, CoordDialog):
        CoordDialog.setObjectName(_fromUtf8("CoordDialog"))
        CoordDialog.resize(320, 172)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(CoordDialog.sizePolicy().hasHeightForWidth())
        CoordDialog.setSizePolicy(sizePolicy)
        CoordDialog.setMinimumSize(QtCore.QSize(320, 172))
        CoordDialog.setMaximumSize(QtCore.QSize(320, 172))
        CoordDialog.setWindowTitle(QtGui.QApplication.translate("CoordDialog", "Area Division", None, QtGui.QApplication.UnicodeUTF8))
        CoordDialog.setAccessibleName(_fromUtf8(""))
        CoordDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.ContinueButton = QtGui.QPushButton(CoordDialog)
        self.ContinueButton.setGeometry(QtCore.QRect(120, 140, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ContinueButton.sizePolicy().hasHeightForWidth())
        self.ContinueButton.setSizePolicy(sizePolicy)
        self.ContinueButton.setText(QtGui.QApplication.translate("CoordDialog", "Continue", None, QtGui.QApplication.UnicodeUTF8))
        self.ContinueButton.setObjectName(_fromUtf8("ContinueButton"))
        self.CancelButton = QtGui.QPushButton(CoordDialog)
        self.CancelButton.setGeometry(QtCore.QRect(220, 140, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CancelButton.sizePolicy().hasHeightForWidth())
        self.CancelButton.setSizePolicy(sizePolicy)
        self.CancelButton.setText(QtGui.QApplication.translate("CoordDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setObjectName(_fromUtf8("CancelButton"))
        self.DivLineGroup = QtGui.QGroupBox(CoordDialog)
        self.DivLineGroup.setGeometry(QtCore.QRect(10, 10, 301, 121))
        self.DivLineGroup.setTitle(QtGui.QApplication.translate("CoordDialog", "Division line", None, QtGui.QApplication.UnicodeUTF8))
        self.DivLineGroup.setObjectName(_fromUtf8("DivLineGroup"))
        self.StartEast = QtGui.QLineEdit(self.DivLineGroup)
        self.StartEast.setGeometry(QtCore.QRect(170, 20, 121, 20))
        self.StartEast.setObjectName(_fromUtf8("StartEast"))
        self.StartEastLabel = QtGui.QLabel(self.DivLineGroup)
        self.StartEastLabel.setGeometry(QtCore.QRect(10, 20, 151, 16))
        self.StartEastLabel.setText(QtGui.QApplication.translate("CoordDialog", "Startpoint east", None, QtGui.QApplication.UnicodeUTF8))
        self.StartEastLabel.setObjectName(_fromUtf8("StartEastLabel"))
        self.StartNorthLabel = QtGui.QLabel(self.DivLineGroup)
        self.StartNorthLabel.setGeometry(QtCore.QRect(10, 40, 151, 16))
        self.StartNorthLabel.setText(QtGui.QApplication.translate("CoordDialog", "Startpoint north", None, QtGui.QApplication.UnicodeUTF8))
        self.StartNorthLabel.setObjectName(_fromUtf8("StartNorthLabel"))
        self.StartNorth = QtGui.QLineEdit(self.DivLineGroup)
        self.StartNorth.setGeometry(QtCore.QRect(170, 40, 121, 20))
        self.StartNorth.setReadOnly(True)
        self.StartNorth.setObjectName(_fromUtf8("StartNorth"))
        self.EndNorthLabel = QtGui.QLabel(self.DivLineGroup)
        self.EndNorthLabel.setGeometry(QtCore.QRect(10, 90, 151, 16))
        self.EndNorthLabel.setText(QtGui.QApplication.translate("CoordDialog", "Endpoint north", None, QtGui.QApplication.UnicodeUTF8))
        self.EndNorthLabel.setObjectName(_fromUtf8("EndNorthLabel"))
        self.EndEast = QtGui.QLineEdit(self.DivLineGroup)
        self.EndEast.setGeometry(QtCore.QRect(170, 70, 121, 20))
        self.EndEast.setObjectName(_fromUtf8("EndEast"))
        self.EndNorth = QtGui.QLineEdit(self.DivLineGroup)
        self.EndNorth.setGeometry(QtCore.QRect(170, 90, 121, 20))
        self.EndNorth.setReadOnly(True)
        self.EndNorth.setObjectName(_fromUtf8("EndNorth"))
        self.EndEastLabel = QtGui.QLabel(self.DivLineGroup)
        self.EndEastLabel.setGeometry(QtCore.QRect(10, 70, 151, 16))
        self.EndEastLabel.setText(QtGui.QApplication.translate("CoordDialog", "Endpoint east", None, QtGui.QApplication.UnicodeUTF8))
        self.EndEastLabel.setObjectName(_fromUtf8("EndEastLabel"))

        self.retranslateUi(CoordDialog)
        QtCore.QMetaObject.connectSlotsByName(CoordDialog)
        CoordDialog.setTabOrder(self.StartEast, self.ContinueButton)
        CoordDialog.setTabOrder(self.ContinueButton, self.CancelButton)

    def retranslateUi(self, CoordDialog):
        pass

