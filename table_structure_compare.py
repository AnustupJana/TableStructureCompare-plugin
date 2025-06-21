# -*- coding: utf-8 -*-
"""
/***************************************************************************
 TableStructureCompare
                                 A QGIS plugin
 Compares the attribute table structures of two vector layers in QGIS, highlighting differences in field names, types, and lengths, with results shown as a temporary layer or a confirmation popup if identical
                              -------------------
        begin                : 2025-06-17
        git sha              : $Format:%H$
        copyright            : (C) 2025 by Anustup Jana
        email                : anustupjana21@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, QVariant
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from qgis.core import (QgsProcessingAlgorithm, QgsProcessingParameterVectorLayer,
                       QgsProcessingParameterFeatureSink, QgsFeature, QgsField,
                       QgsFields, QgsVectorLayer, QgsProcessing, QgsProcessingException,
                       QgsWkbTypes, QgsProcessingProvider, QgsProject, QgsApplication)
from qgis.utils import iface
import processing
import os.path

# Initialize Qt resources from file resources.py
from .resources import *

class TableStructureCompare:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor."""
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.provider = None
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'TableStructureCompare_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            QCoreApplication.installTranslator(self.translator)

        self.actions = []
        self.menu = self.tr(u'&Table Structure Compare')
        self.first_start = None

    def tr(self, message):
        """Get the translation for a string using Qt translation API."""
        return QCoreApplication.translate('TableStructureCompare', message)

    def add_action(self, icon_path, text, callback, enabled_flag=True, add_to_menu=True, add_to_toolbar=True, status_tip=None, whats_this=None, parent=None):
        """Add a toolbar icon to the toolbar."""
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.iface.addToolBarIcon(action)

        if add_to_menu:
            self.iface.addPluginToMenu(self.menu, action)

        self.actions.append(action)
        return action

    def initProcessing(self):
        """Initialize the processing provider."""
        self.provider = TableStructureCompareProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.add_action(
            icon_path,
            text=self.tr(u'Table Structure Compare'),
            callback=self.run,
            parent=self.iface.mainWindow(),
            status_tip='Compare two table structure like a name, type base on 1st input base layer')
        
        self.initProcessing()
        self.first_start = True

    def unload(self):
        """Removes the plugin menu item, icon, and processing provider from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(self.tr(u'&Table Structure Compare'), action)
            self.iface.removeToolBarIcon(action)
        if self.provider:
            QgsApplication.processingRegistry().removeProvider(self.provider)

    def run(self):
        """Run method that performs all the real work."""
        processing.execAlgorithmDialog('table_structure_compare:attributetablecompare', {})

        # Show success message
        self.iface.messageBar().pushMessage(
            "Successful!",
            "Output added in layer, no layer added mean not found any mismatch",
            level=3,  # Qgis.Info
            duration=10
        )

class TableStructureCompareProvider(QgsProcessingProvider):
    """Processing provider for the plugin."""
    def __init__(self):
        QgsProcessingProvider.__init__(self)

    def id(self):
        return 'table_structure_compare'

    def name(self):
        return 'Table Structure Compare'

    def loadAlgorithms(self):
        self.addAlgorithm(AttributeTableCompareAlgorithm())

class AttributeTableCompareAlgorithm(QgsProcessingAlgorithm):
    BASE_LAYER = 'BASE_LAYER'
    COMPARE_LAYER = 'COMPARE_LAYER'
    OUTPUT = 'OUTPUT'

    TYPE_NAME_MAP = {
        'qlonglong': 'Integer (64 bit)',
        'int': 'Integer',
        'double': 'double',
        'QString': 'String',
        'QDate': 'Date',
        'QTime': 'Time',
        'QDateTime': 'DateTime',
        'bool': 'Boolean'
    }

    def initAlgorithm(self, config=None):
        """Define the inputs and outputs of the algorithm."""
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.BASE_LAYER,
                'Base Vector Layer',
                types=[QgsProcessing.TypeVector]
            )
        )
        self.addParameter(
            QgsProcessingParameterVectorLayer(
                self.COMPARE_LAYER,
                'Compare Vector Layer',
                types=[QgsProcessing.TypeVector]
            )
        )
        self.addParameter(
            QgsProcessingParameterFeatureSink(
                self.OUTPUT,
                'Output Difference Table'
            )
        )

    def processAlgorithm(self, parameters, context, feedback):
        """Main processing logic."""
        base_layer = self.parameterAsVectorLayer(parameters, self.BASE_LAYER, context)
        compare_layer = self.parameterAsVectorLayer(parameters, self.COMPARE_LAYER, context)

        if base_layer is None or compare_layer is None:
            raise QgsProcessingException("Invalid input layer")

        base_fields = base_layer.fields()
        compare_fields = compare_layer.fields()

        differences = []
        base_field_names_lower = [f.name().lower() for f in base_fields]
        compare_field_names_lower = [f.name().lower() for f in compare_fields]

        identical = True
        if len(base_fields) != len(compare_fields):
            identical = False
        else:
            for i, base_field in enumerate(base_fields):
                compare_field = compare_fields[i]
                if (base_field.name() != compare_field.name() or
                        base_field.type() != compare_field.type() or
                        base_field.length() != compare_field.length() or
                        base_field.precision() != compare_field.precision()):
                    identical = False
                    break

        if identical:
            feedback.pushInfo("Successful! Not found any mismatch in attribute structure.")
            return {}

        fields = QgsFields()
        fields.append(QgsField('B_Field_Name', QVariant.String))
        fields.append(QgsField('C_Field_Name', QVariant.String))
        fields.append(QgsField('Issue', QVariant.String))
        fields.append(QgsField('Base_Type', QVariant.String))
        fields.append(QgsField('Compare_Type', QVariant.String))
        fields.append(QgsField('Base_Length', QVariant.Int))
        fields.append(QgsField('Compare_Length', QVariant.Int))
        fields.append(QgsField('Base_Position', QVariant.Int))
        fields.append(QgsField('Compare_Position', QVariant.Int))
        fields.append(QgsField('Precision_Issue', QVariant.String))

        (sink, dest_id) = self.parameterAsSink(
            parameters, self.OUTPUT, context,
            fields, QgsWkbTypes.NoGeometry
        )

        for i, base_field in enumerate(base_fields):
            base_name = base_field.name()
            base_name_lower = base_name.lower()
            base_type = self.TYPE_NAME_MAP.get(QVariant.typeToName(base_field.type()), QVariant.typeToName(base_field.type()))
            base_length = base_field.length()
            base_precision = base_field.precision()
            base_position = i + 1

            if base_name_lower not in compare_field_names_lower:
                feature = QgsFeature()
                feature.setAttributes([
                    base_name,
                    '',
                    'Missing in Compare Layer',
                    base_type,
                    '',
                    base_length,
                    None,
                    base_position,
                    None,
                    ''
                ])
                sink.addFeature(feature)
            else:
                compare_idx = compare_field_names_lower.index(base_name_lower)
                compare_field = compare_fields[compare_idx]
                compare_name = compare_field.name()
                compare_type = self.TYPE_NAME_MAP.get(QVariant.typeToName(compare_field.type()), QVariant.typeToName(compare_field.type()))
                compare_length = compare_field.length()
                compare_precision = compare_field.precision()
                compare_position = compare_idx + 1

                issues = []
                precision_issue = ''

                if base_name != compare_name:
                    issues.append(f'Case Mismatch (Compare: {compare_name})')
                if base_field.type() != compare_field.type():
                    issues.append('Type Mismatch')
                if base_length != compare_length:
                    issues.append('Length Mismatch')
                if base_precision != compare_field.precision():
                    precision_issue = f'Base: {base_precision}, Compare: {compare_precision}'
                    issues.append('Precision Mismatch')
                if base_position != compare_position:
                    issues.append('Order Mismatch')

                if issues:
                    feature = QgsFeature()
                    feature.setAttributes([
                        base_name,
                        compare_name,
                        '; '.join(issues),
                        base_type,
                        compare_type,
                        base_length,
                        compare_length,
                        base_position,
                        compare_position,
                        precision_issue
                    ])
                    sink.addFeature(feature)

        for i, compare_field in enumerate(compare_fields):
            compare_name = compare_field.name()
            compare_name_lower = compare_name.lower()
            compare_type = self.TYPE_NAME_MAP.get(QVariant.typeToName(compare_field.type()), QVariant.typeToName(compare_field.type()))
            compare_length = compare_field.length()
            compare_precision = compare_field.precision()
            compare_position = i + 1

            if compare_name_lower not in base_field_names_lower:
                feature = QgsFeature()
                feature.setAttributes([
                    '',
                    compare_name,
                    'Extra in Compare Layer',
                    '',
                    compare_type,
                    None,
                    compare_length,
                    None,
                    compare_position,
                    ''
                ])
                sink.addFeature(feature)

        feedback.pushInfo("Successfully added mismatch output table in layer.")
        return {self.OUTPUT: dest_id}

    def name(self):
        return 'attributetablecompare'

    def displayName(self):
        return 'Compare Attribute Table Structure'

    def group(self):
        return 'Vector Analysis'

    def groupId(self):
        return 'vectoranalysis'

    def createInstance(self):
        return AttributeTableCompareAlgorithm()