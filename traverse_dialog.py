# -*- coding: utf-8 -*-
"""
.. module:: traverse_dialog
    :platform: Linux, Windows
    :synopsis: GUI for traverse calculation

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>
"""
import platform
from PyQt4.QtGui import QDialog, QStandardItem, QFont, QListWidgetItem, QMessageBox
from PyQt4.QtCore import Qt

import config
from traverse_calc import Ui_TraverseCalcDialog
from base_classes import *
from surveying_util import *
from calculation import Calculation
from resultlog import *

class TraverseDialog(QDialog):
    """ Class for traverse calculation dialog
    """
    def __init__(self, log):
        """ Initialize dialog data and event handlers
        """
        super(TraverseDialog, self).__init__()
        self.ui = Ui_TraverseCalcDialog()
        self.ui.setupUi(self)
        self.log = log
        if platform.system() == 'Linux':
            # change font
            self.ui.ResultTextBrowser.setFont(QFont(config.fontname, config.fontsize))

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
        """ Reset dialog when receives a show event.
        """
        self.reset()

    def reset(self):
        """ Reset dialog to initial state
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

    def fillStartEndPointsCombos(self):
        """ Change start and end point combo when an other traversing type selected.
        """
        # get selected stations
        oldStartPoint = self.ui.StartPointComboBox.itemData( self.ui.StartPointComboBox.currentIndex() )
        oldEndPoint = self.ui.EndPointComboBox.itemData( self.ui.EndPointComboBox.currentIndex() )
        # clear combos
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
            self.ui.EndPointComboBox.setEnabled(True)

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
        self.ui.StartPointComboBox.setCurrentIndex( self.ui.StartPointComboBox.findData(oldStartPoint) )
        self.ui.EndPointComboBox.setCurrentIndex( self.ui.EndPointComboBox.findData(oldEndPoint) )
        
        # in case of closed traverse ens point must be the same as start point
        if self.ui.ClosedRadio.isChecked():
            self.ui.EndPointComboBox.setCurrentIndex(self.ui.StartPointComboBox.currentIndex())
    
    def fillTargetList(self):
        """ Change Target List when an other calculation type selected.
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
                
    def fillOpenTraverseEndPoints(self):
        """
            Change End Points combo with target points observed 
            from the last point selected in Order List 
            if open traverse is chosen.
        """
        oldEndPoint = self.ui.EndPointComboBox.itemData( self.ui.EndPointComboBox.currentIndex() )
        # clear combos
        self.ui.EndPointComboBox.clear()
        self.ui.EndPointComboBox.setEnabled(True)
        
        #get last angle point from order list
        if self.ui.OrderList.count() == 0:
            return
        lastp = self.ui.OrderList.item( self.ui.OrderList.count()-1 ).data(Qt.UserRole)
        targets = get_targets(lastp[0], lastp[1], lastp[2])

        # fill end point combo        
        combomodel = self.ui.EndPointComboBox.model()
        known_list = get_known()
        if targets is not None:
            for target in targets:
                item = QStandardItem(u"%s (id:%s)"% (target[0],target[2]))
                item.setData(target,Qt.UserRole)
                if known_list is not None and target[0] in known_list:
                    itemfont = item.font()
                    itemfont.setWeight(QFont.Bold)
                    item.setFont(itemfont)
                combomodel.appendRow( item )

        self.ui.EndPointComboBox.setCurrentIndex( self.ui.EndPointComboBox.findData(oldEndPoint) )
    
    def radioClicked(self):
        """
            Change dialog controls when an other calculation type selected.
        """
        self.fillStartEndPointsCombos()
        self.fillTargetList()
        
    def startpointComboChanged(self):
        if self.ui.ClosedRadio.isChecked():
            self.ui.EndPointComboBox.setCurrentIndex(self.ui.StartPointComboBox.currentIndex())
        if self.ui.OpenRadio.isChecked():
            self.fillOpenTraverseEndPoints()

    def onAddButton(self):
        """
            Add selected target point to used points list.
        """
        self.ui.OrderList.addItem( self.ui.TargetList.takeItem( self.ui.TargetList.currentRow() ) )
        if self.ui.OpenRadio.isChecked():
            self.fillOpenTraverseEndPoints()

    def onRemoveButton(self):
        """
            Remove selected used point and add to target points list.
        """
        self.ui.TargetList.addItem( self.ui.OrderList.takeItem( self.ui.OrderList.currentRow() ) )
        if self.ui.OpenRadio.isChecked():
            self.fillOpenTraverseEndPoints()

    def onUpButton(self):
        """
            Add selected target point to used points list.
        """
        cur = self.ui.OrderList.currentRow()
        if cur>0:
            self.ui.OrderList.insertItem( cur-1, self.ui.OrderList.takeItem( cur ) )
            self.ui.OrderList.setCurrentRow(cur-1)
        if self.ui.OpenRadio.isChecked():
            self.fillOpenTraverseEndPoints()

    def onDownButton(self):
        """
            Add selected target point to used points list.
        """
        cur = self.ui.OrderList.currentRow()
        if cur<self.ui.OrderList.count()-1:
            self.ui.OrderList.insertItem( cur+1, self.ui.OrderList.takeItem( cur ) )
            self.ui.OrderList.setCurrentRow(cur+1)
        if self.ui.OpenRadio.isChecked():
            self.fillOpenTraverseEndPoints()

    def onCalcButton(self):
        """
            Start a traverse calculation when the Calculate button pushed.
        """
        if self.ui.buttonGroup.checkedId() == -1:
            QMessageBox.warning(self, tr("Warning"), tr("Select the type of traverse line!"))
            return

        # get the selected stations
        startpoint = self.ui.StartPointComboBox.itemData( self.ui.StartPointComboBox.currentIndex() )
        if startpoint is None:
            QMessageBox.warning(self, tr("Warning"), tr("Select start point!"))
            self.ui.StartPointComboBox.setFocus()
            return
        endpoint = self.ui.EndPointComboBox.itemData( self.ui.EndPointComboBox.currentIndex() )
        if endpoint is None:
            QMessageBox.warning(self, tr("Warning"), tr("Select end point!"))
            self.ui.EndPointComboBox.setFocus()
            return
        if self.ui.OrderList.count()==0:
            QMessageBox.warning(self, tr("Warning"), tr("Add points to angle point list!"))
            self.ui.OrderList.setFocus()
            return

        # fill stations list
        stations = [startpoint]
        for i in range(self.ui.OrderList.count()):
            station = self.ui.OrderList.item(i).data(Qt.UserRole)
            if i==0 and station == startpoint:
                continue 
            if i==self.ui.OrderList.count()-1 and station == endpoint:
                continue 
            stations.append(station)
        if not self.ui.OpenRadio.isChecked():
            stations.append(endpoint)
            
        # add stations and observations to trav_obs
        trav_obs = []
        for i in range(len(stations)):
            st = get_station(stations[i][0], stations[i][1], stations[i][2])
            targets = get_targets(stations[i][0], stations[i][1], stations[i][2])
            obs1 = None
            obs2 = None
            if targets is not None:
                for target in targets:
                    if i>0 and target[0]==stations[i-1][0]:
                        if obs1 is None:
                            obs1 = get_target(target[0],target[1],target[2])
                        if not self.ui.OpenRadio.isChecked() and (obs2 is not None or i==len(stations)-1):
                            break
                    elif i<len(stations)-1 and target[0]==stations[i+1][0]:
                        if obs2 is None:
                            obs2 = get_target(target[0],target[1],target[2])
                        if obs1 is not None or i==0:
                            break
                    elif self.ui.OpenRadio.isChecked() and i==len(stations)-1 and target[0]==endpoint[0]:
                        if obs2 is None:
                            obs2 = get_target(target[0],target[1],target[2])
                        if obs1 is not None:
                            break
                    
            trav_obs.append([st,obs1,obs2])
            
        # Open Traverse: end point can be selected from end point list
        if self.ui.OpenRadio.isChecked():
            trav_obs.append([Station( Point(endpoint[0]), \
                            PolarObservation(endpoint[0], 'station') ),None,None])
            
            # if end point is a known point -> question
            known_list = get_known()
            if known_list is not None and endpoint[0] in known_list:
                reply = QMessageBox.question(self, tr("Question"), \
                    tr("End point has coordinates.\nAre you sure you want to calculate an open traverse?"), \
                    QMessageBox.Yes, QMessageBox.No)
                if reply == QMessageBox.No:
                    return

        if self.ui.OpenRadio.isChecked():
            plist = Calculation.traverse(trav_obs,True)
        else:
            plist = Calculation.traverse(trav_obs,False)

        if plist is not None:
            #store newly calculated coordinates
            for pt in plist:
                tp = ScPoint(pt.id)
                tp.set_coord(pt)
                tp.store_coord(2)
            traversing_type = self.ui.buttonGroup.checkedButton().text()
            self.ui.ResultTextBrowser.append("\n" + tr("Traversing") + " - %s" % traversing_type)
            self.ui.ResultTextBrowser.append(tr("            bearing    bw dist"))
            self.ui.ResultTextBrowser.append(tr("Point        angle     distance  (dE)     (dN)       dE         dN"))
            self.ui.ResultTextBrowser.append(tr("           correction  fw dist    corrections      Easting    Northing"))
            self.log.write()
            self.log.write_log(tr("Traversing") + " - %s" % traversing_type)
            self.log.write(tr("            bearing    bw dist"))
            self.log.write(tr("Point        angle     distance  (dE)     (dN)       dE         dN"))
            self.log.write(tr("           correction  fw dist    corrections      Easting    Northing"))
            self.ui.ResultTextBrowser.append(ResultLog.resultlog_message)
            self.log.write(ResultLog.resultlog_message)
        else:
            QMessageBox.warning(self, tr("Warning"), tr("Traverse line cannot be calculated!"))
            self.ui.ResultTextBrowser.append(ResultLog.resultlog_message)
            self.log.write(ResultLog.resultlog_message)

    def onResetButton(self):
        """ Reset dialog when the Reset button pushed.
        """
        self.reset()

    def onCloseButton(self):
        """ Close the dialog when the Close button pushed.
        """
        self.accept()
