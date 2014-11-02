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

def get_stations():
    """
        Get list of stations from fieldbooks
        :returns list of station point ids
    """
    slist = []
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
                if not pid in slist:
                    slist.append(pid)
    if len(slist):
        return sorted(slist)
    return None

