# -*- coding: utf-8 -*-
"""
.. module:: single_dialog
    :platform: Linux, Windows
    :synopsis: GUI for single point calculations

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>
"""
import platform
import webbrowser
from PyQt4.QtGui import QDialog, QListWidgetItem, QFont, QMessageBox, \
    QStandardItem
from PyQt4.QtCore import Qt, QSettings

import config
from single_calc import Ui_SingleCalcDialog
from base_classes import *
from surveying_util import *
from calculation import Calculation
from resultlog import *
from gama_interface import *

class SingleDialog(QDialog):
    """ Class for single point calculation dialog (intersection, resection, ...)
    """
    def __init__(self, log):
        """ Initialize dialog data and event handlers
        """
        super(SingleDialog, self).__init__()
        self.ui = Ui_SingleCalcDialog()
        self.ui.setupUi(self)
        self.log = log

        # event handlers
        self.ui.OrientRadio.toggled.connect(self.radioClicked)
        self.ui.RadialRadio.toggled.connect(self.radioClicked)
        self.ui.IntersectRadio.toggled.connect(self.radioClicked)
        self.ui.ResectionRadio.toggled.connect(self.radioClicked)
        self.ui.FreeRadio.toggled.connect(self.radioClicked)
        self.ui.Station1Combo.currentIndexChanged.connect(self.stationComboChanged)
        self.ui.Station2Combo.currentIndexChanged.connect(self.stationComboChanged)
        self.ui.AddButton.clicked.connect(self.onAddButton)
        self.ui.AddAllButton.clicked.connect(self.onAddAllButton)
        self.ui.RemoveButton.clicked.connect(self.onRemoveButton)
        self.ui.RemoveAllButton.clicked.connect(self.onRemoveAllButton)
        self.ui.CalcButton.clicked.connect(self.onCalcButton)
        self.ui.ResetButton.clicked.connect(self.onResetButton)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)
        self.ui.HelpButton.clicked.connect(self.onHelpButton)
        self.ui.SourceList.setSortingEnabled(True)

    def showEvent(self, event):
        """ Reset dialog when receives a show event.

            :param event: NOT USED
        """
        if platform.system() == 'Linux':
            # change font
            fontname = QSettings().value("SurveyingCalculation/fontname",config.fontname)
            fontsize = int(QSettings().value("SurveyingCalculation/fontsize",config.fontsize))
            self.ui.ResultTextBrowser.setFont(QFont(fontname, fontsize))
        log_path = QSettings().value("SurveyingCalculation/log_path",config.log_path)
        self.log.set_log_path(log_path)
        self.reset()
        
    def reset(self):
        """ Reset dialog to initial state
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
        """ Change dialog controls when an other calculation type selected.
        """
        # get selected stations
        oldStation1 = self.ui.Station1Combo.itemData( self.ui.Station1Combo.currentIndex() )
        oldStation2 = self.ui.Station2Combo.itemData( self.ui.Station2Combo.currentIndex() )
        # clear station combos
        self.ui.Station1Combo.clear()
        self.ui.Station2Combo.clear()
        self.ui.Station1Combo.setEnabled(False)
        self.ui.Station2Combo.setEnabled(False)
        
        #get combobox models
        combomodel1 = self.ui.Station1Combo.model()
        combomodel2 = self.ui.Station2Combo.model()

        #get stations        
        known_stations = get_stations(True,False)
        all_stations = get_stations(False,False)
        oriented_stations = get_stations(True,True)
        # fill Station1Combo and Station2Combo
        stations1 = []      
        stations2 = []      
        if known_stations is not None and self.ui.OrientRadio.isChecked():
            for stn in known_stations:
                stations1.append( [u"%s (%s:%s)"% (stn[0],stn[1],stn[2]), stn] )
            self.ui.Station1Combo.setEnabled(True)
        elif oriented_stations is not None and (self.ui.RadialRadio.isChecked() or \
                self.ui.IntersectRadio.isChecked()):
            for stn in oriented_stations:
                stations1.append( [u"%s (%s:%s)"% (stn[0],stn[1],stn[2]), stn] )
                if self.ui.IntersectRadio.isChecked():
                    stations2.append( [u"%s (%s:%s)"% (stn[0],stn[1],stn[2]), stn] )
            self.ui.Station1Combo.setEnabled(True)
            if self.ui.IntersectRadio.isChecked():
                self.ui.Station2Combo.setEnabled(True)
        elif all_stations is not None and (self.ui.ResectionRadio.isChecked() or \
                self.ui.FreeRadio.isChecked()):
            self.ui.Station1Combo.setEnabled(True)
            for stn in all_stations:
                stations1.append( [u"%s (%s:%s)"% (stn[0],stn[1],stn[2]), stn] )

        known_points = get_known()
        if stations1 is not None:
            for station in stations1:
                item = QStandardItem(station[0])
                item.setData(station[1],Qt.UserRole)
                if known_points is not None and station[1][0] in known_points:
                    itemfont = item.font()
                    itemfont.setWeight(QFont.Bold)
                    item.setFont(itemfont)
                combomodel1.appendRow( item )
        if self.ui.IntersectRadio.isChecked() and stations2 is not None:
            for station in stations2:
                item = QStandardItem(station[0])
                item.setData(station[1],Qt.UserRole)
                if known_points is not None and station[1][0] in known_points:
                    itemfont = item.font()
                    itemfont.setWeight(QFont.Bold)
                    item.setFont(itemfont)
                combomodel2.appendRow( item )
                
        # select previously selected stations if present in the list
        self.ui.Station1Combo.setCurrentIndex( self.ui.Station1Combo.findData(oldStation1) )
        self.ui.Station2Combo.setCurrentIndex( self.ui.Station2Combo.findData(oldStation2) )
        
    def fillSourceList(self):
        """ Change dialog controls when an other calculation type selected.
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
            targets = get_targets(stn1[0], stn1[1], stn1[2],False,True)
        elif stn1 is not None and stn2 is not None and \
                self.ui.IntersectRadio.isChecked():
            # fill source list for intersection (common points)
            targets_stn1 = get_targets(stn1[0], stn1[1], stn1[2],False)
            targets_stn2 = get_targets(stn2[0], stn2[1], stn2[2],False)
            for t1 in targets_stn1:
                for t2 in targets_stn2:
                    if t1[0] == t2[0]:
                        if not t1[0] in targets:
                            targets.append([t1,t2])
                        break
            
        # fill source list widget
        known_list = get_known()
        if targets is not None:
            for target in targets:
                if self.ui.IntersectRadio.isChecked():
                    item = QListWidgetItem(target[0][0])
                    item.setData(Qt.UserRole,target)
                    if known_list is not None and target[0][0] in known_list:
                        itemfont = item.font()
                        itemfont.setWeight(QFont.Bold)
                        item.setFont(itemfont)
                else:
                    item = QListWidgetItem(u"%s (id:%s)"% (target[0],target[2]) )
                    item.setData(Qt.UserRole,target)
                    if known_list is not None and target[0] in known_list:
                        itemfont = item.font()
                        itemfont.setWeight(QFont.Bold)
                        item.setFont(itemfont)
                self.ui.SourceList.addItem( item )

    def radioClicked(self):
        """ Change dialog controls when an other calculation type selected.
        """
        self.fillStationCombos()
        self.fillSourceList()
        
    def stationComboChanged(self):
        """ Init source and target list when one of two station combobox changed.
        """
        self.fillSourceList()
        
    def onAddButton(self):
        """ Add selected target points to used points list.
        """
        selected = self.ui.SourceList.selectedItems()
        for item in selected:
            self.ui.TargetList.addItem( self.ui.SourceList.takeItem( self.ui.SourceList.row(item) ) )
            
    def onAddAllButton(self):
        """ Add all target points to used points list.
        """
        while self.ui.SourceList.count():
            self.ui.TargetList.addItem( self.ui.SourceList.takeItem( 0 ) )

    def onRemoveButton(self):
        """ Remove selected used points and add to target points list.
        """
        selected = self.ui.TargetList.selectedItems()
        for item in selected:
            self.ui.SourceList.addItem( self.ui.TargetList.takeItem( self.ui.TargetList.row(item) ) )

    def onRemoveAllButton(self):
        """ Remove all used points and add to target points list.
        """
        while self.ui.TargetList.count():
            self.ui.SourceList.addItem( self.ui.TargetList.takeItem( 0 ) )
    
    def onCalcButton(self):
        """ Start a calculation when the Calculate button pushed.
        """
        if self.ui.radioButtonGroup.checkedId() == -1:
            QMessageBox.warning(self, tr("Warning"), tr("Select the type of calculation!"))
            return

        # get the selected stations
        stn1 = self.ui.Station1Combo.itemData( self.ui.Station1Combo.currentIndex() )
        if stn1 is None:
            QMessageBox.warning(self, tr("Warning"), tr("Select station point 1!"))
            self.ui.Station1Combo.setFocus()
            return
        stn2 = self.ui.Station2Combo.itemData( self.ui.Station2Combo.currentIndex() )
        if stn2 is None and self.ui.IntersectRadio.isChecked():
            QMessageBox.warning(self, tr("Warning"), tr("Select station point 2!"))
            self.ui.Station2Combo.setFocus()
            return
        if self.ui.TargetList.count()==0:
            QMessageBox.warning(self, tr("Warning"), tr("Add points to Used Points list!"))
            self.ui.TargetList.setFocus()
            return

        if self.ui.OrientRadio.isChecked():
            # orientation
            s = get_station(stn1[0], stn1[1], stn1[2])
            ref_list = []
            for i in range(self.ui.TargetList.count()):
                targetp = self.ui.TargetList.item(i).data(Qt.UserRole)
                to = get_target(targetp[0], targetp[1], targetp[2])
                tp = ScPoint(targetp[0])
                ref_list.append([tp,to])
            z = Calculation.orientation(s, ref_list)
            if z is not None:
                set_orientationangle(stn1[0], stn1[1], stn1[2], z.get_angle("GON"))
                self.ui.ResultTextBrowser.append("\n" + tr("Orientation") + " - %s" % s.p.id)
                self.ui.ResultTextBrowser.append(
                    tr("Point num  Code         Direction    Bearing   Orient ang   Distance   e(cc) E(m)"))
                self.ui.ResultTextBrowser.append(ResultLog.resultlog_message)
                self.log.write()
                self.log.write_log(tr("Orientation") + " - %s" % s.p.id)
                self.log.write(tr("Point num  Code         Direction    Bearing   Orient ang   Distance   e(cc) E(m)"))
                self.log.write(ResultLog.resultlog_message)
            else:
                QMessageBox.warning(self, tr("Warning"), tr("Orientation angle cannot be calculated!"))

        elif self.ui.RadialRadio.isChecked():
            # radial surveys (polar point)
            s = get_station(stn1[0], stn1[1], stn1[2])
            log_header = False
            for i in range(self.ui.TargetList.count()):
                targetp = self.ui.TargetList.item(i).data(Qt.UserRole)
                to = get_target(targetp[0], targetp[1], targetp[2])
                tp = ScPoint(targetp[0])
                p = Calculation.polarpoint(s, to)
                if p is not None:
                    # log results
                    if log_header is False:
                        self.ui.ResultTextBrowser.append("\n" + tr("Radial Survey"))
                        self.ui.ResultTextBrowser.append(tr("Point num  Code              E            N        Z     Bearing  H.Distance"))
                        self.log.write()
                        self.log.write_log(tr("Radial Survey"))
                        self.log.write(tr("Point num  Code              E            N        Z     Bearing  H.Distance"))
                        log_stn = u"%-10s %-10s %12.3f %12.3f %8.3s     <station>" % \
                            (s.p.id, (s.p.pc if s.p.pc is not None else "-"), s.p.e, s.p.n, \
                            ("%8.3f"%s.p.z if s.p.z is not None else "") )
                        self.log.write(log_stn)
                        self.ui.ResultTextBrowser.append(log_stn)
                        log_header = True
                    tp.set_coord(p)
                    if p.z is None:
                        # no z calculated
                        self.ui.ResultTextBrowser.append(ResultLog.resultlog_message)
                        self.log.write(ResultLog.resultlog_message)
                        tp.store_coord(2)
                    else:
                        self.ui.ResultTextBrowser.append(ResultLog.resultlog_message)
                        self.log.write(ResultLog.resultlog_message)
                        tp.store_coord(3)
                else:
                    QMessageBox.warning(self, tr("Warning"), tr("Radial survey on %s cannot be calculated!") % targetp[0])

        elif self.ui.IntersectRadio.isChecked():
            # intersection
            s1 = get_station(stn1[0], stn1[1], stn1[2])
            s2 = get_station(stn2[0], stn2[1], stn2[2])
            if stn1 == stn2:
                QMessageBox.warning(self, tr("Warning"), tr("Station 1 and station 2 are the same!"))
                self.ui.Station1Combo.setFocus()
                return
            log_header = False
            for i in range(self.ui.TargetList.count()):
                itemdata = self.ui.TargetList.item(i).data(Qt.UserRole)
                targetp1 = itemdata[0]
                targetp2 = itemdata[1]
                to1 = get_target(targetp1[0], targetp1[1], targetp1[2])
                tp1 = ScPoint(targetp1[0])
                to2 = get_target(targetp2[0], targetp2[1], targetp2[2])
                #tp2 = ScPoint(targetp2[0])
                p = Calculation.intersection(s1, to1, s2, to2)
                if p is not None:
                    # log results
                    if log_header is False:
                        self.ui.ResultTextBrowser.append("\n" + tr("Intersection"))
                        self.ui.ResultTextBrowser.append(tr("Point num  Code              E            N     Bearing1 Bearing2"))
                        self.log.write()
                        self.log.write_log(tr("Intersection"))
                        self.log.write(tr("Point num  Code              E            N     Bearing1 Bearing2"))

                        log_stn = u"%-10s %-10s %12.3f %12.3f     <station>\n" % \
                            (s1.p.id, (s1.p.pc if s1.p.pc is not None else "-"), s1.p.e, s1.p.n)
                        log_stn += u"%-10s %-10s %12.3f %12.3f     <station>" % \
                            (s2.p.id, (s2.p.pc if s2.p.pc is not None else "-"), s2.p.e, s2.p.n)
                        self.log.write(log_stn)
                        self.ui.ResultTextBrowser.append(log_stn)
                        log_header = True
                    tp1.set_coord(p)
                    tp1.store_coord(2)
                    self.ui.ResultTextBrowser.append(ResultLog.resultlog_message)
                    self.log.write(ResultLog.resultlog_message)
                else:
                    QMessageBox.warning(self, tr("Warning"), tr("Intersecion on %s cannot be calculated!") % targetp1[0])

        elif self.ui.ResectionRadio.isChecked():
            # resection
            s = get_station(stn1[0], stn1[1], stn1[2])
            if self.ui.TargetList.count()!=3:
                QMessageBox.warning(self, tr("Warning"), tr("Select exactly 3 used points for resection!"))
                self.ui.TargetList.setFocus()
                return
            targetp1 = self.ui.TargetList.item(0).data(Qt.UserRole)
            targetp2 = self.ui.TargetList.item(1).data(Qt.UserRole)
            targetp3 = self.ui.TargetList.item(2).data(Qt.UserRole)
            to1 = get_target(targetp1[0], targetp1[1], targetp1[2])
            to2 = get_target(targetp2[0], targetp2[1], targetp2[2])
            to3 = get_target(targetp3[0], targetp3[1], targetp3[2])
            tp1 = ScPoint(targetp1[0])            
            tp2 = ScPoint(targetp2[0])            
            tp3 = ScPoint(targetp3[0])            
            p = Calculation.resection(s, tp1, tp2, tp3, to1, to2, to3)
            ScPoint(p).store_coord(2)
            # result log
            self.ui.ResultTextBrowser.append("\n" + tr("Resection"))
            self.ui.ResultTextBrowser.append(tr("Point num  Code                E            N      Direction  Angle"))
            self.ui.ResultTextBrowser.append(ResultLog.resultlog_message)
            self.log.write()
            self.log.write_log(tr("Resection"))
            self.log.write(tr("Point num  Code                E            N      Direction  Angle"))
            self.log.write(ResultLog.resultlog_message)
        elif self.ui.FreeRadio.isChecked():
            # free station
            g = GamaInterface()  # default standard deviations are used!
            s = get_station(stn1[0], stn1[1], stn1[2])
            g.add_point(s.p, 'ADJ')
            g.add_observation(s.o)
            for i in range(self.ui.TargetList.count()):
                targetp = self.ui.TargetList.item(i).data(Qt.UserRole)
                p = get_coord(targetp[0])
                g.add_point(p, 'FIX')
                to = get_target(targetp[0], targetp[1], targetp[2])
                g.add_observation(to)
            t = g.adjust()
            if t is None:
                # adjustment failed
                self.ui.ResultTextBrowser.append(tr('gama-local not installed or other runtime error'))
            else:
                self.ui.ResultTextBrowser.append(t)
        
    def onResetButton(self):
        """ Reset dialog when the Reset button pushed.
        """
        self.reset()
    
    def onCloseButton(self):
        """ Close the dialog when the Close button pushed.
        """
        self.accept()

    def onHelpButton(self):
        """ Open user's guide at Single Point Calculations in the default web browser.
        """
        webbrowser.open("http://www.digikom.hu/SurveyingCalculation/usersguide.html#single-point-calculations")
