# -*- coding: utf-8 -*-
"""
.. module:: plugin_settings_dialog
    :platform: Linux, Windows
    :synopsis: GUI for SurveyingCalculation plugin settings

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>
"""
from PyQt4.QtGui import QDialog, QFileDialog, QMessageBox
from PyQt4.QtCore import Qt
# plugin specific python modules
import config
from plugin_settings import Ui_PluginSettingsDialog
from base_classes import tr

class PluginSettingsDialog(QDialog):
    """ Class for plugin settings dialog
    """
    def __init__(self):
        """ Initialize dialog data and event handlers
        """
        super(PluginSettingsDialog, self).__init__()
        self.ui = Ui_PluginSettingsDialog()
        self.ui.setupUi(self)
        self.setWindowModality(Qt.ApplicationModal)

        # event handlers
        self.ui.HomeDirButton.clicked.connect(self.onHomeDirButton)
        self.ui.LogDirButton.clicked.connect(self.onLogDirButton)
        self.ui.OKButton.clicked.connect(self.onOKButton)
        self.ui.CancelButton.clicked.connect(self.onCancelButton)

        self.fillWidgets()

    def fillWidgets(self):
        """ Fill all widgets of Plugins Settings dialog.
        """
        self.ui.HomeDirEdit.setText(config.homedir)
        self.ui.LogDirEdit.setText(config.log_path)
        self.ui.LineToleranceEdit.setText("%f"%config.line_tolerance)
        self.ui.AreaToleranceEdit.setText("%f"%config.area_tolerance)
        self.ui.MaxIterationEdit.setText("%d"%config.max_iteration)

    def onHomeDirButton(self):
        """ Change the home directory where fieldbooks are stored.
        """
        path = QFileDialog.getExistingDirectory(self, 
                        tr("Select Home Directory"),
                        self.ui.HomeDirEdit.text(),
                        QFileDialog.ShowDirsOnly)
        if path!="":
            self.ui.HomeDirEdit.setText(path)

    def onLogDirButton(self):
        """ Change the directory of the log file.
        """
        path = QFileDialog.getExistingDirectory(self, 
                        tr("Select Log Directory"),
                        self.ui.LogDirEdit.text(),
                        QFileDialog.ShowDirsOnly)
        if path!="":
            self.ui.LogDirEdit.setText(path)

    def onOKButton(self):
        """ Close dialog. The changes will be saved.
        """
        config.homedir = self.ui.HomeDirEdit.text()
        config.log_path = self.ui.LogDirEdit.text()
        try:
            config.line_tolerance = float(self.ui.LineToleranceEdit.text())
        except (ValueError):
            QMessageBox.warning(self, tr("Warning"), tr("Snap tolerance must be a positive float value in layer units!"))
            self.ui.LineToleranceEdit.setFocus()
            return
        if config.line_tolerance<=0.0:
            QMessageBox.warning(self, tr("Warning"), tr("Snap tolerance must be a positive float value in layer units!"))
            self.ui.LineToleranceEdit.setFocus()
            return
        try:
            config.area_tolerance = float(self.ui.AreaToleranceEdit.text())
        except (ValueError):
            QMessageBox.warning(self, tr("Warning"), tr("Area tolerance must be a positive float value in layer units!"))
            self.ui.AreaToleranceEdit.setFocus()
            return
        if config.area_tolerance<=0.0:
            QMessageBox.warning(self, tr("Warning"), tr("Area tolerance must be a positive float value in layer units!"))
            self.ui.AreaToleranceEdit.setFocus()
            return
        try:
            config.max_iteration = int(self.ui.MaxIterationEdit.text())
        except (ValueError):
            QMessageBox.warning(self, tr("Warning"), tr("Maximum iteration must be a positive integer value!"))
            self.ui.MaxIterationEdit.setFocus()
            return
        if config.max_iteration<=0:
            QMessageBox.warning(self, tr("Warning"), tr("Maximum iteration must be a positive integer value!"))
            self.ui.MaxIterationEdit.setFocus()
            return
        # TODO store data from widgets 
        self.accept()

    def onCancelButton(self):
        """ Cancel dialog. The changes won't be saved.
        """
        self.reject()
