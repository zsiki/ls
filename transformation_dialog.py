from PyQt4.QtGui import QDialog
from transformation_calc import Ui_TransformationCalcDialog

class TransformationDialog(QDialog):
    """
        Class for transformation calculation dialog
    """
    def __init__(self):
        super(TransformationDialog, self).__init__()
        self.ui = Ui_TransformationCalcDialog()
        self.ui.setupUi(self)
