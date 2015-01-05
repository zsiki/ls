#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: transformation_dialog
    :platform: Linux, Windows
    :synopsis: GUI for coordinate transformation

.. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""
import platform
from PyQt4.QtGui import QDialog, QFileDialog, QFont, QMessageBox
from PyQt4.QtCore import SIGNAL, QCoreApplication

import config
from transformation_calc import Ui_TransformationCalcDialog
from base_classes import *
from surveying_util import *
from calculation import *

class TransformationDialog(QDialog):
    """ Class for transformation calculation dialog
    """
    def __init__(self, log):
        """ Initialize dialog data and event handlers
        """
        super(TransformationDialog, self).__init__()
        self.ui = Ui_TransformationCalcDialog()
        self.ui.setupUi(self)
        self.log = log
        if platform.system() == 'Linux':
            # change font
            self.ui.ResultTextBrowser.setFont(QFont(config.fontname, config.fontsize))
        self.from_points = []
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
        """ set up initial state of dialog

            :param event: NOT USED
        """
        self.reset()

    def reset(self):
        """ Reset dialog to initial state
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
        self.ui.ResultTextBrowser.clear()

    def onCloseButton(self):
        """ Close dialog after Close button pressed
        """
        self.accept()

    def onResetButton(self):
        """ Reset dialog to initial state after Reset button pressed
        """
        self.reset()

    def onToFileButton(self):
        """ Select target shape file
        """
        fname = QFileDialog.getOpenFileName(None, tr('Coordinate list'),
            filter= tr('Coordinate list file (*.shp);;'))
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
        """ Add selected points to used points in transformation
        """
        selected = self.ui.CommonList.selectedItems()
        for item in selected:
            i  = self.ui.CommonList.row(item)
            self.ui.UsedList.addItem(self.ui.CommonList.takeItem(i))
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
        """ Remove selected points from used points
        """
        selected = self.ui.UsedList.selectedItems()
        for item in selected:
            i  = self.ui.UsedList.row(item)
            self.ui.CommonList.addItem(self.ui.UsedList.takeItem(i))
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
        """ Find common points in coordinate lists
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
        self.from_points = get_known(2, from_name)
        self.common = []
        self.used = []
        for from_p in self.from_points:
            if from_p in to_points:
                self.common.append(from_p)
        for p in self.common:
            self.ui.CommonList.addItem(p)

    def onCalcButton(self):
        """ Start transformation calculation
        """
        from_list = self.ui.FromLayerComboBox.currentText()
        if len(from_list) == 0:
            QMessageBox.warning(self, tr("Warning"), tr("Select from layer!"))
            return
        to_list = 'tmp_to_shape'
        p_list = []
        to_name = self.ui.ToShapeEdit.text()
        if len(to_name) == 0:
            QMessageBox.warning(self, tr("Warning"), tr("Select to shape file!"))
            return
        to_shp = QgsVectorLayer(to_name, "tmp_to_shape", "ogr") 
        QgsMapLayerRegistry.instance().addMapLayer(to_shp, False)
        for point_id in self.used:
            # get coords of points
            p_from = get_coord(point_id, from_list)
            p_to = get_coord(point_id, to_list)
            p_list.append([p_from, p_to])
        w = ''
        if self.ui.OrthogonalRadio.isChecked():
            tr_res = Calculation.orthogonal_transformation(p_list)
            tr_func = self.ortho_tr
            w = tr('\nOrthogonal transformation')
        elif self.ui.AffineRadio.isChecked():
            tr_res = Calculation.affine_transformation(p_list)
            tr_func = self.affine_tr
            w = tr('\nAffine transformation')
        elif self.ui.ThirdRadio.isChecked():
            tr_res = Calculation.polynomial_transformation(p_list, 3)
            tr_func = self.poly3_tr
            w = tr('\n3rd order polynomial transformation')
        elif self.ui.FourthRadio.isChecked():
            tr_res = Calculation.polynomial_transformation(p_list, 4)
            tr_func = self.poly4_tr
            w = tr('\n4th order polynomial transformation')
        elif self.ui.FifthRadio.isChecked():
            tr_res = Calculation.polynomial_transformation(p_list, 5)
            tr_func = self.poly5_tr
            w = tr('\n5th order polynomial transformation')
        else:
            QMessageBox.warning(self, tr("Warning"), tr("Select transformation type!"))
            return

        self.ui.ResultTextBrowser.append(w)
        self.log.write()
        self.log.write_log(w)

        # calculate transformed coordinates
        w = tr('Point num                E from       N from       E to         N to      dE     dN')
        self.ui.ResultTextBrowser.append(w)
        self.log.write(w)
        for (p_from, p_to) in p_list:
            (e, n) = tr_func(p_from, tr_res)
            de = p_to.e - e
            dn = p_to.n - n
            buf = '%-20s ' % p_from.id + \
                '%12.3f ' % p_from.e + '%12.3f ' % p_from.n + \
                '%12.3f ' % p_to.e + '%12.3f ' % p_to.n + \
                '%6.3f ' % de + '%6.3f ' % dn
            self.ui.ResultTextBrowser.append(buf)
            self.log.write(buf)
        # transform and store new points
        for p_num in self.from_points:
            if not p_num in self.used and not p_num in self.common:
                p = get_coord(p_num, from_list)
                (e, n) = tr_func(p, tr_res)
                buf = '%-20s ' % p.id + \
                    '%12.3f ' % p.e + '%12.3f ' % p.n + \
                    '%12.3f ' % e + '%12.3f ' % n
                self.ui.ResultTextBrowser.append(buf)
                self.log.write(buf)
                pp = Point(p_num, e, n, pc='transformed')
                ScPoint(pp).store_coord(2, "tmp_to_shape")
        QgsMapLayerRegistry.instance().removeMapLayer("tmp_to_shape")

    def ortho_tr(self, p, tr):
        """ Calculate orthogonal transformation for a point

            :param p: point to transform (Point)
            :param tr: transformation parameters
            :returns: list of easting and northin of transformed coordinates
        """
        e = tr[0] + tr[2] * p.e - tr[3] * p.n
        n = tr[1] + tr[3] * p.e + tr[2] * p.n
        return (e, n)

    def affine_tr(self, p, tr):
        """ Calculate affine transformation for a point

            :param p: point to transform (Point)
            :param tr: transformation parameters
            :returns: list of easting and northin of transformed coordinates
        """
        e = tr[0] + tr[2] * p.e + tr[3] * p.n
        n = tr[1] + tr[4] * p.e + tr[5] * p.n
        return (e, n)

    def poly_tr(self, p, tr, degree):
        """ Calculate nth order polynomial transformation for a point

            :param p: point to transform (Point)
            :param tr: transformation parameters
            :param degree: degree of transformation
            :returns: list of easting and northin of transformed coordinates
        """
        de = p.e - tr[2][0]
        dn = p.n - tr[2][1]
        l = 0
        e = tr[2][2]
        n = tr[2][3]
        for j in range(0,degree+1):
            for k in range(0,degree+1):
                if j + k <= degree:
                    e += tr[0][l] * math.pow(de,k) * math.pow(dn,j)
                    n += tr[1][l] * math.pow(de,k) * math.pow(dn,j)
                    l += 1
        return (e, n)

    def poly3_tr(self, p, tr):
        """ Calculate 3rd order polynomial transformation for a point

            :param p: point to transform (Point)
            :param tr: transformation parameters (list of lists)
            :returns: list of easting and northing of transformed coordinates
        """
        (e, n) = self.poly_tr(p, tr, 3)
        return (e, n)

    def poly4_tr(self, p, tr):
        """ Calculate 4th order polynomial transformation for a point

            :param p: point to transform (Point)
            :param tr: transformation parameters
            :returns: list of easting and northin of transformed coordinates
        """
        return self.poly_tr(p, tr, 4)

    def poly5_tr(self, p, tr):
        """ Calculate 5th order polynomial transformation for a point

            :param p: point to transform (Point)
            :param tr: transformation parameters
            :returns: list of easting and northin of transformed coordinates
        """
        return self.poly_tr(p, tr, 5)
