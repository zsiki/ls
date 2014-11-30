# -*- coding: utf-8 -*-
"""
.. module: SurveyingCalculation

A QGIS plugin to solve surveying calculations.

.. moduleauthor:: Zoltan Siki <siki@agt.bme.hu>

(C) 2014 by DigiKom Ltd <mail@digikom.hu>

This program is free software; you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 2 of the License, or
(at your option) any later version.

This script initializes the plugin, making it known to QGIS.

"""

# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SurveyingCalculation class from file SurveyingCalculation.

    :param iface: a QGIS interface instance (QgsInterface)
    """
    #
    from .surveying_calculation import SurveyingCalculation
    return SurveyingCalculation(iface)
