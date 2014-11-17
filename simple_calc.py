# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'simple_calc.ui'
#
# Created: Mon Nov 17 21:18:51 2014
#      by: PyQt4 UI code generator 4.10.3
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

class Ui_SimpleCalcDialog(object):
    def setupUi(self, SimpleCalcDialog):
        SimpleCalcDialog.setObjectName(_fromUtf8("SimpleCalcDialog"))
        SimpleCalcDialog.resize(744, 408)
        self.ResetButton = QtGui.QPushButton(SimpleCalcDialog)
        self.ResetButton.setGeometry(QtCore.QRect(540, 370, 91, 23))
        self.ResetButton.setObjectName(_fromUtf8("ResetButton"))
        self.CloseButton = QtGui.QPushButton(SimpleCalcDialog)
        self.CloseButton.setGeometry(QtCore.QRect(650, 370, 75, 23))
        self.CloseButton.setObjectName(_fromUtf8("CloseButton"))
        self.HelpButton = QtGui.QPushButton(SimpleCalcDialog)
        self.HelpButton.setGeometry(QtCore.QRect(10, 370, 75, 23))
        self.HelpButton.setObjectName(_fromUtf8("HelpButton"))
        self.RadioGroup = QtGui.QGroupBox(SimpleCalcDialog)
        self.RadioGroup.setGeometry(QtCore.QRect(0, 0, 141, 211))
        self.RadioGroup.setFlat(False)
        self.RadioGroup.setCheckable(False)
        self.RadioGroup.setObjectName(_fromUtf8("RadioGroup"))
        self.OrientRadio = QtGui.QRadioButton(self.RadioGroup)
        self.OrientRadio.setGeometry(QtCore.QRect(10, 30, 151, 17))
        self.OrientRadio.setObjectName(_fromUtf8("OrientRadio"))
        self.radioButtonGroup = QtGui.QButtonGroup(SimpleCalcDialog)
        self.radioButtonGroup.setObjectName(_fromUtf8("radioButtonGroup"))
        self.radioButtonGroup.addButton(self.OrientRadio)
        self.RadialRadio = QtGui.QRadioButton(self.RadioGroup)
        self.RadialRadio.setGeometry(QtCore.QRect(10, 60, 161, 17))
        self.RadialRadio.setObjectName(_fromUtf8("RadialRadio"))
        self.radioButtonGroup.addButton(self.RadialRadio)
        self.IntersectRadio = QtGui.QRadioButton(self.RadioGroup)
        self.IntersectRadio.setGeometry(QtCore.QRect(10, 90, 151, 17))
        self.IntersectRadio.setObjectName(_fromUtf8("IntersectRadio"))
        self.radioButtonGroup.addButton(self.IntersectRadio)
        self.ResectionRadio = QtGui.QRadioButton(self.RadioGroup)
        self.ResectionRadio.setGeometry(QtCore.QRect(10, 120, 141, 17))
        self.ResectionRadio.setObjectName(_fromUtf8("ResectionRadio"))
        self.radioButtonGroup.addButton(self.ResectionRadio)
        self.FreeRadio = QtGui.QRadioButton(self.RadioGroup)
        self.FreeRadio.setGeometry(QtCore.QRect(10, 150, 141, 17))
        self.FreeRadio.setObjectName(_fromUtf8("FreeRadio"))
        self.radioButtonGroup.addButton(self.FreeRadio)
        self.PointsGroup = QtGui.QGroupBox(SimpleCalcDialog)
        self.PointsGroup.setGeometry(QtCore.QRect(300, 0, 441, 211))
        self.PointsGroup.setObjectName(_fromUtf8("PointsGroup"))
        self.AddButton = QtGui.QPushButton(self.PointsGroup)
        self.AddButton.setGeometry(QtCore.QRect(140, 50, 81, 23))
        self.AddButton.setObjectName(_fromUtf8("AddButton"))
        self.AddAllButton = QtGui.QPushButton(self.PointsGroup)
        self.AddAllButton.setGeometry(QtCore.QRect(140, 80, 81, 23))
        self.AddAllButton.setObjectName(_fromUtf8("AddAllButton"))
        self.TargetList = QtGui.QListView(self.PointsGroup)
        self.TargetList.setGeometry(QtCore.QRect(230, 40, 121, 131))
        self.TargetList.setObjectName(_fromUtf8("TargetList"))
        self.RemoveButton = QtGui.QPushButton(self.PointsGroup)
        self.RemoveButton.setGeometry(QtCore.QRect(140, 110, 81, 23))
        self.RemoveButton.setObjectName(_fromUtf8("RemoveButton"))
        self.RemoveAllButton = QtGui.QPushButton(self.PointsGroup)
        self.RemoveAllButton.setGeometry(QtCore.QRect(140, 140, 81, 23))
        self.RemoveAllButton.setObjectName(_fromUtf8("RemoveAllButton"))
        self.label_9 = QtGui.QLabel(self.PointsGroup)
        self.label_9.setGeometry(QtCore.QRect(10, 20, 121, 16))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.label_10 = QtGui.QLabel(self.PointsGroup)
        self.label_10.setGeometry(QtCore.QRect(230, 20, 121, 16))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.SourceList = QtGui.QListView(self.PointsGroup)
        self.SourceList.setGeometry(QtCore.QRect(10, 40, 121, 131))
        self.SourceList.setObjectName(_fromUtf8("SourceList"))
        self.ResultGroup = QtGui.QGroupBox(SimpleCalcDialog)
        self.ResultGroup.setGeometry(QtCore.QRect(0, 180, 741, 201))
        self.ResultGroup.setObjectName(_fromUtf8("ResultGroup"))
        self.TextBrowser = QtGui.QTextBrowser(self.ResultGroup)
        self.TextBrowser.setEnabled(False)
        self.TextBrowser.setGeometry(QtCore.QRect(10, 20, 721, 161))
        self.TextBrowser.setObjectName(_fromUtf8("TextBrowser"))
        self.StationGroup = QtGui.QGroupBox(SimpleCalcDialog)
        self.StationGroup.setGeometry(QtCore.QRect(150, 0, 141, 211))
        self.StationGroup.setObjectName(_fromUtf8("StationGroup"))
        self.Station1Combo = QtGui.QComboBox(self.StationGroup)
        self.Station1Combo.setGeometry(QtCore.QRect(10, 50, 121, 22))
        self.Station1Combo.setObjectName(_fromUtf8("Station1Combo"))
        self.label_7 = QtGui.QLabel(self.StationGroup)
        self.label_7.setGeometry(QtCore.QRect(10, 20, 71, 16))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.label_8 = QtGui.QLabel(self.StationGroup)
        self.label_8.setGeometry(QtCore.QRect(10, 90, 71, 16))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.Station2Combo = QtGui.QComboBox(self.StationGroup)
        self.Station2Combo.setGeometry(QtCore.QRect(10, 120, 121, 22))
        self.Station2Combo.setObjectName(_fromUtf8("Station2Combo"))
        self.CalcButton = QtGui.QPushButton(SimpleCalcDialog)
        self.CalcButton.setGeometry(QtCore.QRect(450, 370, 75, 23))
        self.CalcButton.setObjectName(_fromUtf8("CalcButton"))

        self.retranslateUi(SimpleCalcDialog)
        QtCore.QMetaObject.connectSlotsByName(SimpleCalcDialog)

    def retranslateUi(self, SimpleCalcDialog):
        SimpleCalcDialog.setWindowTitle(_translate("SimpleCalcDialog", "Simple Point Calculations", None))
        self.ResetButton.setText(_translate("SimpleCalcDialog", "Reset", None))
        self.CloseButton.setText(_translate("SimpleCalcDialog", "Close", None))
        self.HelpButton.setText(_translate("SimpleCalcDialog", "Help", None))
        self.RadioGroup.setTitle(_translate("SimpleCalcDialog", "Calculation", None))
        self.OrientRadio.setToolTip(_translate("SimpleCalcDialog", "Calculate orientation angle  on stations", None))
        self.OrientRadio.setText(_translate("SimpleCalcDialog", "Orientation", None))
        self.RadialRadio.setText(_translate("SimpleCalcDialog", "Radial Survey", None))
        self.IntersectRadio.setText(_translate("SimpleCalcDialog", "Intersection", None))
        self.ResectionRadio.setText(_translate("SimpleCalcDialog", "Resection", None))
        self.FreeRadio.setText(_translate("SimpleCalcDialog", "Free Station", None))
        self.PointsGroup.setTitle(_translate("SimpleCalcDialog", "Points", None))
        self.AddButton.setText(_translate("SimpleCalcDialog", "Add >", None))
        self.AddAllButton.setText(_translate("SimpleCalcDialog", "Add all", None))
        self.RemoveButton.setText(_translate("SimpleCalcDialog", "< Remove", None))
        self.RemoveAllButton.setText(_translate("SimpleCalcDialog", "Remove all", None))
        self.label_9.setText(_translate("SimpleCalcDialog", "Target Points", None))
        self.label_10.setText(_translate("SimpleCalcDialog", "Used Points", None))
        self.ResultGroup.setTitle(_translate("SimpleCalcDialog", "Result of Calculations", None))
        self.StationGroup.setTitle(_translate("SimpleCalcDialog", "Station", None))
        self.label_7.setText(_translate("SimpleCalcDialog", "Station (1)", None))
        self.label_8.setText(_translate("SimpleCalcDialog", "Station (2)", None))
        self.CalcButton.setText(_translate("SimpleCalcDialog", "Calculate", None))

