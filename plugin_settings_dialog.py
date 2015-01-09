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

