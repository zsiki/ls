# -*- coding: utf-8 -*-
"""
.. module:: plugin_settings_dialog
    :platform: Linux, Windows
    :synopsis: GUI for SurveyingCalculation plugin settings

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>
"""
from PyQt4.QtGui import QDialog
# plugin specific python modules
import config
from plugin_settings import Ui_PluginSettingsDialog

class PluginSettingsDialog(QDialog):
    """ Class for plugin settings dialog
    """
    def __init__(self):
        """ Initialize dialog data and event handlers
        """
        super(PluginSettingsDialog, self).__init__()
        self.ui = Ui_PluginSettingsDialog()
        self.ui.setupUi(self)
        self.ui.OutputTab.setCurrentIndex(2)

        # event handlers
        self.ui.HomeDirButton.clicked.connect(self.onHomeDirButton)
        self.ui.LogDirButton.clicked.connect(self.onLogDirButton)
        self.ui.OKButton.clicked.connect(self.onOKButton)
        self.ui.CancelButton.clicked.connect(self.onCancelButton)

    def showEvent(self, event):
        """ Reset dialog when receives a show event.
        """
        self.fillWidgets()
        
    def fillWidgets(self):
        """ Fill all widgets of Plugins Settings dialog.
        """
        pass

    def onHomeDirButton(self):
        """ Change the home directory where fieldbooks are stored.
        """
        pass

    def onLogDirButton(self):
        """ Change the directory of the log file.
        """
        pass

    def onOKButton(self):
        """ Close dialog. The changes will be saved.
        """
        pass

    def onCancelButton(self):
        """ Cancel dialog. The changes won't be saved.
        """
        pass
