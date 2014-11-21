from PyQt4.QtGui import QDialog
from transformation_calc import Ui_TransformationCalcDialog

from surveying_util import *

class TransformationDialog(QDialog):
    """
        Class for transformation calculation dialog
    """
    def __init__(self):
        super(TransformationDialog, self).__init__()
        self.ui = Ui_TransformationCalcDialog()
        self.ui.setupUi(self)
        self.from_points = get_known()
        self.to_points = []
        self.from_points = []
        self.common = []
        self.used = []
        self.ui.CloseButton.clicked.connect(self.onCloseButton)
        self.ui.ResetButton.clicked.connect(self.onResetButton)
        self.ui.ToFileButton.clicked.connect(self.onToFileButton)
        self.ui.AddButton.clicked.connect(self.onAddButton)
        self.ui.RemoveButton.clicked.connect(self.onRemoveButton)
        self.ui.CalcButton.clicked.connect(self.onCalcButton)

    def showEvent(self, event):
        """
            set up initial state of dialog
        """
        self.reset()

    def reset(self):
        """
            Reset dialog to initial state
        """
        # fill from list
        self.ui.FromLayerComboBox.clear()
        clist = get_coordlist()
        if clist is not None:
            self.ui.FromLayerComboBox.addItems(clist)
        # clear to file
        self.ui.ToShapeEdit.setText('')
        # clear comon & used list
        self.ui.CommonList.clear()
        self.ui.UsedList.clear()
        # select orthogonal transformation
        self.ui.OrthogonalRadio.setChecked(True)

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

    def onToFileButton(self):
        """
            Select target shape file
        """
        fname = QFileDialog.getOpenFileName(self.iface.mainWindow(),
            self.tr('Coordinate list'),
            filter= self.tr('Coordinate list file (*.shp);;'))
        if fname:
            self.ui.ToShapeEdit.setText(fname)
            to_shp = QgsVectorLayer(fname, "tmp_to_shape", "ogr") 
            from_name = self.ui.FromLayerComboBox.currentText()
            if len(from_name):
                pass   # TODO 
        else:
            self.ui.ToShapeEdit.setText('')
            # clear comon & used list
            self.ui.CommonList.clear()
            self.ui.UsedList.clear()

    def onAddButton(self):
        """
            Add point to used point in transformation
        """
        pass
    
    def onRemoveButton(self):
        """
            Remove point from used points
        """
        pass

    def onCalcButton(self):
        """
            Start transformation calculation
        """
        pass
