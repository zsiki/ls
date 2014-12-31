# -*- coding: utf-8 -*-
"""
.. module:: area_dialog
    :platform: Linux, Windows
    :synopsis: GUI for area division

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>
"""
from PyQt4.QtGui import QDialog, QMessageBox
from area_div import Ui_AreaDivDialog
from base_classes import tr

class AreaDialog(QDialog):
    """ Class for area division dialog
    """
    def __init__(self, total_area, div_area):
        """ Initialize dialog data and event handlers

            :param log: log instance for log messages
        """
        super(AreaDialog, self).__init__()
        self.total_area = int(total_area + 0.5)
        self.div_area = int(div_area + 0.5)
        self.ui = Ui_AreaDivDialog()
        self.ui.setupUi(self)
        self.ui.CancelButton.clicked.connect(self.onCancelButton)
        self.ui.DivideButton.clicked.connect(self.onDivideButton)

    def showEvent(self, event):
        """ Set up initial state of dialog widgets

            :param event: NOT USED
        """
        self.reset()

    def reset(self):
        """ Reset dialog to initial state
        """
        self.ui.AreaLineEdit.setText(str(self.div_area))
        self.ui.TotalLineEdit.setText(str(self.total_area))
        self.ui.OnePointRadio.setChecked(True)

    def onDivideButton(self):
        """ Check input and accept dialog
        """
        try:
            a = float(self.ui.AreaLineEdit.text())
        except ValueError:
            QMessageBox.warning(self, tr("Warning"), tr("Invalid area value"))
            return
        if a <= 0:
            QMessageBox.warning(self, tr("Warning"), tr("Invalid area value"))
            return
        if not self.ui.OnePointRadio.isChecked() and not self.ui.TwoPointRadio.isChecked():
            QMessageBox.warning(self, tr("Warning"), tr("Select division method"))
            return
        self.accept()

    def onCancelButton(self):
        """ Reject dialog
        """
        self.reject()
