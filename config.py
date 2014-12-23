# -*- coding: utf-8 -*-
"""
.. module:: config
    :platform: Linux, Windows
    :synopsis: config variables

.. moduleauthor: Zoltan Siki <siki@agt.bme.hu>

    :param appname: name of the plugin
    :param fontname: monospace font used in calculation results widgets
    :param fontsize: font size used in calculation results widgets
    :param homedir: start dir used for loading fieldbooks
    :param log_path: path to log file
    :param tolerance: snapping tolerance to line tool
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
