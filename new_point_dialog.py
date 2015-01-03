#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: new_point_dialog
    :platform: Linux, Windows
    :synopsis: GUI to add a point by coordinates

.. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""

from PyQt4.QtGui import QDialog, QMessageBox
#from PyQt4.QtCore import SIGNAL, QCoreApplication

from add_new_point import Ui_AddNewPointDialog
from base_classes import *
from surveying_util import *

class NewPointDialog(QDialog):
    """ Class for new point dialog
    """
    def __init__(self):
        """ Initialize dialog data and event handlers
        """
        super(NewPointDialog, self).__init__()
        self.ui = Ui_AddNewPointDialog()
        self.ui.setupUi(self)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)
        self.ui.ResetButton.clicked.connect(self.onResetButton)
        self.ui.AddButton.clicked.connect(self.onAddButton)

    def showEvent(self, event):
        """ set up initial state of dialog

            :param event: NOT USED
        """
        self.reset()

    def reset(self):
        """ Reset dialog to initial state
        """
        self.ui.PointNumberLineEdit.setText('')
        self.ui.EastCoordLineEdit.setText('')
        self.ui.NorthCoordLineEdit.setText('')
        self.ui.ZCoordLineEdit.setText('')
        self.ui.PointCodeLineEdit.setText('')
        self.ui.PointTypeLineEdit.setText('')

    def onCloseButton(self):
        """ Close dialog after Close button pressed
        """
        self.accept()

    def onResetButton(self):
        """ Reset dialog to initial state after Reset button pressed
        """
        self.reset()

    def onAddButton(self):
        """ Check input data and add point to the coordinate list
        """
        msg = ''
        pnum = self.ui.PointNumberLineEdit.text().strip()[0:20]
        if len(pnum) == 0:
            msg += tr("Please fill point ID\n")
        try:
            e = float(self.ui.EastCoordLineEdit.text().strip())
        except ValueError:
            msg += ("Please give a valid easting coordinate\n")
        try:
            n = float(self.ui.NorthCoordLineEdit.text().strip())
        except ValueError:
            msg += ("Please give a valid northing coordinate\n")
        w = self.ui.ZCoordLineEdit.text().strip()
        if len(w):
            try:
                z = float(w)
            except ValueError:
                msg += ("Please give a valid elevation or clear the field\n")
        else:
            z = None
        w = self.ui.PointCodeLineEdit.text().strip()[0:20]
        if len(w):
            pc = w
        else:
            pc = None
        w = self.ui.PointTypeLineEdit.text().strip()[0:20]
        if len(w):
            pt = w
        else:
            pt = None
        if len(msg):
            QMessageBox.warning(self, tr("Warning"), msg)
            return
        # check new
        #p = Point(pnum)
        if get_coord(pnum) is not None and \
            QMessageBox.question(self, tr("Warning"), tr("Point is already in the point list. Do you want to overwrite?"), tr("Yes"), tr("No")) == 1:
            return

        p = ScPoint(Point(pnum, e, n, z, pc, pt))
        if not p.store_coord():
            QMessageBox.warning(self, tr("Warning"), tr("Point is not stored")) 
        self.reset()
