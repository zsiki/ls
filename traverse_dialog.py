from PyQt4.QtGui import QDialog, QStandardItem, QFont, QListWidgetItem, QMessageBox
from PyQt4.QtCore import Qt
from traverse_calc import Ui_TraverseCalcDialog
from surveying_util import *
from calculation import Calculation
from resultlog import *

class TraverseDialog(QDialog):
    """
        Class for traverse calculation dialog
    """
    def __init__(self):
        super(TraverseDialog, self).__init__()
        self.ui = Ui_TraverseCalcDialog()
        self.ui.setupUi(self)

        # event handlers
        self.ui.ClosedRadio.toggled.connect(self.radioClicked)
        self.ui.LinkRadio.toggled.connect(self.radioClicked)
        self.ui.OpenRadio.toggled.connect(self.radioClicked)
        self.ui.StartPointComboBox.currentIndexChanged.connect(self.startpointComboChanged)
        self.ui.AddButton.clicked.connect(self.onAddButton)
        self.ui.RemoveButton.clicked.connect(self.onRemoveButton)
        self.ui.UpButton.clicked.connect(self.onUpButton)
        self.ui.DownButton.clicked.connect(self.onDownButton)
        self.ui.CalcButton.clicked.connect(self.onCalcButton)
        self.ui.ResetButton.clicked.connect(self.onResetButton)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)
        self.ui.TargetList.setSortingEnabled(True)

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
        self.ui.buttonGroup.setExclusive(False)
        self.ui.ClosedRadio.setChecked(False)
        self.ui.LinkRadio.setChecked(False)
        self.ui.OpenRadio.setChecked(False)
        self.ui.buttonGroup.setExclusive(True)

        # disable widgets
        self.ui.StartPointComboBox.setEnabled(False)
        self.ui.EndPointComboBox.setEnabled(False)

        # clear widgets
        self.ui.StartPointComboBox.clear()
        self.ui.EndPointComboBox.clear()
        self.ui.TargetList.clear()
        self.ui.OrderList.clear()
        self.ui.ResultTextBrowser.clear()

    def fillStationCombos(self):
        """
            Change dialog controls when an other calculation type selected.
        """
        # get selected stations
        oldStation1 = self.ui.StartPointComboBox.itemData( self.ui.StartPointComboBox.currentIndex() )
        oldStation2 = self.ui.EndPointComboBox.itemData( self.ui.EndPointComboBox.currentIndex() )
        # clear station combos
        self.ui.StartPointComboBox.clear()
        self.ui.EndPointComboBox.clear()
        self.ui.StartPointComboBox.setEnabled(False)
        self.ui.EndPointComboBox.setEnabled(False)

        #get combobox models
        combomodel1 = self.ui.StartPointComboBox.model()
        combomodel2 = self.ui.EndPointComboBox.model()

        #get stations        
        known_stations = get_stations(True,False)
        oriented_stations = get_stations(True,True)

        # fill StartPointComboBox and EndPointComboBox
        start_points = []      
        end_points = []      

        if oriented_stations is not None and self.ui.ClosedRadio.isChecked():
            for stn in oriented_stations:
                start_points.append( [u"%s (%s:%s)"% (stn[0],stn[1],stn[2]), stn] )
                end_points.append( [u"%s (%s:%s)"% (stn[0],stn[1],stn[2]), stn] )
            self.ui.StartPointComboBox.setEnabled(True)
        elif known_stations is not None and self.ui.LinkRadio.isChecked():
            for stn in known_stations:
                start_points.append( [u"%s (%s:%s)"% (stn[0],stn[1],stn[2]), stn] )
                end_points.append( [u"%s (%s:%s)"% (stn[0],stn[1],stn[2]), stn] )
            self.ui.StartPointComboBox.setEnabled(True)
            self.ui.EndPointComboBox.setEnabled(True)
        elif oriented_stations is not None and self.ui.OpenRadio.isChecked():
            for stn in oriented_stations:
                start_points.append( [u"%s (%s:%s)"% (stn[0],stn[1],stn[2]), stn] )
            self.ui.StartPointComboBox.setEnabled(True)

        known_points = get_known()
        if start_points is not None:
            for startpoint in start_points:
                item = QStandardItem(startpoint[0])
                item.setData(startpoint[1],Qt.UserRole)
                if known_points is not None and startpoint[1][0] in known_points:
                    itemfont = item.font()
                    itemfont.setWeight(QFont.Bold)
                    item.setFont(itemfont)
                combomodel1.appendRow( item )
        if end_points is not None:
            for endpoint in end_points:
                item = QStandardItem(endpoint[0])
                item.setData(endpoint[1],Qt.UserRole)
                if known_points is not None and endpoint[1][0] in known_points:
                    itemfont = item.font()
                    itemfont.setWeight(QFont.Bold)
                    item.setFont(itemfont)
                combomodel2.appendRow( item )
                
        # select previously selected start/end point if present in the list
        self.ui.StartPointComboBox.setCurrentIndex( self.ui.StartPointComboBox.findData(oldStation1) )
        self.ui.EndPointComboBox.setCurrentIndex( self.ui.EndPointComboBox.findData(oldStation2) )
        
        # in case of closed traverse ens point must be the same as start point
        if self.ui.ClosedRadio.isChecked():
            self.ui.EndPointComboBox.setCurrentIndex(self.ui.StartPointComboBox.currentIndex())
    
    def fillTargetList(self):
        """
            Change dialog controls when an other calculation type selected.
        """
        self.ui.TargetList.clear()
        self.ui.OrderList.clear()
        # get target points
        targets = get_stations(False,False)
        # fill target list widget
        known_list = get_known()
        if targets is not None:
            for target in targets:
                item = QListWidgetItem(u"%s (%s:%s)"% (target[0],target[1],target[2]) )
                item.setData(Qt.UserRole,target)
                if known_list is not None and target[0] in known_list:
                    itemfont = item.font()
                    itemfont.setWeight(QFont.Bold)
                    item.setFont(itemfont)
                self.ui.TargetList.addItem( item )
    
    def radioClicked(self):
        """
            Change dialog controls when an other calculation type selected.
        """
        self.fillStationCombos()
        self.fillTargetList()
        
    def startpointComboChanged(self):
        if self.ui.ClosedRadio.isChecked():
            self.ui.EndPointComboBox.setCurrentIndex(self.ui.StartPointComboBox.currentIndex())

    def onAddButton(self):
        """
            Add selected target point to used points list.
        """
        self.ui.OrderList.addItem( self.ui.TargetList.takeItem( self.ui.TargetList.currentRow() ) )

    def onRemoveButton(self):
        """
            Remove selected used point and add to target points list.
        """
        self.ui.TargetList.addItem( self.ui.OrderList.takeItem( self.ui.OrderList.currentRow() ) )

    def onUpButton(self):
        """
            Add selected target point to used points list.
        """
        cur = self.ui.OrderList.currentRow()
        if cur>0:
            self.ui.OrderList.insertItem( cur-1, self.ui.OrderList.takeItem( cur ) )
            self.ui.OrderList.setCurrentRow(cur-1)

    def onDownButton(self):
        """
            Add selected target point to used points list.
        """
        cur = self.ui.OrderList.currentRow()
        if cur<self.ui.OrderList.count()-1:
            self.ui.OrderList.insertItem( cur+1, self.ui.OrderList.takeItem( cur ) )
            self.ui.OrderList.setCurrentRow(cur+1)

    def onCalcButton(self):
        """
            Start a calculation when the Calculate button pushed.
        """
        if self.ui.buttonGroup.checkedId() == -1:
            QMessageBox.warning(self,u"Warning",u"Select the type of traverse line!")
            return

        # get the selected stations
        stn1 = self.ui.StartPointComboBox.itemData( self.ui.StartPointComboBox.currentIndex() )
        if stn1 is None:
            QMessageBox.warning(self,u"Warning",u"Select start point!")
            self.ui.StartPointComboBox.setFocus()
            return
        stn2 = self.ui.EndPointComboBox.itemData( self.ui.EndPointComboBox.currentIndex() )
        if stn2 is None and not self.ui.OpenRadio.isChecked():
            QMessageBox.warning(self,u"Warning",u"Select end point!")
            self.ui.EndPointComboBox.setFocus()
            return
        if self.ui.OrderList.count()==0:
            QMessageBox.warning(self,u"Warning",u"Add points to angle point list!")
            self.ui.OrderList.setFocus()
            return
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
