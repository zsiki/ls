# -*- coding: utf-8 -*-
"""
.. module:: line_tool
    :platform: Linux, Windows
    :synopsis: rubber line drawing

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>

"""

from PyQt4.QtCore import Qt, SIGNAL
from qgis.core import *
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool

class LineMapTool(QgsMapToolEmitPoint):
    """ Class implements rubberband line tool for polygon division
    """
    def __init__(self, canvas):
        """ initialize rubberband line drawing
            :param canvas: canvas to draw on
        """
        self.canvas = canvas
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
        self.startPoint = self.toMapCoordinates(e.pos())
        self.endPoint = self.startPoint
        self.isEmittingPoint = True
        self.showLine(self.startPoint, self.endPoint)

    def canvasReleaseEvent(self, e):
        """ Handler to handle left button up, end rubberband line
            :param e: event
        """
        self.isEmittingPoint = False
        # print "Line:", self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y()

    def canvasMoveEvent(self, e):
        """ handler to handle mouse move event
            :param e: event
        """
        if not self.isEmittingPoint:
            return

        self.endPoint = self.toMapCoordinates(e.pos())
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
        self.deactivate()
        self.emit(SIGNAL("deactivated()"))
