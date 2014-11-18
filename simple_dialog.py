from PyQt4.QtGui import QDialog, QListWidgetItem
from PyQt4.QtCore import Qt, QVariant
# debugging
#from PyQt4.QtCore import pyqtRemoveInputHook
#import pdb
#import sys
#sys.path.append(r'C:\Program Files\eclipse-standard-luna-R-win32-x86_64\eclipse\plugins\org.python.pydev_3.8.0.201409251235\pysrc')
#import pydevd

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
        self.ui.OrientRadio.toggled.connect(self.radioClicked)
        self.ui.RadialRadio.toggled.connect(self.radioClicked)
        self.ui.IntersectRadio.toggled.connect(self.radioClicked)
        self.ui.ResectionRadio.toggled.connect(self.radioClicked)
        self.ui.FreeRadio.toggled.connect(self.radioClicked)
        self.ui.Station1Combo.currentIndexChanged.connect(self.stationComboChanged)
        self.ui.Station2Combo.currentIndexChanged.connect(self.stationComboChanged)
        self.ui.CalcButton.clicked.connect(self.onCalcButton)
        self.ui.ResetButton.clicked.connect(self.onResetButton)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)

    def showEvent(self, event):
        """
            Reset dialog when receives a show event.
        """
        #pydevd.settrace()
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
        self.ui.Station1Combo.clear()
        self.ui.Station2Combo.clear()
        self.ui.SourceList.clear()
        self.ui.TargetList.clear()
        self.ui.ResultTextBrowser.clear()

    def fillStationCombos(self):
        """
            Change dialog controls when an other calculation type selected.
        """
        # get selected stations
        oldStation1 = self.ui.Station1Combo.itemData( self.ui.Station1Combo.currentIndex() )
        oldStation2 = self.ui.Station2Combo.itemData( self.ui.Station2Combo.currentIndex() )
        # clear station combos
        self.ui.Station1Combo.clear()
        self.ui.Station2Combo.clear()
        self.ui.Station1Combo.setEnabled(False)
        self.ui.Station2Combo.setEnabled(False)

        #get stations        
        known_stations = get_stations(True)
        all_stations = get_stations(False)
        # fill Station1Combo and Station2Combo      
        if known_stations is not None and (self.ui.OrientRadio.isChecked() or \
                self.ui.RadialRadio.isChecked() or self.ui.IntersectRadio.isChecked()):
            for stn in known_stations:
                self.ui.Station1Combo.addItem( u"%s (%s:%s)"% (stn[0],stn[1],stn[2]), stn )
                if self.ui.IntersectRadio.isChecked():
                    self.ui.Station2Combo.addItem( u"%s (%s:%s)"% (stn[0],stn[1],stn[2]), stn )
            self.ui.Station1Combo.setEnabled(True)
            if self.ui.IntersectRadio.isChecked():
                self.ui.Station2Combo.setEnabled(True)
        elif all_stations is not None and (self.ui.ResectionRadio.isChecked() or \
                self.ui.FreeRadio.isChecked()):
            self.ui.Station1Combo.setEnabled(True)
            for stn in all_stations:
                self.ui.Station1Combo.addItem( u"%s (%s:%s)"% (stn[0],stn[1],stn[2]), stn )
                
        # select previously selected stations if present in the list
        self.ui.Station1Combo.setCurrentIndex( self.ui.Station1Combo.findData(oldStation1) )
        self.ui.Station2Combo.setCurrentIndex( self.ui.Station2Combo.findData(oldStation2) )
        
    def fillSourceList(self):
        """
            Change dialog controls when an other calculation type selected.
        """
        # get the selected stations
        stn1 = self.ui.Station1Combo.itemData( self.ui.Station1Combo.currentIndex() )
        stn2 = self.ui.Station2Combo.itemData( self.ui.Station2Combo.currentIndex() )
        # clear source and target list
        self.ui.SourceList.clear()
        self.ui.TargetList.clear()
        # get tartget poins according to the stations
        targets = []
        if stn1 is not None and (self.ui.OrientRadio.isChecked() or \
                self.ui.ResectionRadio.isChecked() or self.ui.FreeRadio.isChecked()):
            targets = get_targets(stn1[0], stn1[1], stn1[2],True)
        elif stn1 is not None and self.ui.RadialRadio.isChecked():
            targets = get_targets(stn1[0], stn1[1], stn1[2],False)
        elif stn1 is not None and stn2 is not None and \
                self.ui.IntersectRadio.isChecked():
            targets_stn1 = get_targets(stn1[0], stn1[1], stn1[2],False)
            targets_stn2 = get_targets(stn2[0], stn2[1], stn2[2],False)
            #TODO fill source list for intersection (common points)
            #for t1 in targets_stn1:
            #    for t2 in targets_stn2:
            #        if t1.point_id == t2.point_id:
            #            targets.append(t1)
            
        # fill source list widget
        if targets is not None:
            for target in targets:
                item = QListWidgetItem(u"%s (id:%s)"% (target[0],target[2]) )
                item.setData(Qt.UserRole,target)
                self.ui.SourceList.addItem( item )

    def radioClicked(self):
        """
            Change dialog controls when an other calculation type selected.
        """
        self.fillStationCombos()
        self.fillSourceList()
        
    def stationComboChanged(self):
        """
            Init source and target list when one of two station combobox changed.
        """
        self.fillSourceList()
        
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