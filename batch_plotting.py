# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'batch_plotting.ui'
#
# Created: Thu Dec 18 21:22:49 2014
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
        BatchPlottingDialog.resize(291, 413)
        self.TemplateList = QtGui.QListWidget(BatchPlottingDialog)
        self.TemplateList.setGeometry(QtCore.QRect(10, 70, 271, 101))
        self.TemplateList.setObjectName(_fromUtf8("TemplateList"))
        self.TemplateLabel = QtGui.QLabel(BatchPlottingDialog)
        self.TemplateLabel.setGeometry(QtCore.QRect(10, 50, 111, 16))
        self.TemplateLabel.setObjectName(_fromUtf8("TemplateLabel"))
        self.PlotButton = QtGui.QPushButton(BatchPlottingDialog)
        self.PlotButton.setGeometry(QtCore.QRect(50, 380, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PlotButton.sizePolicy().hasHeightForWidth())
        self.PlotButton.setSizePolicy(sizePolicy)
        self.PlotButton.setObjectName(_fromUtf8("PlotButton"))
        self.CloseButton = QtGui.QPushButton(BatchPlottingDialog)
        self.CloseButton.setGeometry(QtCore.QRect(160, 380, 81, 23))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.CloseButton.sizePolicy().hasHeightForWidth())
        self.CloseButton.setSizePolicy(sizePolicy)
        self.CloseButton.setObjectName(_fromUtf8("CloseButton"))
        self.ScaleLabel = QtGui.QLabel(BatchPlottingDialog)
        self.ScaleLabel.setGeometry(QtCore.QRect(10, 180, 111, 21))
        self.ScaleLabel.setObjectName(_fromUtf8("ScaleLabel"))
        self.ScaleCombo = QtGui.QComboBox(BatchPlottingDialog)
        self.ScaleCombo.setGeometry(QtCore.QRect(120, 180, 81, 22))
        self.ScaleCombo.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
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
        self.TempDirButton.setGeometry(QtCore.QRect(200, 50, 81, 21))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TempDirButton.sizePolicy().hasHeightForWidth())
        self.TempDirButton.setSizePolicy(sizePolicy)
        self.TempDirButton.setObjectName(_fromUtf8("TempDirButton"))
        self.LayersLabel = QtGui.QLabel(BatchPlottingDialog)
        self.LayersLabel.setGeometry(QtCore.QRect(10, 10, 111, 21))
        self.LayersLabel.setObjectName(_fromUtf8("LayersLabel"))
        self.LayersComboBox = QtGui.QComboBox(BatchPlottingDialog)
        self.LayersComboBox.setGeometry(QtCore.QRect(120, 10, 161, 22))
        self.LayersComboBox.setInputMethodHints(QtCore.Qt.ImhDigitsOnly)
        self.LayersComboBox.setEditable(False)
        self.LayersComboBox.setObjectName(_fromUtf8("LayersComboBox"))
        self.OutputTab = QtGui.QTabWidget(BatchPlottingDialog)
        self.OutputTab.setGeometry(QtCore.QRect(10, 220, 271, 151))
        self.OutputTab.setObjectName(_fromUtf8("OutputTab"))
        self.toPDF = QtGui.QWidget()
        self.toPDF.setObjectName(_fromUtf8("toPDF"))
        self.OutDirLabel = QtGui.QLabel(self.toPDF)
        self.OutDirLabel.setGeometry(QtCore.QRect(10, 10, 111, 16))
        self.OutDirLabel.setObjectName(_fromUtf8("OutDirLabel"))
        self.OutDirButton = QtGui.QPushButton(self.toPDF)
        self.OutDirButton.setGeometry(QtCore.QRect(220, 30, 31, 21))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.OutDirButton.sizePolicy().hasHeightForWidth())
        self.OutDirButton.setSizePolicy(sizePolicy)
        self.OutDirButton.setObjectName(_fromUtf8("OutDirButton"))
        self.OutDirEdit = QtGui.QLineEdit(self.toPDF)
        self.OutDirEdit.setGeometry(QtCore.QRect(10, 30, 211, 20))
        self.OutDirEdit.setObjectName(_fromUtf8("OutDirEdit"))
        self.PrefixEdit = QtGui.QLineEdit(self.toPDF)
        self.PrefixEdit.setGeometry(QtCore.QRect(10, 80, 241, 20))
        self.PrefixEdit.setObjectName(_fromUtf8("PrefixEdit"))
        self.PrefixLabel = QtGui.QLabel(self.toPDF)
        self.PrefixLabel.setGeometry(QtCore.QRect(10, 60, 221, 16))
        self.PrefixLabel.setObjectName(_fromUtf8("PrefixLabel"))
        self.OutputTab.addTab(self.toPDF, _fromUtf8(""))
        self.toPrinter = QtGui.QWidget()
        self.toPrinter.setObjectName(_fromUtf8("toPrinter"))
        self.OutputTab.addTab(self.toPrinter, _fromUtf8(""))
        self.toComposerView = QtGui.QWidget()
        self.toComposerView.setObjectName(_fromUtf8("toComposerView"))
        self.ComposerLabel = QtGui.QLabel(self.toComposerView)
        self.ComposerLabel.setGeometry(QtCore.QRect(10, 10, 121, 16))
        self.ComposerLabel.setObjectName(_fromUtf8("ComposerLabel"))
        self.ComposerEdit = QtGui.QLineEdit(self.toComposerView)
        self.ComposerEdit.setGeometry(QtCore.QRect(10, 30, 241, 20))
        self.ComposerEdit.setObjectName(_fromUtf8("ComposerEdit"))
        self.OutputTab.addTab(self.toComposerView, _fromUtf8(""))

        self.retranslateUi(BatchPlottingDialog)
        self.ScaleCombo.setCurrentIndex(3)
        self.LayersComboBox.setCurrentIndex(-1)
        self.OutputTab.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(BatchPlottingDialog)
        BatchPlottingDialog.setTabOrder(self.LayersComboBox, self.TempDirButton)
        BatchPlottingDialog.setTabOrder(self.TempDirButton, self.TemplateList)
        BatchPlottingDialog.setTabOrder(self.TemplateList, self.ScaleCombo)
        BatchPlottingDialog.setTabOrder(self.ScaleCombo, self.PlotButton)
        BatchPlottingDialog.setTabOrder(self.PlotButton, self.CloseButton)

    def retranslateUi(self, BatchPlottingDialog):
        BatchPlottingDialog.setWindowTitle(_translate("BatchPlottingDialog", "Batch Plotting", None))
        self.TemplateLabel.setText(_translate("BatchPlottingDialog", "Available templates:", None))
        self.PlotButton.setText(_translate("BatchPlottingDialog", "Plot", None))
        self.CloseButton.setText(_translate("BatchPlottingDialog", "Close", None))
        self.ScaleLabel.setText(_translate("BatchPlottingDialog", "Map Scale:", None))
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
        self.LayersLabel.setText(_translate("BatchPlottingDialog", "Polygon layers:", None))
        self.OutDirLabel.setText(_translate("BatchPlottingDialog", "Output Directory:", None))
        self.OutDirButton.setText(_translate("BatchPlottingDialog", "...", None))
        self.PrefixLabel.setText(_translate("BatchPlottingDialog", "Fiename prefix: [prefix]_0001.pdf)", None))
        self.OutputTab.setTabText(self.OutputTab.indexOf(self.toPDF), _translate("BatchPlottingDialog", "To PDF", None))
        self.OutputTab.setTabText(self.OutputTab.indexOf(self.toPrinter), _translate("BatchPlottingDialog", "To Printer", None))
        self.ComposerLabel.setText(_translate("BatchPlottingDialog", "Composer name:", None))
        self.OutputTab.setTabText(self.OutputTab.indexOf(self.toComposerView), _translate("BatchPlottingDialog", "To Composer View", None))

