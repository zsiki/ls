# -*- coding: utf-8 -*-
"""
.. module:: line_tool
    :platform: Linux, Windows
    :synopsis: rubber line drawing

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>

"""
from math import fabs
from PyQt4.QtCore import Qt, SIGNAL
from PyQt4.QtGui import QMessageBox
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool
from qgis.core import *
# debugging
from PyQt4.QtCore import pyqtRemoveInputHook
import pdb

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
        self.startPoint = None
        self.endPoint = None
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
        self.layer.snapPoint(self.startPoint, config.line_tolerance)
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.showLine()

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
        self.layer.snapPoint(self.endPoint, config.line_tolerance)
        self.showLine()

    def showLine(self):
        """ Draw rubberband line
        """
        self.rubberBand.reset(QGis.Line)
        if self.startPoint.x() == self.endPoint.x() or \
            self.startPoint.y() == self.endPoint.y():
            return
        self.rubberBand.addPoint(self.startPoint, False)
        self.rubberBand.addPoint(self.endPoint, True)
        self.rubberBand.show()

    def deactivate(self):
        """ deactivate line tool
        """
        try:
            self.rubberBand.reset(QGis.Line)           # erase rubberband line
        except:
            pass
        super(LineMapTool, self).deactivate()
        self.emit(SIGNAL("deactivated()"))

    def divide(self, area, rotate):
        """ Divide the selected polygon.

            :param area: area to divide (float)
            :param rotate: rotate/offset True/False (bool)
        """
        selection = self.layer.selectedFeatures()
        if len(selection) != 1:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("Not a single polygon is selected in active layer"))
            return
        feat = selection[0]             # feature to divide
        geom = feat.geometry()
        if geom.area() <= area:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("Area of polygon is smaller then requested area"))
            return
        # TODO multipart ?
        # change to layer coordinates
        point1 = self.toLayerCoordinates(self.layer, QgsPoint(self.startPoint.x(), self.startPoint.y()))
        point2 = self.toLayerCoordinates(self.layer, QgsPoint(self.endPoint.x(), self.endPoint.y()))
        while geom.contains(point1):
            # extend line outside polygon
            point1 = QgsPoint(point1.x() - (point2.x() - point1.x()) * 10, \
                point1.y() - (point2.y() - point1.y()) * 10)
        while geom.contains(point2):
            # extend line outside polygon
            point2 = QgsPoint(point2.x() + (point2.x() - point1.x()) * 10, \
                point2.y() + (point2.y() - point1.y()) * 10)
        geom_line = QgsGeometry.fromPolyline([point1, point2])  # divider
        if not geom.intersects(geom_line):
            # find an internal point
            if qgis.utils.QGis.QGIS_VERSION > '2.4':
                cp = feat.pointOnSurface()
            else:
                # TODO centroid may be outside
                cp = feat.centroid()
            if rotate:
                # move point2 to go through cp
                point2 = QgsPoint(point1.x() + (cp.x() - point1.x()) * 1000., self.point1.y() + (cp.y() - point1.y()) * 1000.)
                geom_line = QgsGeometry.fromPolyline([point1, point2])  # divider
            else:
                # offset line to go through cp
                dx = self.point2.x() - self.point1.x()
                dy = self.point2.y() - self.point1.y()
                point1 = QgsPoint(cp.x() - 2.0 * dx, cp.y() - 2.0 * dy)
                point2 = QgsPoint(cp.y() + 2.0 * dx, cp.y() + 2.0 * dy) 
                geom_line = QgsGeometry.fromPolyline([point1, point2])  # divider
        save_geom = geom      # save original geometry
        #pyqtRemoveInputHook()
        #pdb.set_trace()

        while True:
            # divide polygon
            result, new_geoms, test_points = geom.splitGeometry([point1, point2], True)
            if result != 0:
                QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("Area division failed ") + str(result))
                return
            if fabs(geom.area() - area) <= config.area_tolerance:
                break;               # area OK exit loop
            if rotate:               # change line direction
                pass
            else:                    # offset line
                pass
            geom = save_geom         # continue from original geomerty
            # calculate area
            for g in new_geoms:
                print g.area()
            break
        # refresh old geometry
        fid = feat.id()
        self.layer.dataProvider().changeGeometryValues({ fid : geom})
        # add new feature
        feat_new = QgsFeature()
        fields = self.layer.dataProvider().fields()
        feat_new.setFields(fields, True)
        # TODO new_geoms to multipart
        feat_new.setGeometry(new_geoms[0])
