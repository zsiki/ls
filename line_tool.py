# -*- coding: utf-8 -*-
"""
.. module:: line_tool
    :platform: Linux, Windows
    :synopsis: rubber line drawing

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>

"""
from math import fabs, atan2, atan, sin, cos, pi
from PyQt4.QtCore import Qt, SIGNAL, QSettings
from PyQt4.QtGui import QMessageBox
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool
from qgis.core import *
from qgis.utils import QGis

import config
from base_classes import tr
from area_dialog import AreaDialog
from coord_dialog import CoordDialog

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
        line_tolerance = float( QSettings().value("SurveyingCalculation/line_tolerance",config.line_tolerance) )
        self.layer.snapPoint(self.startPoint, line_tolerance)
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.showLine()

    def canvasReleaseEvent(self, e):
        """ Handler to handle left button up, end rubberband line

            :param e: event
        """
        self.isEmittingPoint = False
        if self.startPoint.x() == self.endPoint.x() or \
            self.startPoint.y() == self.endPoint.y():
            return
        self.divide()

    def canvasMoveEvent(self, e):
        """ handler to handle mouse move event

            :param e: event
        """
        if not self.isEmittingPoint:
            return

        line_tolerance = float( QSettings().value("SurveyingCalculation/line_tolerance",config.line_tolerance) )

        self.endPoint = self.toMapCoordinates(e.pos())
        self.layer.snapPoint(self.endPoint, line_tolerance)
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

    def divide(self):
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
        if geom is None:
            return
        save_geom = QgsGeometry(geom)   # save original geometry
        # change to layer coordinates
        point1 = self.toLayerCoordinates(self.layer, QgsPoint(self.startPoint.x(), self.startPoint.y()))
        point2 = self.toLayerCoordinates(self.layer, QgsPoint(self.endPoint.x(), self.endPoint.y()))
        # show coordinates to change
        coord_dlg = CoordDialog(point1, point2)
        if not coord_dlg.exec_():
            return

        point1 = QgsPoint(float(coord_dlg.ui.StartEast.text()), \
                          float(coord_dlg.ui.StartNorth.text()))
        point2 = QgsPoint(float(coord_dlg.ui.EndEast.text()), \
                          float(coord_dlg.ui.EndNorth.text()))
        # center of rotation
        point0 = point1
        rotate = True
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
            if QMessageBox.question(self.iface.mainWindow(), \
                tr("Question"), tr("Line does not intersects polygon, line will be shifted into the polygon. Do you want to continue?"), \
                QMessageBox.Yes, QMessageBox.No) == QMessageBox.No:
                return
            # find an internal point
            if QGis.QGIS_VERSION > '2.4':
                cp = geom.pointOnSurface().vertexAt(0)
            else:
                cp = geom.centroid().vertexAt(0)
            # offset line to go through cp
            dx = point2.x() - point1.x()
            dy = point2.y() - point1.y()
            point0 = QgsPoint(cp.x(), cp.y())
            point1 = QgsPoint(cp.x() - 1000.0 * dx, cp.y() - 1000.0 * dy)
            point2 = QgsPoint(cp.x() + 1000.0 * dx, cp.y() + 1000.0 * dy) 
            rotate = False
        # divide polygon
        result, new_geoms, test_points = geom.splitGeometry([point1, point2], True)
        if result != 0:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("Area division failed ") + str(result))
            return
        # open modal dialog
        area_dlg = AreaDialog(save_geom.area(), geom.area(), rotate)
        if not area_dlg.exec_():
            return
        area = float(area_dlg.ui.AreaLineEdit.text())
        rotate = area_dlg.ui.OnePointRadio.isChecked()
        if save_geom.area() <= area:
            QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("Area of polygon is smaller then requested area"))
            return
        
        area_tolerance = float( QSettings().value("SurveyingCalculation/area_tolerance",config.area_tolerance) )
        max_iteration = int( QSettings().value("SurveyingCalculation/max_iteration",config.max_iteration) )

        i = 0
        #l = ((point2.x() - point1.x())**2 + (point2.y() - point1.y())**2)**0.5
        while True:
            da = geom.area() - area
            if fabs(da) <= area_tolerance:
                break;               # area OK exit loop
            # length of intersection
            geom_line = QgsGeometry.fromPolyline([point1, point2])
            section = save_geom.intersection(geom_line)
            l = section.length()     # section length
            dir = atan2(point2.x() - point0.x(), point2.y() - point0.y())
            if rotate:               # change line direction
                b = da * 2.0 / l
                dir += atan(b/l)
                point1 = QgsPoint(point0.x() + sin(dir + pi) * 1000.0, \
                    point0.y() + cos(dir + pi) * 1000.0)
                point2 = QgsPoint(point0.x() + sin(dir) * 1000.0, \
                    point0.y() + cos(dir) * 1000.0)
            else:                    # offset line
                # perpendicular direction to line
                b = da / l       # approximate offset
                dir += pi / 2.0  # perpendicular dir
                point1 = QgsPoint(point1.x() + sin(dir) * b, \
                    point1.y() + cos(dir) * b)
                point2 = QgsPoint(point2.x() + sin(dir) * b, \
                    point2.y() + cos(dir) * b)
            i += 1
            if i > max_iteration:
                QMessageBox.warning(self.iface.mainWindow(), tr("Warning"), tr("Area division not finished after max iteration") + str(result))
                return
            geom = QgsGeometry(save_geom)     # continue from original geomerty
            while geom.contains(point1):
                # extend line outside polygon
                point1 = QgsPoint(point1.x() - (point2.x() - point1.x()) * 10, \
                    point1.y() - (point2.y() - point1.y()) * 10)
            while geom.contains(point2):
                # extend line outside polygon
                point2 = QgsPoint(point2.x() + (point2.x() - point1.x()) * 10, \
                    point2.y() + (point2.y() - point1.y()) * 10)
            result, new_geoms, test_points = geom.splitGeometry([point1, point2], True)
        # refresh old geometry
        fid = feat.id()
        self.layer.dataProvider().changeGeometryValues({ fid : geom})
        # add new feature
        feat_new = QgsFeature()
        fields = self.layer.dataProvider().fields()
        feat_new.setFields(fields, True)
        # combine new_geoms to single geometry
        new_geom = QgsGeometry(new_geoms[0])
        for new_g in new_geoms[1:]:
            new_geom = QgsGeometry(new_geom.combine(new_g))
        feat_new.setGeometry(new_geom)
        self.layer.dataProvider().addFeatures([feat_new])
        # refresh canvas
        self.canvas.refresh()
