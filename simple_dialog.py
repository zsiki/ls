from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QObject
# debugging
from PyQt4.QtCore import pyqtRemoveInputHook
import pdb

from simple_calc import Ui_SimpleCalcDialog
from surveying_util import *
from calculation import Calculation

class SimpleDialog(QDialog):
    """
        Class for single point calculation dialog (intersection, resection, ...)
    """
    def __init__(self):
        super(SimpleDialog, self).__init__()
        self.ui = Ui_SimpleCalcDialog()
        self.ui.setupUi(self)
        # event handlers
        self.ui.OrientRadio.toggled.connect(self.orient_clicked)
        self.ui.CalcButton.clicked.connect(self.onCalcButton)
        self.ui.ResetButton.clicked.connect(self.onResetButton)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)

    def showEvent(self, event):
        """
            Reset dialog to initial state
        """
        self.reset()

    def reset(self):
        # reset radio buttons
        self.ui.OrientRadio.setChecked(False)
        self.ui.RadialRadio.setChecked(False)
        self.ui.IntersectRadio.setChecked(False)
        self.ui.ResectionRadio.setChecked(False)
        self.ui.FreeRadio.setChecked(False)
        # reset result text
        self.ui.TextBrowser.clear()

    def orient_clicked(self, enabled):
        """
            Change dialog controls for orientation
            :param enable: True/False (Bool)
        """
        if enabled:
            self.ui.TextBrowser.append('orient')
            # fill station1 combo
            self.ui.Station1Combo.clear()
            st = get_stations(True)
            if st is not None:
                for s in st:
                    self.ui.Station1Combo.addItem(s[0])
            self.ui.Station2Combo.clear()

    def initDialog(self):
        self.reset()
        #self.ui.Station1Combo.clear()
        #self.ui.Station2Combo.clear()
        #stations = get_stations()
        #if stations is not None:
        #    for stn in stations:
        #        self.ui.Station1Combo.addItem( stn[0] )
        #        self.ui.Station2Combo.addItem( stn[0] )
        
    def onCalcButton(self):
        if self.ui.OrientRadio.isChecked():
            #Calculation.orientation(None, None)
            pass
        elif self.ui.RadialRadio.isChecked():
            #Calculation.polarpoint(None, None)
            pass
        elif self.ui.IntersectRadio.isChecked():
            #Calculation.intersection(None, None, None, None)
            pass
        elif self.ui.ResectionRadio.isChecked():
            #Calculation.resection(None, None, None, None, None, None, None)
            pass
        elif self.ui.FreeRadio.isChecked():
            pass
    
    def onResetButton(self):
        self.initDialog()
        
    def onCloseButton(self):
        self.accept()
