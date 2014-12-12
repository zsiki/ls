#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: surveying_util.py
    :platform: Linux/Windows
    :synopsis: Utility module for SurveyingCalculation Plug-in for QGIS

.. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""
from qgis.core import *
import re
from base_classes import *
# debugging
from PyQt4.QtCore import pyqtRemoveInputHook
import pdb

def get_namelist(pattern):
    """ Find layers matching name with the pattern

        :param pattern: regexp pattern for layer name (str)
        :returns: list of matching names or None
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
    """ Find the coordinate list point shape in the actual project

        :returns: layer name or None
    """
    return get_namelist('^coord_')

def get_fblist():
    """ Find the fieldbook tables in the actual project

        :returns: layer name or None
    """
    return get_namelist('^fb_')

def get_layer_by_name(name):
    """ Look for a layer object by name

        :param name: name of the layer (str)
        :returns: layer object 
    """
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for n, layer in layermap.iteritems():
        if layer.name() == name:
            if layer.isValid():
                return layer
            else:
                return None
    return None

def get_polygon_layers():
    """ Find layers with type of polygon

        :returns: list of names of polygon layers or None
    """
    w = []
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for n, layer in layermap.iteritems():
        if layer.type() == QgsMapLayer.VectorLayer:
            if layer.geometryType() == QGis.Polygon:
                w.append(layer.name())
    if len(w):
        return w
    return None

def get_fieldlist(vlayer):
    """ Create a list of fields

        :param vlayer: vector layer
        :returns: list of fields
    """
    vprovider = vlayer.dataProvider()
    allAttrs = vprovider.attributeIndexes()
    vprovider.select(allAttrs)
    myFields = vprovider.fields()
    return myFields

def get_fieldnames(vlayer):
    """ Create a list from column names of a vector layer

        :paramter vlayer: vector layer
        :returns: sorted list of field names
    """
    fieldmap = get_fieldlist(vlayer)
    fieldlist = []
    for name, field in fieldmap.iteritems():
        if not field.name() in fieldlist:
            fieldlist.append(unicode(field.name()))
    return sorted(fieldlist)

def get_coord(p, clist=None):
    """ Get the coordinates of a point 

        :param p: point number (str)
        :param clist: coordinate list to search for (str), optional
        :returns: Point object with coordinates
    """
    if clist is None:
        coord_lists = get_coordlist()
    else:
        coord_lists = [clist]
    if coord_lists is None:
        return None
    for coord_list in coord_lists:
        lay = get_layer_by_name(coord_list)
        if lay is None:
            continue
        for feat in lay.getFeatures():
            if feat['point_id'] ==  p:
                #return Point(p, feat['e'], feat['n'], feat['z'], feat['pc'], feat['pt'])
                pp = Point(p)
                if type(feat['e']) is float and type(feat['n']) is float:
                    pp.e = feat['e']
                    pp.n = feat['n']
                if type(feat['z']) is float:
                    pp.z = feat['z']
                if type(feat['pc']) is str:
                    p.pc = feat['pc']
                if type(feat['pt']) is str:
                    p.pt = feat['pt']
                return pp
    return None

def get_known(dimension=2, clist=None):
    """ Get list of known points

        :param dimension: 1/2/3 point dimension, default: 2
        :param clist: single coordinate list to search, default None (all lists)
        :returns: list of point ids
    """
    plist = []
    if clist is None:
        coord_lists = get_coordlist()
    else:
        coord_lists = [clist]
    if coord_lists is None:
        return None
    for coord_list in coord_lists:
        lay = get_layer_by_name(coord_list)
        if lay is None:
            continue
        for feat in lay.getFeatures():
            if (dimension == 1 and type(feat['z']) is float) or \
               (dimension == 2 and type(feat['e']) is float and type(feat['n']) is float) or \
               (dimension == 3 and type(feat['e']) is float and type(feat['n']) is float and type(feat['z']) is float):
                if not feat['point_id'] in plist:
                    plist.append(feat['point_id'])
    if len(plist):
        return sorted(plist)
    return None
    
def get_measured(dimension=2):
    """ Get list of unknown points

        :param dimension: 1/2/3 point dimension
        :returns: list of point ids
    """
    plist = []
    found = []
    fb_list = get_fblist()
    if fb_list is None:
        return None
    for fb in fb_list:
        lay = get_layer_by_name(fb)
        if lay is None:
            continue
        for feat in lay.getFeatures():
            pid = feat['point_id']
            p = get_coord(pid)
            if (p is None) or \
               (dimension == 1 and p.z is None) or \
               (dimension == 2 and (p.e is None  or p.n is None)) or \
               (dimension == 3 and (p.e is None or p.n is None or p.z is None)):
                coord = False
            else:
                coord = True
            if not pid in found:
                plist.append([pid, coord])
                found.append(pid)

    if len(plist):
        return sorted(plist)
    return None

def get_unknown(dimension=2):
    """ Get list of measured points

        :param dimension: 1/2/3 point dimension
        :returns: list of [point id, True/False], second element marks if point have coordinates of dimension
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
            pid = feat['point_id']
            p = get_coord(pid)
            if (p is None) or \
               (dimension == 1 and p.z is None) or \
               (dimension == 2 and (p.e is None or p.n is None)) or \
               (dimension == 3 and (p.e is None or p.n is None or p.z is None)):
                if not pid in plist:
                    plist.append(pid)
    if len(plist):
        return sorted(plist)
    return None

