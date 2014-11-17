#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: surveying_util.py
    :platform: Linux/Windows
    :synopsis: Utility module for Land Surveying Plug-in for QGIS
    GPL v2.0 license
    Copyright (C) 2014-  DgiKom Kft. http://digikom.hu
    .. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""
from qgis.core import *
import re
from base_classes import *
# debugging
from PyQt4.QtCore import pyqtRemoveInputHook
import pdb

def get_namelist(pattern):
    """
        Find layers matching name with the pattern
        :parameter pattern: regexp pattern for layer name
        :return list of matching names or None
    """
    w = []
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.type() == QGis.Point and re.search(pattern, layer.name()):
            w.append(layer.name())
    if len(w):
        return w
    return None

def get_coordlist():
    """
        Find the coordinate list point shape in the actual project
        :return layer name or None
    """
    return get_namelist('^coord_')

def get_fblist():
    """
        Find the fieldbook tables in the actual project
        :return layer name or None
    """
    return get_namelist('^fb_')

def get_layer_by_name(name):
    """
        Look for a layer object by name
        :parameter name: name of the layer
        :return layer object 
    """
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for n, layer in layermap.iteritems():
        if layer.name() == name:
            if layer.isValid():
                return layer
            else:
                return None
    return None

def get_fieldlist(vlayer):
    """
        Create a list of fields
        :parameter vlayer: vector layer
        :return list of fields
    """
    vprovider = vlayer.dataProvider()
    # feat = QgsFeature()
    allAttrs = vprovider.attributeIndexes()
    vprovider.select(allAttrs)
    myFields = vprovider.fields()
    return myFields

def get_fieldnames(vlayer):
    """
        Create a list from column names of a vector layer
        :paramter vlayer: vector layer
        :return sorted list of field names
    """
    fieldmap = get_fieldlist(vlayer)
    fieldlist = []
    for name, field in fieldmap.iteritems():
        if not field.name() in fieldlist:
            fieldlist.append(unicode(field.name()))
    return sorted(fieldlist)

def get_coord(p):
    """
        DEPRICATED SEE QPoint class!!!!!!
        Get the coordinates of a point 
        :parameter p: point number
        :return Point object with coordinates
    """
    coord_lists = get_coordlist()
    if coord_lists is None:
        return None
    for coord_list in coord_lists:
        lay = get_layer_by_name(coord_list)
        if lay is None:
            continue
        for feat in lay.getFeatures():
            if feat['point_id'] ==  p:
                return Point(p, feat['e'], feat['n'], feat['z'], feat['pc'], feat['pt'])
    return None

def get_known(dimension=2):
    """
        Get list of known points
        :param dimension: 1/2/3 point dimension
        :returns list of point ids
    """
    plist = []
    coord_lists = get_coordlist()
    if coord_lists is None:
        return None
    for coord_list in coord_lists:
        lay = get_layer_by_name(coord_list)
        if lay is None:
            continue
        for feat in lay.getFeatures():
            if (dimension == 1 and feat['z'] != NULL) or \
               (dimension == 2 and feat['e'] != NULL and feat['n'] != NULL) or \
               (dimension == 3 and feat['e'] != NULL and feat['n'] != NULL and feat['z'] != NULL):
                if not feat['point_id'] in plist:
                    plist.append(feat['point_id'])
    if len(plist):
        return sorted(plist)
    return None
    
def get_unknown(dimension=2):
    """
        Get list of unknown points
        :param dimension: 1/2/3 point dimension
        :returns list of point ids
    """
    plist = []
    fb_list = get_fblist()
    if fb_list is None:
        return None
    for fb in fb_list:
        lay = get_layer_by_name(fb)
        if lay is None:
            continue
        for feat in lay.getFeatures():
            if re.match('station_', feat['point_id']):
                pid = feat['point_id'][8:]
            else:
                pid = feat['point_id']
            p = get_coord(pid)
            if (p is None) or \
               (dimension == 1 and p.z == NULL) or \
               (dimension == 2 and p.e == NULL and p.n == NULL) or \
               (dimension == 3 and p.e == NULL and p.n == NULL and p.z == NULL):
                if not pid in plist:
                    plist.append(pid)
    if len(plist):
        return sorted(plist)
    return None

