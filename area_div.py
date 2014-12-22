# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'area_div.ui'
#
# Created: Mon Dec 22 10:06:20 2014
#      by: PyQt4 UI code generator 4.8.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_AreaDivDialog(object):
    def setupUi(self, AreaDivDialog):
        AreaDivDialog.setObjectName(_fromUtf8("AreaDivDialog"))
        AreaDivDialog.resize(320, 172)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AreaDivDialog.sizePolicy().hasHeightForWidth())
        AreaDivDialog.setSizePolicy(sizePolicy)
        AreaDivDialog.setMinimumSize(QtCore.QSize(320, 172))
        AreaDivDialog.setMaximumSize(QtCore.QSize(320, 172))
        AreaDivDialog.setWindowTitle(_fromUtf8("Area Division"))
        AreaDivDialog.setAccessibleName(_fromUtf8(""))
        AreaDivDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.ResetButton = QtGui.QPushButton(AreaDivDialog)
        self.ResetButton.setGeometry(QtCore.QRect(120, 140, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResetButton.sizePolicy().hasHeightForWidth())
        self.ResetButton.setSizePolicy(sizePolicy)
        self.ResetButton.setObjectName(_fromUtf8("ResetButton"))
        self.DivideButton = QtGui.QPushButton(AreaDivDialog)
        self.DivideButton.setGeometry(QtCore.QRect(20, 140, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DivideButton.sizePolicy().hasHeightForWidth())
        self.DivideButton.setSizePolicy(sizePolicy)
        self.DivideButton.setObjectName(_fromUtf8("DivideButton"))
        self.CloseButton = QtGui.QPushButton(AreaDivDialog)
        self.CloseButton.setGeometry(QtCore.QRect(220, 140, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CloseButton.sizePolicy().hasHeightForWidth())
        self.CloseButton.setSizePolicy(sizePolicy)
        self.CloseButton.setObjectName(_fromUtf8("CloseButton"))
        self.AreaDivGroup = QtGui.QGroupBox(AreaDivDialog)
        self.AreaDivGroup.setGeometry(QtCore.QRect(10, 10, 301, 121))
        self.AreaDivGroup.setObjectName(_fromUtf8("AreaDivGroup"))
        self.AreaLineEdit = QtGui.QLineEdit(self.AreaDivGroup)
        self.AreaLineEdit.setGeometry(QtCore.QRect(170, 20, 121, 20))
        self.AreaLineEdit.setObjectName(_fromUtf8("AreaLineEdit"))
        self.AreaLabel = QtGui.QLabel(self.AreaDivGroup)
        self.AreaLabel.setGeometry(QtCore.QRect(10, 20, 171, 16))
        self.AreaLabel.setObjectName(_fromUtf8("AreaLabel"))
        self.OnePointRadio = QtGui.QRadioButton(self.AreaDivGroup)
        self.OnePointRadio.setGeometry(QtCore.QRect(10, 60, 191, 17))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OnePointRadio.sizePolicy().hasHeightForWidth())
        self.OnePointRadio.setSizePolicy(sizePolicy)
        self.OnePointRadio.setObjectName(_fromUtf8("OnePointRadio"))
        self.TwoPointRadio = QtGui.QRadioButton(self.AreaDivGroup)
        self.TwoPointRadio.setGeometry(QtCore.QRect(10, 90, 191, 17))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TwoPointRadio.sizePolicy().hasHeightForWidth())
        self.TwoPointRadio.setSizePolicy(sizePolicy)
        self.TwoPointRadio.setObjectName(_fromUtf8("TwoPointRadio"))

        self.retranslateUi(AreaDivDialog)
        QtCore.QMetaObject.connectSlotsByName(AreaDivDialog)
        AreaDivDialog.setTabOrder(self.AreaLineEdit, self.OnePointRadio)
        AreaDivDialog.setTabOrder(self.OnePointRadio, self.TwoPointRadio)
        AreaDivDialog.setTabOrder(self.TwoPointRadio, self.DivideButton)
        AreaDivDialog.setTabOrder(self.DivideButton, self.ResetButton)
        AreaDivDialog.setTabOrder(self.ResetButton, self.CloseButton)

    def retranslateUi(self, AreaDivDialog):
        self.ResetButton.setText(QtGui.QApplication.translate("AreaDivDialog", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.DivideButton.setText(QtGui.QApplication.translate("AreaDivDialog", "Divide", None, QtGui.QApplication.UnicodeUTF8))
        self.CloseButton.setText(QtGui.QApplication.translate("AreaDivDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.AreaDivGroup.setTitle(QtGui.QApplication.translate("AreaDivDialog", "Divide selected area", None, QtGui.QApplication.UnicodeUTF8))
        self.AreaLabel.setText(QtGui.QApplication.translate("AreaDivDialog", "Area (in layer units)", None, QtGui.QApplication.UnicodeUTF8))
        self.OnePointRadio.setText(QtGui.QApplication.translate("AreaDivDialog", "Through a given point", None, QtGui.QApplication.UnicodeUTF8))
        self.TwoPointRadio.setText(QtGui.QApplication.translate("AreaDivDialog", "Paralel to given points", None, QtGui.QApplication.UnicodeUTF8))

