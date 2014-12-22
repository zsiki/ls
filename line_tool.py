#from PyQt4.QtGui import QColor
from PyQt4.QtCore import Qt, SIGNAL
from qgis.core import *
from qgis.gui import QgsMapToolEmitPoint, QgsRubberBand, QgsMapTool

class LineMapTool(QgsMapToolEmitPoint):
  def __init__(self, canvas):
      self.canvas = canvas
      QgsMapToolEmitPoint.__init__(self, self.canvas)
      self.rubberBand = QgsRubberBand(self.canvas, QGis.Line)
      self.rubberBand.setColor(Qt.red)
      self.rubberBand.setWidth(1)
      self.reset()

  def reset(self):
      self.startPoint = self.endPoint = None
      self.isEmittingPoint = False
      self.rubberBand.reset(QGis.Line)

  def canvasPressEvent(self, e):
      self.startPoint = self.toMapCoordinates(e.pos())
      self.endPoint = self.startPoint
      self.isEmittingPoint = True
      self.showLine(self.startPoint, self.endPoint)

  def canvasReleaseEvent(self, e):
      self.isEmittingPoint = False
      print "Line:", self.startPoint.x(), self.startPoint.y(), self.endPoint.x(), self.endPoint.y()

  def canvasMoveEvent(self, e):
      if not self.isEmittingPoint:
        return

      self.endPoint = self.toMapCoordinates(e.pos())
      self.showLine(self.startPoint, self.endPoint)

  def showLine(self, startPoint, endPoint):
      self.rubberBand.reset(QGis.Line)
      if startPoint.x() == endPoint.x() or startPoint.y() == endPoint.y():
        return

      point1 = QgsPoint(startPoint.x(), startPoint.y())
      point2 = QgsPoint(endPoint.x(), endPoint.y())

      self.rubberBand.addPoint(point1, False)
      self.rubberBand.addPoint(point2, True)
      self.rubberBand.show()

      #return QgsPolyline(self.startPoint, self.endPoint)

  def deactivate(self):
      # QgsMapTool.deactivate(self)
      self.emit(SIGNAL("deactivated()"))
