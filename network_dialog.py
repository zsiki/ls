from PyQt4.QtGui import QDialog
from network_calc import Ui_NetworkCalcDialog

class NetworkDialog(QDialog):
    """
        Class for network calculation dialog
    """
    def __init__(self):
        super(NetworkDialog, self).__init__()
        self.ui = Ui_NetworkCalcDialog()
        self.ui.setupUi(self)
        self.ui.CloseButton.clicked.connect(self.onCloseButton)

    def showEvent(self, event):
        """ set up initial state of dialog
        """
        pass

    def onCloseButton(self):
        self.accept()

