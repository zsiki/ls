from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QObject
# debugging
#from PyQt4.QtCore import pyqtRemoveInputHook
#import pdb
import sys

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
        self.ui.OrientRadio.toggled.connect(self.radio_clicked)
        self.ui.RadialRadio.toggled.connect(self.radio_clicked)
        self.ui.IntersectRadio.toggled.connect(self.radio_clicked)
        self.ui.ResectionRadio.toggled.connect(self.radio_clicked)
        self.ui.FreeRadio.toggled.connect(self.radio_clicked)
        self.ui.CalcButton.clicked.connect(self.onCalcButton)
        self.ui.ResetButton.clicked.connect(self.onResetButton)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)

    def showEvent(self, event):
        """
            Reset dialog when receives a show event.
        """
        self.reset()
        
    def reset(self):
        """
            Reset dialog to initial state
        """
        # reset radio buttons
        self.ui.radioButtonGroup.setExclusive(False)
        self.ui.OrientRadio.setChecked(False)
        self.ui.RadialRadio.setChecked(False)
        self.ui.IntersectRadio.setChecked(False)
        self.ui.ResectionRadio.setChecked(False)
        self.ui.FreeRadio.setChecked(False)
        self.ui.radioButtonGroup.setExclusive(True)

        # disable widgets
        self.ui.Station1Combo.setEnabled(False)
        self.ui.Station2Combo.setEnabled(False)

        # clear widgets
        self.ui.ResultTextBrowser.clear()
        self.ui.Station1Combo.clear()
        self.ui.Station2Combo.clear()

    def radio_clicked(self, enabled):
        """
            Change dialog controls when an other calculation type selected.
            :param enable: True/False (Bool)
        """
        oldStation1 = self.ui.Station1Combo.itemData( self.ui.Station1Combo.currentIndex() )
        oldStation2 = self.ui.Station2Combo.itemData( self.ui.Station2Combo.currentIndex() )
        self.ui.Station1Combo.clear()
        self.ui.Station2Combo.clear()
        self.ui.Station1Combo.setEnabled(False)
        self.ui.Station2Combo.setEnabled(False)
        
        known_stations = get_stations(True)
        all_stations = get_stations(False)
        # fill Station1Combo and Station2Combo      
        if known_stations is not None and (self.ui.OrientRadio.isChecked() or \
                self.ui.RadialRadio.isChecked() or self.ui.IntersectRadio.isChecked()):
            for stn in known_stations:
                self.ui.Station1Combo.addItem( stn[0], stn )
                if self.ui.IntersectRadio.isChecked():
                    self.ui.Station2Combo.addItem( stn[0], stn )
            self.ui.Station1Combo.setEnabled(True)
            if self.ui.IntersectRadio.isChecked():
                self.ui.Station2Combo.setEnabled(True)
        elif all_stations is not None and (self.ui.ResectionRadio.isChecked() or \
                self.ui.FreeRadio.isChecked()):
            self.ui.Station1Combo.setEnabled(True)
            for stn in all_stations:
                self.ui.Station1Combo.addItem( stn[0], stn )
                
        self.ui.Station1Combo.setCurrentIndex( self.ui.Station1Combo.findData(oldStation1) )
        self.ui.Station2Combo.setCurrentIndex( self.ui.Station2Combo.findData(oldStation2) )

    def onCalcButton(self):
        """
            Start a calculation when the Calculate button pushed.
        """
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
        """
            Reset dialog when the Reset button pushed.
        """
        self.reset()
    
    def onCloseButton(self):
        """
            Close the dialog when the Close button pushed.
        """
        self.accept()
