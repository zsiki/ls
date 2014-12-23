# -*- coding: utf-8 -*-
"""
.. module:: config
    :platform: Linux, Windows
    :synopsis: config variables

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>

Variables set::

    appname: name of the plugin
    fontname: monospace font used in calculation results widgets
    fontsize: font size used in calculation results widgets
    homedir: start dir used for loading fieldbooks
    log_path: path to log file
    tolerance: snapping tolerance to line tool
"""

appname = 'SurveyingCalculation'
# dialogs
fontname = 'DejaVu Sans Mono'
fontsize = 9
#
homedir = '/tmp'
# logging
log_path = '/tmp/log.log'
# line tool
tolerance = 1   # tolerance in canvas units?
