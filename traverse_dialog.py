from PyQt4.QtGui import QDialog
from traverse_calc import Ui_TraverseCalcDialog
from surveying_util import *
from calculation import Calculation
from base_classes import ResultLog

class TraverseDialog(QDialog):
    """
        Class for traverse calculation dialog
    """
    def __init__(self):
        super(TraverseDialog, self).__init__()
        self.ui = Ui_TraverseCalcDialog()
        self.ui.setupUi(self)

        self.ui.AddButton.clicked.connect(self.onAddButton)
        self.ui.RemoveButton.clicked.connect(self.onRemoveButton)
        self.ui.UpButton.clicked.connect(self.onUpButton)
        self.ui.DownButton.clicked.connect(self.onDownButton)
        self.ui.CalcButton.clicked.connect(self.onCalcButton)
        self.ui.ResetButton.clicked.connect(self.onResetButton)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)

    def showEvent(self, event):
        """
            Reset dialog when receives a show event.
        """
        self.reset()

    def reset(self):
        """
            Reset dialog to initial state
        """
        # reset radio buttons
        self.ui.buttonGroup.setExclusive(False)
        self.ui.ClosedRadio.setChecked(False)
        self.ui.LinkRadio.setChecked(False)
        self.ui.OpenRadio.setChecked(False)
        self.ui.buttonGroup.setExclusive(True)

        # disable widgets
        self.ui.StartPointComboBox.setEnabled(False)
        self.ui.EndPointComboBox.setEnabled(False)

        # clear widgets
        self.ui.StartPointComboBox.clear()
        self.ui.EndPointComboBox.clear()
        self.ui.TargetList.clear()
        self.ui.OrderList.clear()
        self.ui.ResultTextBrowser.clear()

    def onAddButton(self):
        """
            Add selected target point to used points list.
        """
        self.ui.OrderList.addItem( self.ui.TargetList.takeItem( self.ui.TargetList.currentRow() ) )

    def onRemoveButton(self):
        """
            Remove selected used point and add to target points list.
        """
        self.ui.TargetList.addItem( self.ui.OrderList.takeItem( self.ui.OrderList.currentRow() ) )

    def onUpButton(self):
        """
            Add selected target point to used points list.
        """
        cur = self.ui.OrderList.currentRow()
        if cur>0:
            self.ui.OrderList.addItem( cur-1, self.ui.OrderList.takeItem( cur ) )
            self.ui.OrderList.setCurrentRow(cur-1)

    def onDownButton(self):
        """
            Add selected target point to used points list.
        """
        cur = self.ui.OrderList.currentRow()
        if cur<self.ui.OrderList.count()-1:
            self.ui.OrderList.addItem( cur+1, self.ui.OrderList.takeItem( cur ) )
            self.ui.OrderList.setCurrentRow(cur+1)

    def onCalcButton(self):
        """
            Start a calculation when the Calculate button pushed.
        """
        pass
    
    def onResetButton(self):
        """
            Reset dialog when the Reset button pushed.
        """
        self.reset()
    
    def onCloseButton(self):
        """
            Close the dialog when the Close button pushed.
        """
        self.accept()
