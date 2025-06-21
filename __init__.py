# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TableStructureCompare
                                 A QGIS plugin
 Compares the attribute table structures of two vector layers in QGIS, highlighting differences in field names, types, and lengths, with results shown as a temporary layer or a confirmation popup if identical
                             -------------------
        begin                : 2025-06-17
        copyright            : (C) 2025 by Anustup Jana
        email                : anustupjana21@gmail.com
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
    """Load TableStructureCompare class from file TableStructureCompare.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .table_structure_compare import TableStructureCompare
    return TableStructureCompare(iface)