def get_stations(known=False, oriented=False):
    """ Get list of stations from fieldbooks

        :param known: If True only known points get into list.
        :param oriented: If True only oriented stations get into list.
        :returns: list of station [[point_id fieldbook_name id] ...]
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
                if known and known_list is not None and not pid in known_list:
                    # skip unknown points
                    continue
                if oriented and type(feat['hz']) is not float:
                    continue
                fid = feat['id']
                act = [pid, fb, fid]
                if not act in slist:
                    slist.append(act)
    if len(slist):
        return sorted(slist)
    return None

def get_targets(point_id, fieldbook, fid, known=False, polar=False):
    """ Collect observation data from one station

        :param point_id: station number/name (str)
        :param fieldbook: name of fieldbook (str)
        :param fid: id in fieldbook (int)
        :param known: If True only known points get into list.
        :returns: list of target points [[point_id fieldbook_name id] ...]
    """
    obs = []
    found = False
    lay = get_layer_by_name(fieldbook)
    if lay is None:
        return None
    if known:
        known_list = get_known()
    #pyqtRemoveInputHook()
    #pdb.set_trace()
    #for feat in lay.getFeatures():
    # TODO binary search?
    sorted_features = sorted(lay.getFeatures(), key=lambda x: x["id"])
    for feat in sorted_features:
        if feat['id'] == fid and feat['station'] == 'station' and feat['point_id'] == point_id:
            found = True
            continue
        elif feat['station'] == 'station' and found:
            # next station reached
            found = False
            break
        elif found:
            pid = feat['point_id']
            fid = feat['id']
            if known and known_list is not None and not pid in known_list:
                # skip unknown points
                continue
            if polar and (type(feat['hz']) is not float or type(feat['sd']) is not float):
                continue
            o = [pid, fieldbook, fid]
            obs.append(o)
    if len(obs):
        return sorted(obs)
    return None

def get_station(point_id, fieldbook, fid):
    """ Create a Station instance from a fieldbook row and from the coord table.

        :param point_id: station number/name (str)
        :param fieldbook: name of fieldbook (str)
        :param fid: id in fieldbook (int)
        :returns: station (Station)
    """
    p = ScPoint(point_id)
    o = get_fieldbookrow(point_id, fieldbook, fid)
    return Station(p,o)
    
def get_target(point_id, fieldbook, fid):
    """ Create a PolarObservation instance of a target point from a fieldbook row.

        :param point_id: point number/name (str)
        :param fieldbook: name of fieldbook (str)
        :param fid: id in fieldbook (int)
        :returns: observation on the point (PolarObservation)
    """
    return get_fieldbookrow(point_id, fieldbook, fid)

def get_fieldbookrow(point_id, fieldbook, fid):
    """ Reads a fieldbook row and put into a PolarObservation object.

        :param point_id: point number/name (str)
        :param fieldbook: name of fieldbook (str)
        :param fid: id in fieldbook (int)
        :returns: observation to the point or a station (PolarObservation)
    """
    lay = get_layer_by_name(fieldbook)
    if lay is None:
        return None
    #for feat in lay.getFeatures():
    # TODO binary search
    sorted_features = sorted(lay.getFeatures(), key=lambda x: x["id"])
    for feat in sorted_features:
        if feat['id'] == fid and feat['point_id'] == point_id:
            if type(feat['sd']) is float:
                if type(feat['v']) is not float:
                    dist = Distance(feat['sd'],"HD")
                elif feat['v']==0.0:    # ???
                    dist = Distance(feat['sd'],"VD")
                else:
                    dist = Distance(feat['sd'],"SD")
            else:
                dist = None
            o = PolarObservation(feat['point_id'],
                ('station' if feat['station'] == 'station' else None),
                (Angle(feat['hz'],"GON") if type(feat['hz']) is float else None),
                (Angle(feat['v'],"GON") if type(feat['v']) is float else None),
                dist,
                (feat['th'] if type(feat['th']) is float else None),
                (feat['pc'] if type(feat['pc']) is float else None))
            break
    return o

def set_orientationangle(point_id, fieldbook, fid, angle):
    """ Sets the orientation angle(hz) of the given station in the given fieldbook.

        :param point_id: point number/name (str)
        :param fieldbook: name of fieldbook (str)
        :param fid: id in fieldbook (int)
        :param angle: orientation angle (float)
    """
    lay = get_layer_by_name(fieldbook)
    if lay is None:
        return False
    #for feat in lay.getFeatures():
    # TODO binary search
    sorted_features = sorted(lay.getFeatures(), key=lambda x: x["id"])
    for feat in sorted_features:
        if feat['id'] == fid and feat['point_id'] == point_id:
            fid = feat.id()
            attrs = {feat.fieldNameIndex('hz') : angle}
            lay.dataProvider().changeAttributeValues({ fid : attrs })
            return

class ScPoint(Point):
    """
        Extended point class to store table position
    """

    def __init__(self, p, coo=None):
        """ Initialize a new ScPoint instance.

            :param p: Point object (Point) or a point_id (String)
            :param coo: name of the table where point is/to be store (String) it is None if a new point to add
        """
        if isinstance(p, Point):
            super(ScPoint, self).__init__(p.id, p.e, p.n, p.z, p.pc, p.pt)
        elif isinstance(p, str) or isinstance(p, unicode):
            super(ScPoint, self).__init__(p)
            self.get_coord()
        else:
            super(ScPoint, self).__init__("@")

        self.coo = coo

    def get_coord(self):
        """ Get the coordinates of the point from coord table and update coordinate fields
        """
        p = get_coord(self.id)
        if p is None:
            self.e = None
            self.n = None
            self.z = None
            self.pc = None
            self.pt = None
            self.coo = None
        else:
            self.e = p.e
            self.n = p.n
            self.z = p.z
            self.pc = p.pc
            self.pt = p.pt
            # TODO get_coord should return a tuple (p coo)
            #self.coo = coord_list
        return

    def store_coord(self, dimension=3, clist=None):
        """ Update coordinates in coord table, insert new point if coo is None or point not found

            :param dimension: 1/2/3D coordinates to store (int)
            :param clist: name of layer to add (str)
        """
        if clist is None:
            if self.coo is None:
                # new point to add to the first table
                cl = get_coordlist()
                if cl is None:
                    return False
            self.coo = cl[0]
        else:
            self.coo = clist
        # e, n coordinates must be given (geometry)
        if self.e is None or self.n is None:
            # TODO error report
            return
        lay = get_layer_by_name(self.coo)
        if lay is None:
            return False
        for feat in lay.getFeatures():
            if feat['point_id'] ==  self.id:
                # set feature geometry and attributes
                #pyqtRemoveInputHook()
                #pdb.set_trace()
                fid = feat.id()
                attrs = {feat.fieldNameIndex('point_id') : self.id}
                if dimension in [2, 3]:
                    attrs[feat.fieldNameIndex('e')] = self.e
                    attrs[feat.fieldNameIndex('n')] = self.n
                if dimension in [1, 3]:
                    attrs[feat.fieldNameIndex('z')] = self.z
                attrs[feat.fieldNameIndex('pc')] = self.pc
                attrs[feat.fieldNameIndex('pt')] = self.pt
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
        """ Set the coordinates

            :param p: Point
        """
        self.point_id = p.id
        self.e = p.e
        self.n = p.n
        self.z = p.z
        self.pc = p.pc
        self.pt = p.pt
