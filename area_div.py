# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'area_div.ui'
#
# Created: Sun Dec 21 22:04:13 2014
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
        AreaDivDialog.resize(343, 251)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(AreaDivDialog.sizePolicy().hasHeightForWidth())
        AreaDivDialog.setSizePolicy(sizePolicy)
        AreaDivDialog.setMinimumSize(QtCore.QSize(343, 251))
        AreaDivDialog.setMaximumSize(QtCore.QSize(343, 251))
        AreaDivDialog.setWindowTitle(_fromUtf8("Area Division"))
        AreaDivDialog.setAccessibleName(_fromUtf8(""))
        AreaDivDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.ResetButton = QtGui.QPushButton(AreaDivDialog)
        self.ResetButton.setGeometry(QtCore.QRect(130, 220, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ResetButton.sizePolicy().hasHeightForWidth())
        self.ResetButton.setSizePolicy(sizePolicy)
        self.ResetButton.setText(QtGui.QApplication.translate("AreaDivDialog", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.ResetButton.setObjectName(_fromUtf8("ResetButton"))
        self.AddButton = QtGui.QPushButton(AreaDivDialog)
        self.AddButton.setGeometry(QtCore.QRect(20, 220, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.AddButton.sizePolicy().hasHeightForWidth())
        self.AddButton.setSizePolicy(sizePolicy)
        self.AddButton.setText(QtGui.QApplication.translate("AreaDivDialog", "Divide", None, QtGui.QApplication.UnicodeUTF8))
        self.AddButton.setObjectName(_fromUtf8("AddButton"))
        self.CloseButton = QtGui.QPushButton(AreaDivDialog)
        self.CloseButton.setGeometry(QtCore.QRect(240, 220, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CloseButton.sizePolicy().hasHeightForWidth())
        self.CloseButton.setSizePolicy(sizePolicy)
        self.CloseButton.setText(QtGui.QApplication.translate("AreaDivDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.CloseButton.setObjectName(_fromUtf8("CloseButton"))
        self.AreaDivGroup = QtGui.QGroupBox(AreaDivDialog)
        self.AreaDivGroup.setGeometry(QtCore.QRect(10, 10, 321, 191))
        self.AreaDivGroup.setTitle(QtGui.QApplication.translate("AreaDivDialog", "Divide selected area", None, QtGui.QApplication.UnicodeUTF8))
        self.AreaDivGroup.setObjectName(_fromUtf8("AreaDivGroup"))
        self.AreaLineEdit = QtGui.QLineEdit(self.AreaDivGroup)
        self.AreaLineEdit.setGeometry(QtCore.QRect(190, 20, 121, 20))
        self.AreaLineEdit.setObjectName(_fromUtf8("AreaLineEdit"))
        self.AreaLabel = QtGui.QLabel(self.AreaDivGroup)
        self.AreaLabel.setGeometry(QtCore.QRect(10, 20, 171, 16))
        self.AreaLabel.setText(QtGui.QApplication.translate("AreaDivDialog", "Area (in layer units)", None, QtGui.QApplication.UnicodeUTF8))
        self.AreaLabel.setObjectName(_fromUtf8("AreaLabel"))
        self.OnePointRadio = QtGui.QRadioButton(self.AreaDivGroup)
        self.OnePointRadio.setGeometry(QtCore.QRect(10, 60, 191, 17))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OnePointRadio.sizePolicy().hasHeightForWidth())
        self.OnePointRadio.setSizePolicy(sizePolicy)
        self.OnePointRadio.setText(QtGui.QApplication.translate("AreaDivDialog", "Through a given point", None, QtGui.QApplication.UnicodeUTF8))
        self.OnePointRadio.setObjectName(_fromUtf8("OnePointRadio"))
        self.TwoPointRadio = QtGui.QRadioButton(self.AreaDivGroup)
        self.TwoPointRadio.setGeometry(QtCore.QRect(10, 90, 191, 17))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TwoPointRadio.sizePolicy().hasHeightForWidth())
        self.TwoPointRadio.setSizePolicy(sizePolicy)
        self.TwoPointRadio.setText(QtGui.QApplication.translate("AreaDivDialog", "Paralel to given points", None, QtGui.QApplication.UnicodeUTF8))
        self.TwoPointRadio.setObjectName(_fromUtf8("TwoPointRadio"))

        self.retranslateUi(AreaDivDialog)
        QtCore.QMetaObject.connectSlotsByName(AreaDivDialog)
        AreaDivDialog.setTabOrder(self.AreaLineEdit, self.AddButton)
        AreaDivDialog.setTabOrder(self.AddButton, self.ResetButton)
        AreaDivDialog.setTabOrder(self.ResetButton, self.CloseButton)

    def retranslateUi(self, AreaDivDialog):
        pass

