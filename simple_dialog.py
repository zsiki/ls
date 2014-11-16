from PyQt4.QtGui import QDialog
from simple_calc import Ui_SimpleCalcDialog

class SimpleDialog(QDialog):
    """
        Class for single point calculation dialog (intersection, resection, ...)
    """
    def __init__(self):
        super(SimpleDialog, self).__init__()
        ui = Ui_SimpleCalcDialog()
        ui.setupUi(self)
