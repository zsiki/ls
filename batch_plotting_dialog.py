# -*- coding: utf-8 -*-
"""
.. module:: batch_plotting_dialog
    :platform: Linux, Windows
    :synopsis: GUI for batch plotting

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>
"""
import os, glob
from PyQt4.QtGui import QDialog, QFileDialog, QMessageBox
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
        self.ui.PlotButton.clicked.connect(self.onPlotButton)
        self.ui.TempDirButton.clicked.connect(self.onTempDirButton)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)
        self.ui.TemplateList.setSortingEnabled(True)
        
        plugin_dir = os.path.dirname(os.path.abspath(__file__))
        self.dirpath = os.path.join(plugin_dir, 'template')

        self.fillTemplateList()
        
    def fillTemplateList(self):
        """ Fill the listbox of composer template files.
        """
        self.ui.TemplateList.clear()
        if  os.path.exists(self.dirpath):
            pattern = os.path.join(self.dirpath,'*.qpt')
            for temp in glob.iglob(pattern):
                tname = os.path.basename(temp)
                self.ui.TemplateList.addItem(tname)

    def onTempDirButton(self):
        """ Change the directory that contains print composer templates.
        """
        dirpath = str(QFileDialog.getExistingDirectory(self, 
                        "Select Directory",self.dirpath))
        if dirpath!="":
            self.dirpath = dirpath 
        self.fillTemplateList()

    def onPlotButton(self):
        """ Batch plots selected geometry items using the selected template and scale.
        """
        if self.ui.TemplateList.selectedItems() == []:
            QMessageBox.warning(self,self.tr("Warning"),self.tr("Select a composer template!"))
            self.ui.TemplateList.setFocus()
            return
        #if not len(self.ui.ScaleCombo.currentText()):
        
        self.template_file = os.path.join(self.dirpath,
            self.ui.TemplateList.currentItem().text())
        try:
            self.scale = int(self.ui.ScaleCombo.currentText())
        except (ValueError):
            QMessageBox.warning(self,self.tr("Warning"),self.tr("Scale must be an integer value!"))
            self.ui.ScaleCombo.setFocus()
            return

        self.accept()
        
    def onCloseButton(self):
        """ Close the dialog when the Close button pushed.
        """
        self.reject()
    