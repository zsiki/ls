from PyQt4.QtGui import QDialog
from traverse_calc import Ui_TraverseCalcDialog

class TraverseDialog(QDialog):
    """
        Class for traverse calculation dialog
    """
    def __init__(self):
        super(TraverseDialog, self).__init__()
        self.ui = Ui_TraverseCalcDialog()
        self.ui.setupUi(self)
