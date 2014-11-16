from PyQt4.QtGui import QDialog
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

        self.ui.CalcButton.clicked.connect(self.onCalcButton)
        self.ui.ResetButton.clicked.connect(self.onResetButton)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)

    def initDialog(self):
        self.ui.Station1Combo.clear()
        self.ui.Station2Combo.clear()
        stations = get_stations()
        if stations is not None:
            for stn in stations:
                self.ui.Station1Combo.addItem( stn[0] )
                self.ui.Station2Combo.addItem( stn[0] )
        
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
