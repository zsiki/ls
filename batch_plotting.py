# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'batch_plotting.ui'
#
# Created: Thu Dec 11 15:47:27 2014
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

class Ui_BatchPlottingDialog(object):
    def setupUi(self, BatchPlottingDialog):
        BatchPlottingDialog.setObjectName(_fromUtf8("BatchPlottingDialog"))
        BatchPlottingDialog.resize(291, 300)
        self.TemplateList = QtGui.QListWidget(BatchPlottingDialog)
        self.TemplateList.setGeometry(QtCore.QRect(10, 30, 271, 101))
        self.TemplateList.setObjectName(_fromUtf8("TemplateList"))
        self.TemplateLabel = QtGui.QLabel(BatchPlottingDialog)
        self.TemplateLabel.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.TemplateLabel.setObjectName(_fromUtf8("TemplateLabel"))
        self.PrintButton = QtGui.QPushButton(BatchPlottingDialog)
        self.PrintButton.setGeometry(QtCore.QRect(50, 260, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PrintButton.sizePolicy().hasHeightForWidth())
        self.PrintButton.setSizePolicy(sizePolicy)
        self.PrintButton.setObjectName(_fromUtf8("PrintButton"))
        self.CloseButton = QtGui.QPushButton(BatchPlottingDialog)
        self.CloseButton.setGeometry(QtCore.QRect(160, 260, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CloseButton.sizePolicy().hasHeightForWidth())
        self.CloseButton.setSizePolicy(sizePolicy)
        self.CloseButton.setObjectName(_fromUtf8("CloseButton"))
        self.ScaleLabel = QtGui.QLabel(BatchPlottingDialog)
        self.ScaleLabel.setGeometry(QtCore.QRect(10, 140, 51, 21))
        self.ScaleLabel.setObjectName(_fromUtf8("ScaleLabel"))
        self.ScaleCombo = QtGui.QComboBox(BatchPlottingDialog)
        self.ScaleCombo.setGeometry(QtCore.QRect(60, 140, 81, 22))
        self.ScaleCombo.setEditable(True)
        self.ScaleCombo.setObjectName(_fromUtf8("ScaleCombo"))
        self.ScaleCombo.addItem(_fromUtf8(""))
        self.ScaleCombo.addItem(_fromUtf8(""))
        self.ScaleCombo.addItem(_fromUtf8(""))
        self.ScaleCombo.addItem(_fromUtf8(""))
        self.ScaleCombo.addItem(_fromUtf8(""))
        self.ScaleCombo.addItem(_fromUtf8(""))
        self.ScaleCombo.addItem(_fromUtf8(""))
        self.ScaleCombo.addItem(_fromUtf8(""))
        self.ScaleCombo.addItem(_fromUtf8(""))
        self.ScaleCombo.addItem(_fromUtf8(""))
        self.ScaleCombo.addItem(_fromUtf8(""))
        self.ScaleCombo.addItem(_fromUtf8(""))
        self.TempDirButton = QtGui.QPushButton(BatchPlottingDialog)
        self.TempDirButton.setGeometry(QtCore.QRect(200, 10, 81, 21))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TempDirButton.sizePolicy().hasHeightForWidth())
        self.TempDirButton.setSizePolicy(sizePolicy)
        self.TempDirButton.setObjectName(_fromUtf8("TempDirButton"))
        self.TODOLabel = QtGui.QLabel(BatchPlottingDialog)
        self.TODOLabel.setGeometry(QtCore.QRect(70, 200, 111, 16))
        self.TODOLabel.setObjectName(_fromUtf8("TODOLabel"))

        self.retranslateUi(BatchPlottingDialog)
        self.ScaleCombo.setCurrentIndex(3)
        QtCore.QMetaObject.connectSlotsByName(BatchPlottingDialog)
        BatchPlottingDialog.setTabOrder(self.TemplateList, self.ScaleCombo)
        BatchPlottingDialog.setTabOrder(self.ScaleCombo, self.PrintButton)
        BatchPlottingDialog.setTabOrder(self.PrintButton, self.CloseButton)

    def retranslateUi(self, BatchPlottingDialog):
        BatchPlottingDialog.setWindowTitle(_translate("BatchPlottingDialog", "Dialog", None))
        self.TemplateLabel.setText(_translate("BatchPlottingDialog", "Available templates:", None))
        self.PrintButton.setText(_translate("BatchPlottingDialog", "Print", None))
        self.CloseButton.setText(_translate("BatchPlottingDialog", "Close", None))
        self.ScaleLabel.setText(_translate("BatchPlottingDialog", "Scale:", None))
        self.ScaleCombo.setItemText(0, _translate("BatchPlottingDialog", "100", None))
        self.ScaleCombo.setItemText(1, _translate("BatchPlottingDialog", "250", None))
        self.ScaleCombo.setItemText(2, _translate("BatchPlottingDialog", "500", None))
        self.ScaleCombo.setItemText(3, _translate("BatchPlottingDialog", "1000", None))
        self.ScaleCombo.setItemText(4, _translate("BatchPlottingDialog", "2000", None))
        self.ScaleCombo.setItemText(5, _translate("BatchPlottingDialog", "2500", None))
        self.ScaleCombo.setItemText(6, _translate("BatchPlottingDialog", "5000", None))
        self.ScaleCombo.setItemText(7, _translate("BatchPlottingDialog", "10000", None))
        self.ScaleCombo.setItemText(8, _translate("BatchPlottingDialog", "20000", None))
        self.ScaleCombo.setItemText(9, _translate("BatchPlottingDialog", "25000", None))
        self.ScaleCombo.setItemText(10, _translate("BatchPlottingDialog", "50000", None))
        self.ScaleCombo.setItemText(11, _translate("BatchPlottingDialog", "100000", None))
        self.TempDirButton.setText(_translate("BatchPlottingDialog", "Change Dir ...", None))
        self.TODOLabel.setText(_translate("BatchPlottingDialog", "TODO anything?", None))

