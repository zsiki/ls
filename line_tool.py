# -*- coding: utf-8 -*-
"""
.. module:: line_tool
    :platform: Linux, Windows
    :synopsis: rubber line drawing

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>

"""

from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QMessageBox
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool
from qgis.core import *

import config
from base_classes import tr
from area_dialog import AreaDialog

class LineMapTool(QgsMapToolEmitPoint):
    """ Class implements rubberband line tool for polygon division
    """
    def __init__(self, iface):
        """ initialize rubberband line drawing
            :param iface: interface to QGIS
        """
        self.iface = iface
        self.layer = None
        self.canvas = self.iface.mapCanvas()
        QgsMapToolEmitPoint.__init__(self, self.canvas)
        self.rubberBand = QgsRubberBand(self.canvas, QGis.Line)
        self.rubberBand.setColor(Qt.red)
        self.rubberBand.setWidth(1)
        self.reset()

    def reset(self):
        """ reset rubberband line tool to original state
        """
        self.startPoint = self.endPoint = None
        self.isEmittingPoint = False
        self.rubberBand.reset(QGis.Line)

    def canvasPressEvent(self, e):
        """ handler to handle left button down, start rubberband line

            :param e: event
        """
        al = self.iface.activeLayer()
        if al is None or al.type() != QgsMapLayer.VectorLayer or \
            al.geometryType() != 2:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("Actual layer contains no polygons"))
            return
        if len(al.selectedFeatures()) != 1:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("Not a single polygon is selected in active layer"))
            return
        self.layer = al
        self.startPoint = self.toMapCoordinates(e.pos())
        # snap to point on active layer
        self.layer.snapPoint(self.startPoint, config.tolerance)
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.showLine(self.startPoint, self.endPoint)

    def canvasReleaseEvent(self, e):
        """ Handler to handle left button up, end rubberband line

            :param e: event
        """
        self.isEmittingPoint = False
        area_dlg = AreaDialog()
        # show the dialog
        area_dlg.show()
        # run the dialog event loop
        if area_dlg.exec_():
            self.divide(float(area_dlg.ui.AreaLineEdit.text()), \
                area_dlg.ui.OnePointRadio.isChecked())

    def canvasMoveEvent(self, e):
        """ handler to handle mouse move event

            :param e: event
        """
        if not self.isEmittingPoint:
            return

        self.endPoint = self.toMapCoordinates(e.pos())
        self.layer.snapPoint(self.endPoint, config.tolerance)
        self.showLine(self.startPoint, self.endPoint)

    def showLine(self, startPoint, endPoint):
        """ Draw rubberband line

            :param startPoint: start point of line
            :param endPoint: end point of line
        """
        self.rubberBand.reset(QGis.Line)
        if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
            return
        point1 = QgsPoint(startPoint.x(), startPoint.y())
        point2 = QgsPoint(endPoint.x(), endPoint.y())
        self.rubberBand.addPoint(point1, False)
        self.rubberBand.addPoint(point2, True)
        self.rubberBand.show()

    def deactivate(self):
        """ deactivate line tool
        """
        try:
            # TODO
            self.deactivate()
            self.emit(SIGNAL("deactivated()"))
        except TypeError:
            pass

    def divide(self, area, rotate):
        """ Divide the selected polygon.

            :param area: area to divide (float)
            :param rotate: rotate/offset True/False (bool)
        """
        pass
