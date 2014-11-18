from PyQt4.QtGui import QDialog
from network_calc import Ui_NetworkCalcDialog
from surveying_util import *
# debugging
from PyQt4.QtCore import pyqtRemoveInputHook
import pdb


class NetworkDialog(QDialog):
    """
        Class for network calculation dialog
    """
    def __init__(self):
        super(NetworkDialog, self).__init__()
        self.ui = Ui_NetworkCalcDialog()
        self.ui.setupUi(self)
        self.points = []
        self.fix = []
        self.adj = []
        # set original state
        # event handling
        self.ui.CloseButton.clicked.connect(self.onCloseButton)
        self.ui.ResetButton.clicked.connect(self.onResetButton)
        self.ui.AddFixButton.clicked.connect(self.onAddFixButton)
        self.ui.AddAdjButton.clicked.connect(self.onAddAdjButton)
        self.ui.RemoveFixButton.clicked.connect(self.onRemoveFixButton)
        self.ui.RemoveAdjButton.clicked.connect(self.onRemoveAdjButton)


    def showEvent(self, event):
        """ set up initial state of dialog
        """
        self.reset()

    def reset(self):
        """
            Reset dialog to initial state
        """
        self.points = get_measured()
        self.fix = []
        self.adj = []
        # clear lists
        self.ui.PointsList.clear()
        self.ui.FixList.clear()
        self.ui.AdjustedList.clear()
        self.ui.ResultTextBrowser.clear()
        for p in self.points:
            self.ui.PointsList.addItem(p[0])

    def onCloseButton(self):
        """
            Close dialog after Close button pressed
        """
        self.accept()

    def onResetButton(self):
        """
            Reset dialog to initial state after Reset button pressed
        """
        self.reset()

    def onAddFixButton(self):
        i = self.ui.PointsList.currentRow()
        if i < 0:
            return
        if self.points[i][1]:
            # has coordinates
            item = self.ui.PointsList.takeItem(i)
            self.ui.FixList.addItem(item)
            self.fix.append(self.points[i])
            del self.points[i]

    def onAddAdjButton(self):
        i = self.ui.PointsList.currentRow()
        if i < 0:
            return
        item = self.ui.PointsList.takeItem(i)
        self.ui.AdjustedList.addItem(item)
        self.adj.append(self.points[i])
        del self.points[i]

    def onRemoveFixButton(self):
        i = self.ui.FixList.currentRow()
        if i < 0:
            return
        item = self.ui.FixList.takeItem(i)
        self.ui.PointsList.addItem(item)
        self.points.append(self.points[i])
        del self.fix[i]

    def onRemoveAdjButton(self):
        i = self.ui.AdjustedList.currentRow()
        if i < 0:
            return
        item = self.ui.AdjustedList.takeItem(i)
        self.ui.PointsList.addItem(item)
        self.adj.append(self.points[i])
        del self.adj[i]