def get_stations(known=False):
    """
        Get list of stations from fieldbooks
        :returns list of station [[point_id fieldbook_name id] ...]
    """
    slist = []
    fb_list = get_fblist()
    if fb_list is None:
        return None
    if known:
        known_list = get_known()
    for fb in fb_list:
        lay = get_layer_by_name(fb)
        if lay is None:
            continue
        for feat in lay.getFeatures():
            if feat['station'] == "station":
                pid = feat['point_id']
                if known and not pid in known_list:
                    # skip unknown points
                    continue
                id = feat['id']
                act = [pid, fb, id]
                if not act in slist:
                    slist.append(act)
    if len(slist):
        return sorted(slist)
    return None

class QPoint(Point):
    """
        Extended point class to store table position
    """

    def __init__(self, p, coo=None):
        """
            :parameter p: Point object (Point) or a point_id (String)
            :parameter coo: name of the table where point is/to be store (String)
                it is None if a new point to add
        """
        super(QPoint, self).__init__(p.id, p.e, p.n, p.z, p.pc, p.pt)
        self.coo = coo

    def get_coord(self):
        """
            Get the coordinates of the point from coord table and
            update coordinate fields
        """
        coord_lists = get_coordlist()
        if coord_lists is None:
            self.e = None
            self.n = None
            self.z = None
            self.pc = None
            self.pt = None
            self.coo = None
            return
        for coord_list in coord_lists:
            lay = get_layer_by_name(coord_list)
            if lay is None:
                continue
            for feat in lay.getFeatures():
                if feat['point_id'] ==  self.id:
                    self.e = feat['e']
                    self.n = feat['n']
                    self.z = feat['z']
                    self.pc = feat['pc']
                    self.pt = feat['pt']
                    self.coo = coord_list
                    return
        self.e = None
        self.n = None
        self.z = None
        self.pc = None
        self.pt = None
        self.coo = None
        return

    def store_coord(self, dimension=3):
        """
            Update coordinates in coord table, insert new point if 
            coo is None
            :param dimension: 1/2/3D coordinates to store
        """
        if self.coo is None:
            # new point to add to the first table
            cl = get_coordlist()
            if cl is None:
                return False

            self.coo = cl[0]
        lay = get_layer_by_name(self.coo)
        if lay is None:
            return False
        for feat in lay.getFeatures():
            if feat['point_id'] ==  self.id:
                # set feature geometry and attributes
                #pyqtRemoveInputHook()
                #pdb.set_trace()
                fid = feat.id()
                # TODO handle dimension!
                attrs = {feat.fieldNameIndex('point_id') : self.id,
                    feat.fieldNameIndex('e') : self.e,
                    feat.fieldNameIndex('n') : self.n,
                    feat.fieldNameIndex('z') : self.z,
                    feat.fieldNameIndex('pc') : self.pc,
                    feat.fieldNameIndex('pt') : self.pt}
                lay.dataProvider().changeAttributeValues({ fid : attrs })
                # feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(self.e, self.n)))
                lay.dataProvider().changeGeometryValues({ fid : QgsGeometry.fromPoint(QgsPoint(self.e, self.n)) })
                # TODO refresh canvas
                return True
        # add new point
        feat = QgsFeature()
        #feat.setFields(lay.pendingFields(), True)
        #feat.setFields(lay.dataProvider().fields(), True)
        fields = lay.dataProvider().fields()
        feat.setFields(fields, True)
        #pyqtRemoveInputHook()
        #pdb.set_trace()
        feat.setAttribute(feat.fieldNameIndex('point_id'), self.id)
        if dimension in [2, 3]:
            feat.setAttribute(feat.fieldNameIndex('e'), self.e)
            feat.setAttribute(feat.fieldNameIndex('n'), self.n)
        if dimension in [1, 3]:
            feat.setAttribute(feat.fieldNameIndex('z'), self.z)
        feat.setAttribute(feat.fieldNameIndex('pc'), self.pc)
        feat.setAttribute(feat.fieldNameIndex('pt'), self.pt)
        feat.setGeometry(QgsGeometry.fromPoint(QgsPoint(self.e, self.n)))
        lay.dataProvider().addFeatures([feat])
        # TODO refresh canvas
    
    def set_coord(self, p):
        """
            Set the coordinates
            :param p: Point
        """
        self.point_id = p.id
        self.e = p.e
        self.n = p.n
        self.z = p.z
        self.pc = p.pc
        self.pt = p.pt
