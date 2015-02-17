# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'area_div.ui'
#
# Created: Tue Feb 17 11:28:30 2015
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

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
        AreaDivDialog.setAccessibleName(_fromUtf8(""))
        AreaDivDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.DivideButton = QtGui.QPushButton(AreaDivDialog)
        self.DivideButton.setGeometry(QtCore.QRect(120, 140, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.DivideButton.sizePolicy().hasHeightForWidth())
        self.DivideButton.setSizePolicy(sizePolicy)
        self.DivideButton.setObjectName(_fromUtf8("DivideButton"))
        self.CancelButton = QtGui.QPushButton(AreaDivDialog)
        self.CancelButton.setGeometry(QtCore.QRect(220, 140, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CancelButton.sizePolicy().hasHeightForWidth())
        self.CancelButton.setSizePolicy(sizePolicy)
        self.CancelButton.setObjectName(_fromUtf8("CancelButton"))
        self.AreaDivGroup = QtGui.QGroupBox(AreaDivDialog)
        self.AreaDivGroup.setGeometry(QtCore.QRect(10, 10, 301, 121))
        self.AreaDivGroup.setObjectName(_fromUtf8("AreaDivGroup"))
        self.AreaLineEdit = QtGui.QLineEdit(self.AreaDivGroup)
        self.AreaLineEdit.setGeometry(QtCore.QRect(170, 20, 121, 20))
        self.AreaLineEdit.setObjectName(_fromUtf8("AreaLineEdit"))
        self.AreaLabel = QtGui.QLabel(self.AreaDivGroup)
        self.AreaLabel.setGeometry(QtCore.QRect(10, 20, 151, 16))
        self.AreaLabel.setObjectName(_fromUtf8("AreaLabel"))
        self.OnePointRadio = QtGui.QRadioButton(self.AreaDivGroup)
        self.OnePointRadio.setGeometry(QtCore.QRect(10, 90, 271, 17))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OnePointRadio.sizePolicy().hasHeightForWidth())
        self.OnePointRadio.setSizePolicy(sizePolicy)
        self.OnePointRadio.setObjectName(_fromUtf8("OnePointRadio"))
        self.TwoPointRadio = QtGui.QRadioButton(self.AreaDivGroup)
        self.TwoPointRadio.setGeometry(QtCore.QRect(10, 70, 271, 17))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TwoPointRadio.sizePolicy().hasHeightForWidth())
        self.TwoPointRadio.setSizePolicy(sizePolicy)
        self.TwoPointRadio.setObjectName(_fromUtf8("TwoPointRadio"))
        self.TotalLabel = QtGui.QLabel(self.AreaDivGroup)
        self.TotalLabel.setGeometry(QtCore.QRect(10, 40, 151, 16))
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
        AreaDivDialog.setWindowTitle(_translate("AreaDivDialog", "Area Division", None))
        self.DivideButton.setText(_translate("AreaDivDialog", "Divide", None))
        self.CancelButton.setText(_translate("AreaDivDialog", "Cancel", None))
        self.AreaDivGroup.setTitle(_translate("AreaDivDialog", "Divide selected area", None))
        self.AreaLabel.setText(_translate("AreaDivDialog", "Area (in layer units)", None))
        self.OnePointRadio.setText(_translate("AreaDivDialog", "Through the first given point", None))
        self.TwoPointRadio.setText(_translate("AreaDivDialog", "Parallel to the given line", None))
        self.TotalLabel.setText(_translate("AreaDivDialog", "Full area", None))

