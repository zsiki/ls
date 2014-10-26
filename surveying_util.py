#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Utility module for Land Surveying Plug-in for QGIS
    GPL v2.0 license
    Copyright (C) 2014-  DgiKom Kft. http://digikom.hu
    .. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""
from qgis.core import *
import re
import local

def get_namelist(pattern):
    """
        Find layers matching name with the pattern
        :parameter pattern: regexp pattern for layer name
        :return list of matching names or None
    """
    w = []
    layermap = QgsMapLayerRegistry.instance().mapLayers()
    for name, layer in layermap.iteritems():
        if layer.type() == QGis.Point and re.search(pattern, name):
            w.append(name)
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

def get_fieldlist(vlayer):
    """
        Create a list of fields
        :parameter vlayer: vector layer
        :return list od fields
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
    return sorted(fieldlist, cmp=locale.strcoll)


