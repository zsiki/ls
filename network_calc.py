# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'network_calc.ui'
#
# Created: Tue Nov 11 17:30:59 2014
#      by: PyQt4 UI code generator 4.8.6
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_NetworkCalcDialog(object):
    def setupUi(self, NetworkCalcDialog):
        NetworkCalcDialog.setObjectName(_fromUtf8("NetworkCalcDialog"))
        NetworkCalcDialog.resize(537, 531)
        NetworkCalcDialog.setWindowTitle(_fromUtf8("Network Adjustment"))
        NetworkCalcDialog.setAccessibleName(_fromUtf8(""))
        NetworkCalcDialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        self.Points_GroupBox = QtGui.QGroupBox(NetworkCalcDialog)
        self.Points_GroupBox.setGeometry(QtCore.QRect(10, 10, 521, 311))
        self.Points_GroupBox.setTitle(QtGui.QApplication.translate("NetworkCalcDialog", "Points", None, QtGui.QApplication.UnicodeUTF8))
        self.Points_GroupBox.setObjectName(_fromUtf8("Points_GroupBox"))
        self.Points_ListView = QtGui.QListView(self.Points_GroupBox)
        self.Points_ListView.setGeometry(QtCore.QRect(20, 40, 121, 261))
        self.Points_ListView.setObjectName(_fromUtf8("Points_ListView"))
        self.AddFix_PushButton = QtGui.QPushButton(self.Points_GroupBox)
        self.AddFix_PushButton.setGeometry(QtCore.QRect(160, 50, 81, 23))
        self.AddFix_PushButton.setText(QtGui.QApplication.translate("NetworkCalcDialog", "Add >", None, QtGui.QApplication.UnicodeUTF8))
        self.AddFix_PushButton.setObjectName(_fromUtf8("AddFix_PushButton"))
        self.AddAdj_PushButton = QtGui.QPushButton(self.Points_GroupBox)
        self.AddAdj_PushButton.setGeometry(QtCore.QRect(160, 200, 81, 23))
        self.AddAdj_PushButton.setText(QtGui.QApplication.translate("NetworkCalcDialog", "Add >", None, QtGui.QApplication.UnicodeUTF8))
        self.AddAdj_PushButton.setObjectName(_fromUtf8("AddAdj_PushButton"))
        self.FixPoints_ListView = QtGui.QListView(self.Points_GroupBox)
        self.FixPoints_ListView.setGeometry(QtCore.QRect(260, 40, 121, 111))
        self.FixPoints_ListView.setObjectName(_fromUtf8("FixPoints_ListView"))
        self.RemoveFix_PushButton = QtGui.QPushButton(self.Points_GroupBox)
        self.RemoveFix_PushButton.setGeometry(QtCore.QRect(160, 90, 81, 23))
        self.RemoveFix_PushButton.setText(QtGui.QApplication.translate("NetworkCalcDialog", "< Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.RemoveFix_PushButton.setObjectName(_fromUtf8("RemoveFix_PushButton"))
        self.ListPoints_Label = QtGui.QLabel(self.Points_GroupBox)
        self.ListPoints_Label.setGeometry(QtCore.QRect(20, 20, 121, 16))
        self.ListPoints_Label.setText(QtGui.QApplication.translate("NetworkCalcDialog", "List of Points", None, QtGui.QApplication.UnicodeUTF8))
        self.ListPoints_Label.setObjectName(_fromUtf8("ListPoints_Label"))
        self.FixPoints_Label = QtGui.QLabel(self.Points_GroupBox)
        self.FixPoints_Label.setGeometry(QtCore.QRect(260, 20, 121, 16))
        self.FixPoints_Label.setText(QtGui.QApplication.translate("NetworkCalcDialog", "Fix Points", None, QtGui.QApplication.UnicodeUTF8))
        self.FixPoints_Label.setObjectName(_fromUtf8("FixPoints_Label"))
        self.Calculate_PushButton = QtGui.QPushButton(self.Points_GroupBox)
        self.Calculate_PushButton.setGeometry(QtCore.QRect(410, 270, 91, 23))
        self.Calculate_PushButton.setText(QtGui.QApplication.translate("NetworkCalcDialog", "Calculate", None, QtGui.QApplication.UnicodeUTF8))
        self.Calculate_PushButton.setObjectName(_fromUtf8("Calculate_PushButton"))
        self.RemoveAdj_PushButton = QtGui.QPushButton(self.Points_GroupBox)
        self.RemoveAdj_PushButton.setGeometry(QtCore.QRect(160, 240, 81, 23))
        self.RemoveAdj_PushButton.setText(QtGui.QApplication.translate("NetworkCalcDialog", "< Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.RemoveAdj_PushButton.setObjectName(_fromUtf8("RemoveAdj_PushButton"))
        self.AdjPoints_ListView = QtGui.QListView(self.Points_GroupBox)
        self.AdjPoints_ListView.setGeometry(QtCore.QRect(260, 190, 121, 111))
        self.AdjPoints_ListView.setObjectName(_fromUtf8("AdjPoints_ListView"))
        self.AdjPoints_Label = QtGui.QLabel(self.Points_GroupBox)
        self.AdjPoints_Label.setGeometry(QtCore.QRect(260, 170, 141, 16))
        self.AdjPoints_Label.setText(QtGui.QApplication.translate("NetworkCalcDialog", "Adjustment Points", None, QtGui.QApplication.UnicodeUTF8))
        self.AdjPoints_Label.setObjectName(_fromUtf8("AdjPoints_Label"))
        self.Reset_PushButton = QtGui.QPushButton(NetworkCalcDialog)
        self.Reset_PushButton.setGeometry(QtCore.QRect(340, 500, 81, 23))
        self.Reset_PushButton.setText(QtGui.QApplication.translate("NetworkCalcDialog", "Reset", None, QtGui.QApplication.UnicodeUTF8))
        self.Reset_PushButton.setObjectName(_fromUtf8("Reset_PushButton"))
        self.Close_PushButton = QtGui.QPushButton(NetworkCalcDialog)
        self.Close_PushButton.setGeometry(QtCore.QRect(440, 500, 75, 23))
        self.Close_PushButton.setText(QtGui.QApplication.translate("NetworkCalcDialog", "Close", None, QtGui.QApplication.UnicodeUTF8))
        self.Close_PushButton.setObjectName(_fromUtf8("Close_PushButton"))
        self.Result_GroupBox = QtGui.QGroupBox(NetworkCalcDialog)
        self.Result_GroupBox.setGeometry(QtCore.QRect(10, 330, 521, 161))
        self.Result_GroupBox.setTitle(QtGui.QApplication.translate("NetworkCalcDialog", "Result of Calculations", None, QtGui.QApplication.UnicodeUTF8))
        self.Result_GroupBox.setObjectName(_fromUtf8("Result_GroupBox"))
        self.Result_TextBrowser = QtGui.QTextBrowser(self.Result_GroupBox)
        self.Result_TextBrowser.setGeometry(QtCore.QRect(10, 20, 501, 131))
        self.Result_TextBrowser.setObjectName(_fromUtf8("Result_TextBrowser"))
        self.Help_PushButton = QtGui.QPushButton(NetworkCalcDialog)
        self.Help_PushButton.setGeometry(QtCore.QRect(20, 500, 75, 23))
        self.Help_PushButton.setText(QtGui.QApplication.translate("NetworkCalcDialog", "Help", None, QtGui.QApplication.UnicodeUTF8))
        self.Help_PushButton.setObjectName(_fromUtf8("Help_PushButton"))

        self.retranslateUi(NetworkCalcDialog)
        QtCore.QMetaObject.connectSlotsByName(NetworkCalcDialog)

    def retranslateUi(self, NetworkCalcDialog):
        pass

