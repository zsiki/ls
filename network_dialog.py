from PyQt4.QtGui import QDialog
from network_calc import Ui_NetworkCalcDialog

class NetworkDialog(QDialog):
    """
        Class for network calculation dialog
    """
    def __init__(self):
        super(NetworkDialog, self).__init__()
        ui = Ui_NetworkCalcDialog()
        ui.setupUi(self)
