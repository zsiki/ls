from PyQt4.QtGui import QDialog
from network_calc import Ui_NetworkCalcDialog
from surveying_util import *
from gama_interface import *
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
        # event handling
        self.ui.CloseButton.clicked.connect(self.onCloseButton)
        self.ui.ResetButton.clicked.connect(self.onResetButton)
        self.ui.AddFixButton.clicked.connect(self.onAddFixButton)
        self.ui.AddAdjButton.clicked.connect(self.onAddAdjButton)
        self.ui.RemoveFixButton.clicked.connect(self.onRemoveFixButton)
        self.ui.RemoveAdjButton.clicked.connect(self.onRemoveAdjButton)
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
        self.points = get_measured()
        self.fix = []
        self.adj = []
        # clear lists
        self.ui.PointsList.clear()
        self.ui.FixList.clear()
        self.ui.AdjustedList.clear()
        self.ui.ResultTextBrowser.clear()
        if self.points is not None:
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

    def onCalcButton(self):
        if len(self.adj):
            dimension = int(self.ui.DimensionComboBox.currentText())
            conf = float(self.ui.ConfidenceComboBox.currentText())
            stda = float(self.ui.AngleDevComboBox.currentText())
            stdd = float(self.ui.DistDevMMComboBox.currentText())
            stdd1 = float(self.ui.DistDevMMKMComboBox.currentText())
            g = GamaInterface(dimension, conf, stda, stdd, stdd1)
            # add points to adjustment
            fix_names = []
            adj_names = []
            for fp in self.fix:
                p = get_coord(fp[0])
                g.add_point(p, 'FIX')
                fix_names.append(fp[0])
            for fp in self.adj:
                p = get_coord(fp[0])
                if p is None:
                    p = Point(fp[0])
                g.add_point(p, 'ADJ')
                adj_names.append(fp[0])
            # add observations to adjustment
            fb_list = get_fblist()
            if fb_list is None:
                return None
            for fb in fb_list:
                lay = get_layer_by_name(fb)
                if lay is None:
                    continue
                st = None
                for feat in lay.getFeatures():
                    pid = feat['point_id']
                    if feat['station'] == 'station':
                        st = None
                        if pid in fix_names or pid in adj_names:
                            st = pid
                            o = PolarObservation(pid, feat['station'])
                            o.th = feat['th'] if type(feat['th']) is float else None
                            o.pc = feat['pc'] if type(feat['pc']) is str else None
                            g.add_observation(o)
                            # TODO empty station? without observation
                    else:
                        if st is not None and (pid in fix_names or pid in adj_names):
                            if dimension in [2, 3] and (type(feat['hz']) is float or \
                                type(feat['v']) is float and type(feat['sd']) is float) or \
                                dimension == 1 and type(feat['v']) is float and \
                                type(feat['sd']):
                                o = PolarObservation(pid, None)
                                o.hz = Angle(feat['hz'], 'GON') if type(feat['hz']) is float else None
                                o.v = Angle(feat['v'], 'GON') if type(feat['v']) is float else None
                                if type(feat['sd']) is float and \
                                    (st in adj_names or pid in adj_names):
                                    # add distance if one end is unknown
                                    o.sd = Distance(feat['sd'], 'SD')
                                o.th = feat['th'] if type(feat['th']) is float else None
                                o.pc = feat['pc'] if type(feat['pc']) is str else None
                                g.add_observation(o)
            t = g.adjust()
            self.ui.ResultTextBrowser.append(t)
