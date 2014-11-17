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
        self.ui.OrientRadio.toggled.connect(self.reset)
        self.ui.RadialRadio.toggled.connect(self.reset)
        self.ui.IntersectRadio.toggled.connect(self.reset)
        self.ui.ResectionRadio.toggled.connect(self.reset)
        self.ui.FreeRadio.toggled.connect(self.reset)
        self.ui.CalcButton.clicked.connect(self.onCalcButton)
        self.ui.ResetButton.clicked.connect(self.reset)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)

    def showEvent(self, event):
        """
            Reset dialog to initial state
        """
        self.reset()
        
    def reset(self):
        # reset radio buttons
        #pyqtRemoveInputHook()
        #pdb.set_trace()
        
        self.ui.OrientRadio.setChecked(False)
        self.ui.RadialRadio.setChecked(False)
        self.ui.IntersectRadio.setChecked(False)
        self.ui.ResectionRadio.setChecked(False)
        self.ui.FreeRadio.setChecked(False)
        self.ui.Station1Combo.setEnabled(False)
        self.ui.Station2Combo.setEnabled(False)

        # reset result text
        self.ui.TextBrowser.clear()

        known_stations = get_stations(True)
        all_stations = get_stations(False)
        # fill Station1Combo and Station2Combo      
        self.ui.Station1Combo.clear()
        self.ui.Station2Combo.clear()
        if known_stations is not None and (self.ui.OrientRadio.isChecked() or \
                self.ui.RadialRadio.isChecked() or self.ui.IntersectRadio.isChecked()):
            for stn in known_stations:
                self.ui.Station1Combo.addItem( stn[0] )
                if self.ui.IntersectRadio.isChecked():
                    self.ui.Station2Combo.addItem( stn[0] )
            self.ui.Station1Combo.setEnabled(True)
            if self.ui.IntersectRadio.isChecked():
                self.ui.Station2Combo.setEnabled(True)
        elif all_stations is not None and (self.ui.ResectionRadio.isChecked() or \
                self.ui.FreeRadio.isChecked()):
            self.ui.Station1Combo.setEnabled(True)
            for stn in all_stations:
                self.ui.Station1Combo.addItem( stn[0] )

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
        self.reset()
    
    def onCloseButton(self):
        self.accept()
