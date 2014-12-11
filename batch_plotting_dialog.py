# -*- coding: utf-8 -*-
"""
.. module:: batch_plotting_dialog
    :platform: Linux, Windows
    :synopsis: GUI for batch plotting

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>
"""
from PyQt4.QtGui import QDialog
#from PyQt4.QtCore import Qt

from batch_plotting import Ui_BatchPlottingDialog

class BatchPlottingDialog(QDialog):
    """ Class for batch plotting dialog
    """
    def __init__(self):
        """ Initialize dialog data and event handlers
        """
        super(BatchPlottingDialog, self).__init__()
        self.ui = Ui_BatchPlottingDialog()
        self.ui.setupUi(self)

        # event handlers
        self.ui.PrintButton.clicked.connect(self.onPrintButton)
        self.ui.TempDirButton.clicked.connect(self.onTempDirButton)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)
        self.ui.TemplateList.setSortingEnabled(True)

    def onTempDirButton(self):
        """ Change the directory that contains print composer templates.
        """
        pass

    def onPrintButton(self):
        """ Batch plots selected geometry items using the selected template and scale.
        """
        pass

    def onCloseButton(self):
        """ Close the dialog when the Close button pushed.
        """
        self.accept()
    