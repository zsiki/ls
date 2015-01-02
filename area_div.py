# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'area_div.ui'
#
# Created: Fri Jan  2 13:44:36 2015
#      by: PyQt4 UI code generator 4.8.6
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
        self.DivideButton = QtGui.QPushButton(AreaDivDialog)
        self.DivideButton.setGeometry(QtCore.QRect(120, 140, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DivideButton.sizePolicy().hasHeightForWidth())
        self.DivideButton.setSizePolicy(sizePolicy)
        self.DivideButton.setText(QtGui.QApplication.translate("AreaDivDialog", "Divide", None, QtGui.QApplication.UnicodeUTF8))
        self.DivideButton.setObjectName(_fromUtf8("DivideButton"))
        self.CancelButton = QtGui.QPushButton(AreaDivDialog)
        self.CancelButton.setGeometry(QtCore.QRect(220, 140, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CancelButton.sizePolicy().hasHeightForWidth())
        self.CancelButton.setSizePolicy(sizePolicy)
        self.CancelButton.setText(QtGui.QApplication.translate("AreaDivDialog", "Cancel", None, QtGui.QApplication.UnicodeUTF8))
        self.CancelButton.setObjectName(_fromUtf8("CancelButton"))
        self.AreaDivGroup = QtGui.QGroupBox(AreaDivDialog)
        self.AreaDivGroup.setGeometry(QtCore.QRect(10, 10, 301, 121))
        self.AreaDivGroup.setTitle(QtGui.QApplication.translate("AreaDivDialog", "Divide selected area", None, QtGui.QApplication.UnicodeUTF8))
        self.AreaDivGroup.setObjectName(_fromUtf8("AreaDivGroup"))
        self.AreaLineEdit = QtGui.QLineEdit(self.AreaDivGroup)
        self.AreaLineEdit.setGeometry(QtCore.QRect(170, 20, 121, 20))
        self.AreaLineEdit.setObjectName(_fromUtf8("AreaLineEdit"))
        self.AreaLabel = QtGui.QLabel(self.AreaDivGroup)
        self.AreaLabel.setGeometry(QtCore.QRect(10, 20, 151, 16))
        self.AreaLabel.setText(QtGui.QApplication.translate("AreaDivDialog", "Area (in layer units)", None, QtGui.QApplication.UnicodeUTF8))
        self.AreaLabel.setObjectName(_fromUtf8("AreaLabel"))
        self.OnePointRadio = QtGui.QRadioButton(self.AreaDivGroup)
        self.OnePointRadio.setGeometry(QtCore.QRect(10, 90, 271, 17))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OnePointRadio.sizePolicy().hasHeightForWidth())
        self.OnePointRadio.setSizePolicy(sizePolicy)
        self.OnePointRadio.setText(QtGui.QApplication.translate("AreaDivDialog", "Through the first given point", None, QtGui.QApplication.UnicodeUTF8))
        self.OnePointRadio.setObjectName(_fromUtf8("OnePointRadio"))
        self.TwoPointRadio = QtGui.QRadioButton(self.AreaDivGroup)
        self.TwoPointRadio.setGeometry(QtCore.QRect(10, 70, 271, 17))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TwoPointRadio.sizePolicy().hasHeightForWidth())
        self.TwoPointRadio.setSizePolicy(sizePolicy)
        self.TwoPointRadio.setText(QtGui.QApplication.translate("AreaDivDialog", "Paralel to the given line", None, QtGui.QApplication.UnicodeUTF8))
        self.TwoPointRadio.setObjectName(_fromUtf8("TwoPointRadio"))
        self.TotalLabel = QtGui.QLabel(self.AreaDivGroup)
        self.TotalLabel.setGeometry(QtCore.QRect(10, 40, 151, 16))
        self.TotalLabel.setText(QtGui.QApplication.translate("AreaDivDialog", "Full area", None, QtGui.QApplication.UnicodeUTF8))
        self.TotalLabel.setObjectName(_fromUtf8("TotalLabel"))
        self.TotalLineEdit = QtGui.QLineEdit(self.AreaDivGroup)
        self.TotalLineEdit.setGeometry(QtCore.QRect(170, 40, 121, 20))
        self.TotalLineEdit.setReadOnly(True)
        self.TotalLineEdit.setObjectName(_fromUtf8("TotalLineEdit"))

        self.retranslateUi(AreaDivDialog)
        QtCore.QMetaObject.connectSlotsByName(AreaDivDialog)
        AreaDivDialog.setTabOrder(self.AreaLineEdit, self.OnePointRadio)
        AreaDivDialog.setTabOrder(self.OnePointRadio, self.TwoPointRadio)
        AreaDivDialog.setTabOrder(self.TwoPointRadio, self.DivideButton)
        AreaDivDialog.setTabOrder(self.DivideButton, self.CancelButton)

    def retranslateUi(self, AreaDivDialog):
        pass

