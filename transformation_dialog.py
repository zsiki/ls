#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    GNU Gama interface classes for Land Surveying Plug-in for QGIS
    GPL v2.0 license
    Copyright (C) 2014-  DigiKom Kft. http://digikom.hu
    .. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""

from PyQt4.QtGui import QDialog, QFileDialog
from PyQt4.QtCore import SIGNAL
from transformation_calc import Ui_TransformationCalcDialog

from surveying_util import *
from calculation import *

class TransformationDialog(QDialog):
    """
        Class for transformation calculation dialog
    """
    def __init__(self):
        super(TransformationDialog, self).__init__()
        self.ui = Ui_TransformationCalcDialog()
        self.ui.setupUi(self)
        self.common = []
        self.used = []
        self.ui.CloseButton.clicked.connect(self.onCloseButton)
        self.ui.ResetButton.clicked.connect(self.onResetButton)
        self.ui.ToFileButton.clicked.connect(self.onToFileButton)
        self.ui.AddButton.clicked.connect(self.onAddButton)
        self.ui.RemoveButton.clicked.connect(self.onRemoveButton)
        self.ui.CalcButton.clicked.connect(self.onCalcButton)
        # coordinate list changed
        self.connect(self.ui.FromLayerComboBox, SIGNAL("currentIndexChanged(const QString&)"), self.fill_common)

    def showEvent(self, event):
        """
            set up initial state of dialog
        """
        self.reset()

    def reset(self):
        """
            Reset dialog to initial state
        """
        # fill from list
        self.ui.FromLayerComboBox.clear()
        clist = get_coordlist()
        if clist is not None:
            self.ui.FromLayerComboBox.addItems(clist)
        # clear to file
        self.ui.ToShapeEdit.setText('')
        # clear comon & used list
        self.ui.CommonList.clear()
        self.ui.UsedList.clear()
        # select orthogonal transformation
        self.ui.OrthogonalRadio.setChecked(False)
        self.ui.AffineRadio.setChecked(False)
        self.ui.ThirdRadio.setChecked(False)
        self.ui.FourthRadio.setChecked(False)
        self.ui.FifthRadio.setChecked(False)
        self.ui.OrthogonalRadio.setEnabled(False)
        self.ui.AffineRadio.setEnabled(False)
        self.ui.ThirdRadio.setEnabled(False)
        self.ui.FourthRadio.setEnabled(False)
        self.ui.FifthRadio.setEnabled(False)

    def onCloseButton(self):
        """
            Close dialog after Close button pressed
        """
        self.accept()

    def onResetButton(self):
        """
            Reset dialog to initial state after Reset button pressed
        """
        self.reset()

    def onToFileButton(self):
        """
            Select target shape file
        """
        fname = QFileDialog.getOpenFileName(None, self.tr('Coordinate list'),
            filter= self.tr('Coordinate list file (*.shp);;'))
        if fname:
            self.ui.ToShapeEdit.setText(fname)
            if len(self.ui.FromLayerComboBox.currentText()):
                # fill common list
                self.fill_common()
        else:
            self.ui.ToShapeEdit.setText('')
            # clear comon & used list
            self.ui.CommonList.clear()
            self.ui.UsedList.clear()

    def onAddButton(self):
        """
            Add point to used point in transformation
        """
        i = self.ui.CommonList.currentRow()
        if i < 0:
            return
        item = self.ui.CommonList.takeItem(i)
        self.ui.UsedList.addItem(item)
        self.used.append(self.common[i])
        del self.common[i]
        if len(self.used) > 1:
            self.ui.OrthogonalRadio.setEnabled(True)
        if len(self.used) > 2:
            self.ui.AffineRadio.setEnabled(True)
        if len(self.used) > 9:
            self.ui.ThirdRadio.setEnabled(True)
        if len(self.used) > 14:
            self.ui.FourthRadio.setEnabled(True)
        if len(self.used) > 20:
            self.ui.FifthRadio.setEnabled(True)
    
    def onRemoveButton(self):
        """
            Remove point from used points
        """
        i = self.ui.UsedList.currentRow()
        if i < 0:
            return
        item = self.ui.UsedList.takeItem(i)
        self.ui.CommonList.addItem(item)
        self.common.append(self.used[i])
        del self.used[i]
        if len(self.used) < 2:
            self.ui.OrthogonalRadio.setEnabled(False)
        if len(self.used) < 3:
            self.ui.AffineRadio.setEnabled(False)
        if len(self.used) < 10:
            self.ui.ThirdRadio.setEnabled(False)
        if len(self.used) < 15:
            self.ui.FourthRadio.setEnabled(False)
        if len(self.used) < 21:
            self.ui.FifthRadio.setEnabled(False)

    def fill_common(self):
        """
            Find common points in coordinate lists
        """
        self.ui.UsedList.clear()
        self.ui.CommonList.clear()
        from_name = self.ui.FromLayerComboBox.currentText()
        to_name = self.ui.ToShapeEdit.text()
        if len(from_name) == 0 or len(to_name) == 0:
            return
        to_shp = QgsVectorLayer(to_name, "tmp_to_shape", "ogr") 
        QgsMapLayerRegistry.instance().addMapLayer(to_shp, False)
        to_points = get_known(2, "tmp_to_shape")
        QgsMapLayerRegistry.instance().removeMapLayer("tmp_to_shape")
        from_points = get_known(2, from_name)
        self.common = []
        self.used = []
        for from_p in from_points:
            if from_p in to_points:
                self.common.append(from_p)
        for p in self.common:
            self.ui.CommonList.addItem(p)

    def onCalcButton(self):
        """
            Start transformation calculation
        """
        from_list = self.ui.FromLayerComboBox.currentText()
        to_list = 'tmp_to_shape'
        p_list = []
        to_name = self.ui.ToShapeEdit.text()
        to_shp = QgsVectorLayer(to_name, "tmp_to_shape", "ogr") 
        QgsMapLayerRegistry.instance().addMapLayer(to_shp, False)
        for point_id in self.used:
            # get coords of points
            p_from = get_coord(point_id, from_list)
            p_to = get_coord(point_id, to_list)
            p_list.append([p_from, p_to])
            print p_from
            print p_to
        QgsMapLayerRegistry.instance().removeMapLayer("tmp_to_shape")
        if self.ui.OrthogonalRadio.isChecked():
            tr = Calculation.orthogonal_transformation(p_list)
            print tr
        elif self.ui.AffineRadio.isChecked():
            tr = Calculation.affine_transformation(p_list)
            print tr
        elif self.ui.ThirdRadio.isChecked():
            tr = Calculation.polynomial_transformation(p_list, 3)
            print tr
        elif self.ui.FourthRadio.isChecked():
            tr = Calculation.polynomial_transformation(p_list, 4)
            print tr
        elif self.ui.FifthRadio.isChecked():
            tr = Calculation.polynomial_transformation(p_list, 5)
            print tr
