# -*- coding: utf-8 -*-
"""
.. module:: coord_dialog
    :platform: Linux, Windows
    :synopsis: GUI for area division

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>
"""
from PyQt4.QtGui import QDialog, QMessageBox
from coords import Ui_CoordDialog
from base_classes import tr

class CoordDialog(QDialog):
    """ Class for coords of division line dialog
    """
    def __init__(self, point1, point2):
        """ Initialize dialog data and event handlers

            :param log: log instance for log messages
        """
        super(CoordDialog, self).__init__()
        self.point1 = point1
        self.point2 = point2
        self.ui = Ui_CoordDialog()
        self.ui.setupUi(self)
        self.ui.CancelButton.clicked.connect(self.onCancelButton)
        self.ui.ContinueButton.clicked.connect(self.onContinueButton)

    def showEvent(self, event):
        """ Set up initial state of dialog widgets

            :param event: NOT USED
        """
        self.reset()

    def reset(self):
        """ Reset dialog to initial state
        """
        self.ui.StartEast.setText('{0:.2f}'.format(self.point1.x()))
        self.ui.StartNorth.setText('{0:.2f}'.format(self.point1.y()))
        self.ui.EndEast.setText('{0:.2f}'.format(self.point2.x()))
        self.ui.EndNorth.setText('{0:.2f}'.format(self.point2.y()))

    def onContinueButton(self):
        """ Check input and accept dialog
        """
        try:
            w = float(self.ui.StartEast.text())
            w = float(self.ui.StartNorth.text())
            w = float(self.ui.EndEast.text())
            w = float(self.ui.EndNorth.text())
        except ValueError:
            QMessageBox.warning(self, tr("Warning"), tr("Invalid coordinate value"))
            return
        self.accept()

    def onCancelButton(self):
        """ Reject dialog
        """
        self.reject()
