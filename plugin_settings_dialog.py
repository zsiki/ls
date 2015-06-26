# -*- coding: utf-8 -*-
"""
.. module:: plugin_settings_dialog
    :platform: Linux, Windows
    :synopsis: GUI for SurveyingCalculation plugin settings

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>
"""
from PyQt4.QtGui import QDialog, QFileDialog, QMessageBox
from PyQt4.QtCore import Qt, QSettings, QVariant
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
        self.ui.GamaDirButton.clicked.connect(self.onGamaDirButton)
        self.ui.OKButton.clicked.connect(self.onOKButton)
        self.ui.CancelButton.clicked.connect(self.onCancelButton)

        self.fillWidgets()

    def fillWidgets(self):
        """ Fill all widgets of Plugins Settings dialog.
        """
        QSettings().value("SurveyingCalculation/fontname",config.fontname)
        QSettings().value("SurveyingCalculation/fontsize",config.fontsize)
        self.ui.HomeDirEdit.setText(QSettings().value("SurveyingCalculation/homedir",config.homedir))
        self.ui.LogDirEdit.setText(QSettings().value("SurveyingCalculation/log_path",config.log_path))
        self.ui.GamaDirEdit.setText(QSettings().value("SurveyingCalculation/gama_path",config.gama_path))
        self.ui.LineToleranceEdit.setText("%f"%float( QSettings().value("SurveyingCalculation/line_tolerance",config.line_tolerance) ))
        self.ui.AreaToleranceEdit.setText("%f"%float( QSettings().value("SurveyingCalculation/area_tolerance",config.area_tolerance) ))
        self.ui.MaxIterationEdit.setText("%d"%int( QSettings().value("SurveyingCalculation/max_iteration",config.max_iteration) ))

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

    def onGamaDirButton(self):
        """ Change the directory of the gama-local executable.
        """
        path = QFileDialog.getExistingDirectory(self, 
                        tr("Select GNU Gama Directory"),
                        self.ui.GamaDirEdit.text(),
                        QFileDialog.ShowDirsOnly)
        if path!="":
            self.ui.GamaDirEdit.setText(path)

    def onOKButton(self):
        """ Close dialog. The changes will be saved.
        """
        # check values in widgets
        try:
            line_tolerance = float(self.ui.LineToleranceEdit.text())
        except (ValueError):
            QMessageBox.warning(self, tr("Warning"), tr("Snap tolerance must be a positive float value in layer units!"))
            self.ui.LineToleranceEdit.setFocus()
            return
        if line_tolerance<=0.0:
            QMessageBox.warning(self, tr("Warning"), tr("Snap tolerance must be a positive float value in layer units!"))
            self.ui.LineToleranceEdit.setFocus()
            return
        try:
            area_tolerance = float(self.ui.AreaToleranceEdit.text())
        except (ValueError):
            QMessageBox.warning(self, tr("Warning"), tr("Area tolerance must be a positive float value in layer units!"))
            self.ui.AreaToleranceEdit.setFocus()
            return
        if area_tolerance<=0.0:
            QMessageBox.warning(self, tr("Warning"), tr("Area tolerance must be a positive float value in layer units!"))
            self.ui.AreaToleranceEdit.setFocus()
            return
        try:
            max_iteration = int(self.ui.MaxIterationEdit.text())
        except (ValueError):
            QMessageBox.warning(self, tr("Warning"), tr("Maximum iteration must be a positive integer value!"))
            self.ui.MaxIterationEdit.setFocus()
            return
        if max_iteration<=0:
            QMessageBox.warning(self, tr("Warning"), tr("Maximum iteration must be a positive integer value!"))
            self.ui.MaxIterationEdit.setFocus()
            return

        # store settings
# TODO store font setting from widgets
        QSettings().setValue("SurveyingCalculation/fontname","DejaVu Sans Mono")
        QSettings().setValue("SurveyingCalculation/fontsize",9)
        QSettings().setValue("SurveyingCalculation/homedir",self.ui.HomeDirEdit.text())
        QSettings().setValue("SurveyingCalculation/log_path",self.ui.LogDirEdit.text())
        QSettings().setValue("SurveyingCalculation/gama_path",self.ui.GamaDirEdit.text())
        QSettings().setValue("SurveyingCalculation/line_tolerance",line_tolerance)
        QSettings().setValue("SurveyingCalculation/area_tolerance",area_tolerance)
        QSettings().setValue("SurveyingCalculation/max_iteration",max_iteration)
        QSettings().sync()

        self.accept()

    def onCancelButton(self):
        """ Cancel dialog. The changes won't be saved.
        """
        self.reject()
