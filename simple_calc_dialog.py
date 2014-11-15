#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: simple_calc_dialog.py
    :platform: Linux/Windows
    :synopsis: Dialog window of simple calculations for Land Surveying Plug-in for QGIS
    GPL v2.0 license
    Copyright (C) 2014-  DgiKom Kft. http://digikom.hu
    .. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""


import os
from PyQt4 import QtGui, uic
from qgis.core import *
from base_classes import *
from calculation import *
from surveying_util import *

FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'simple_calc.ui'))

class SimpleCalculationDialog(QtGui.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        """Constructor."""
        super(SimpleCalculationDialog, self).__init__(parent)
        self.setupUi(self)
