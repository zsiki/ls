# -*- coding: utf-8 -*-
"""
/***************************************************************************
 SurveyingCalculation
                                 A QGIS plugin
 To solve surveying calculations
                             -------------------
        begin                : 2014-10-17
        copyright            : (C) 2014 by DigiKom Kft.
        email                : mail@digikom.hu
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load SurveyingCalculation class from file SurveyingCalculation.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .surveying_calculation import SurveyingCalculation
    return SurveyingCalculation(iface)
