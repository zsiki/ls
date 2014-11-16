from PyQt4.QtGui import QDialog
from PyQt4.QtCore import QObject
# debugging
from PyQt4.QtCore import pyqtRemoveInputHook
import pdb

from simple_calc import Ui_SimpleCalcDialog
from surveying_util import *

class SimpleDialog(QDialog):
    """
        Class for single point calculation dialog (intersection, resection, ...)
    """
    def __init__(self):
        super(SimpleDialog, self).__init__()
        self.ui = Ui_SimpleCalcDialog()
        self.ui.setupUi(self)
        # event handlers
        self.ui.OrientRadio.toggled.connect(self.orient_clicked)

    def showEvent(self, event):
        """
            Reset dialog to initial state
        """
        # reset radio buttons
        self.ui.OrientRadio.setChecked(False)
        self.ui.RadialRadio.setChecked(False)
        self.ui.IntersectRadio.setChecked(False)
        self.ui.ResectionRadio.setChecked(False)
        self.ui.FreeRadio.setChecked(False)
        # reset result text
        self.ui.TextBrowser.clear()

    def orient_clicked(self, enabled):
        """
            Change dialog controls for orientation
            :param enable: True/False (Bool)
        """
        if enabled:
            self.ui.TextBrowser.append('orient')
            # fill station1 combo
            self.ui.Station1Combo.clear()
            st = get_stations(True)
            for s in st:
                self.ui.Station1Combo.addItem(s[0])
            self.ui.Station2Combo.clear()
