#!/usr/bin/env python
# -*- coding:utf-8 -*-
# ============================================================================
# Copyright (C) 2021 Fractal Picture, All Rights Reserved.
#
# The coded instructions, statements, computer programs, and/or related
# material (collectively the "Data") in these files contain unpublished
# information proprietary to Fractal Picture, which is
# protected by IP Protection law.
#
# Author: sudarshanhavale@gmail.com (Sudarshan Havale)
# Module: fractal standard renamer
# ============================================================================
import sys
import pymel.core as pm
from maya import OpenMayaUI
from PySide2.QtWidgets import (QApplication, QMainWindow, QCompleter, QLineEdit, QVBoxLayout,
                               QWidget, QLabel, QComboBox, QHBoxLayout, QPushButton, QMessageBox)
from PySide2.QtCore import Qt
from PySide2 import QtGui
from shiboken2 import wrapInstance

# Pipeline configurations
config_values = {'description': {'bag': 'tooltip',
                 'barrel': 'tooltip',
                 'blocks': 'tooltip',
                 'bolt': 'tooltip',
                 'box': 'tooltip',
                 'branch': 'tooltip',
                 'brick': 'tooltip',
                 'car': 'tooltip',
                 'cloth': 'tooltip',
                 'container': 'tooltip',
                 'crate': 'tooltip',
                 'debris': 'tooltip',
                 'door': 'tooltip',
                 'floor': 'tooltip',
                 'flower': 'tooltip',
                 'frame': 'tooltip',
                 'fruit': 'tooltip',
                 'glass': 'tooltip',
                 'ground': 'tooltip',
                 'jewelry': 'tooltip',
                 'leaf': 'tooltip',
                 'light': 'tooltip',
                 'machine': 'tooltip',
                 'mountain': 'tooltip',
                 'panel': 'tooltip',
                 'pebble': 'tooltip',
                 'pillar': 'tooltip',
                 'pipe': 'tooltip',
                 'plank': 'tooltip',
                 'plant': 'tooltip',
                 'plate': 'tooltip',
                 'pot': 'tooltip',
                 'railing': 'tooltip',
                 'rivet': 'tooltip',
                 'road': 'tooltip',
                 'rock': 'tooltip',
                 'roof': 'tooltip',
                 'roots': 'tooltip',
                 'slab': 'tooltip',
                 'soil': 'tooltip',
                 'stair': 'tooltip',
                 'stand': 'tooltip',
                 'stone': 'tooltip',
                 'streetlight': 'tooltip',
                 'table': 'tooltip',
                 'tree': 'tooltip',
                 'trunk': 'tooltip',
                 'tyre': 'tooltip',
                 'vehicle': 'tooltip',
                 'wall': 'tooltip',
                 'wheel': 'tooltip',
                 'window': 'tooltip',
                 'wire': 'tooltip'},
 'material': {'ceramic': 'tooltip',
              'cloth': 'tooltip',
              'concrete': 'tooltip',
              'fabric': 'tooltip',
              'gem': 'tooltip',
              'glass': 'tooltip',
              'leather': 'tooltip',
              'liquid': 'tooltip',
              'metal': 'tooltip',
              'paper': 'tooltip',
              'plastic': 'tooltip',
              'rubber': 'tooltip',
              'stone': 'tooltip',
              'wood': 'tooltip'},
 'object_type': {'crv': 'curve object',
                 'geo': 'mesh object',
                 'grm': 'groom scalp',
                 'ins': 'instanced object',
                 'ply': 'poly blocker',
                 'prx': 'proxy object',
                 'sdm': 'subdiv mesh object',
                 'vol': 'volume reference'},
 'resolution': {'hi': 'hires',
                'lo': 'lores',
                'md': 'mid res',
                'xhi': 'extra hires',
                'xlo': 'extra lores'},
 'x_axis': {'b': 'back', 'f': 'front'},
 'y_axis': {'d': 'down', 't': 'top'},
 'z_axis': {'l': 'left', 'm': 'middle', 'r': 'right'}}


config_description = config_values.get("description", {"object": "default value"})
config_material = config_values.get("material", {"def": "default value"})
config_resolution = config_values.get("resolution", {})
config_x_axis = config_values.get("x_axis", {})
config_y_axis = config_values.get("y_axis", {})
config_z_axis = config_values.get("z_axis", {})
config_type = config_values.get("object_type", {})


def query_assets():
    """
    Query asset names from Shotgun's current project.

    Returns:
        list: A list of asset names.
    """

    asset_names = []
    # # Set up the Shotgun Toolkit API
    # engine = sgtk.platform.current_engine()
    # tk = engine.sgtk
    # ctx = engine.context
    #
    # # Query asset names from the current project
    # asset_data = tk.shotgun.find("Asset", [["project", "is", ctx.project]], ["code"])
    #
    # # Extract asset names from the query results
    # asset_names = [asset["code"] for asset in asset_data]

    return asset_names


class MainWindow(QMainWindow):
    def __init__(self, asset_names):
        main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        main_window = wrapInstance(int(main_window_ptr), QWidget)

        super(MainWindow, self).__init__(main_window)

        self.setWindowTitle("FRename")

        # Create an autocomplete text field for Asset Name
        asset_name_label = QLabel("Asset Name")
        self.asset_name_input = QLineEdit(self)
        self.asset_name_input.setPlaceholderText("Enter Asset Name")
        self.asset_name_input.setCompleter(self.create_completer(asset_names))

        # Create a label and a preset dropdown for X-Axis
        x_axis_label = QLabel("X-Axis")
        self.x_axis_dropdown = QComboBox(self)
        self.x_axis_dropdown.addItems(config_x_axis.keys())
        self.x_axis_dropdown.setCurrentIndex(-1)
        for i, v in enumerate(config_x_axis.values()):
            self.x_axis_dropdown.setItemData(i, v, Qt.ToolTipRole)

        # Create a label and a preset dropdown for Y-Axis
        y_axis_label = QLabel("Y-Axis")
        self.y_axis_dropdown = QComboBox(self)
        self.y_axis_dropdown.addItems(config_y_axis.keys())
        self.y_axis_dropdown.setCurrentIndex(-1)
        for i, v in enumerate(config_y_axis.values()):
            self.y_axis_dropdown.setItemData(i, v, Qt.ToolTipRole)

        # Create a label and a preset dropdown for Z-Axis
        z_axis_label = QLabel("Z-Axis")
        self.z_axis_dropdown = QComboBox(self)
        self.z_axis_dropdown.addItems(config_z_axis.keys())
        self.z_axis_dropdown.setCurrentIndex(-1)
        for i, v in enumerate(config_z_axis.values()):
            self.z_axis_dropdown.setItemData(i, v, Qt.ToolTipRole)

        # Create a label and an autocomplete text field for Description
        description_label = QLabel("Description")
        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Enter Description")
        self.description_input.setText("object")
        self.description_input.setCompleter(self.create_completer(config_description))

        # Create a label and an autocomplete text field for Material
        material_label = QLabel("Material")
        self.material_input = QLineEdit(self)
        self.material_input.setPlaceholderText("Enter Material")
        self.material_input.setText("def")
        self.material_input.setCompleter(self.create_completer(config_material))

        # Create a label and a preset dropdown for LOD
        lod_label = QLabel("LOD")
        self.lod_dropdown = QComboBox(self)
        self.lod_dropdown.addItems(config_resolution.keys())
        self.lod_dropdown.setCurrentIndex(-1)
        for i, v in enumerate(config_resolution.values()):
            self.lod_dropdown.setItemData(i, v, Qt.ToolTipRole)

        # Create a label and an instance number input field
        instance_number_label = QLabel("Instance Number")
        self.instance_number_input = QLineEdit(self)
        self.instance_number_input.setPlaceholderText("Enter Instance Number")
        self.instance_number_input.setText("001")
        self.instance_number_input.setValidator(QtGui.QIntValidator(1, 999, self))

        # Create a label and a preset dropdown for Type
        type_label = QLabel("Type")
        self.type_dropdown = QComboBox(self)
        self.type_dropdown.addItems(config_type.keys())
        self.type_dropdown.setCurrentText("geo")

        # Create a button for renaming selected objects
        self.rename_button = QPushButton("Rename Selected Objects", self)
        self.rename_button.clicked.connect(self.rename_objects)

        # Create a vertical layout for the main window
        main_layout = QVBoxLayout()

        # Create a vertical layout for Asset Name
        asset_name_layout = QVBoxLayout()
        asset_name_layout.addWidget(asset_name_label)
        asset_name_layout.addWidget(self.asset_name_input)
        main_layout.addLayout(asset_name_layout)

        # Create a horizontal layout for Axis
        axis_layout = QHBoxLayout()
        axis_layout.addWidget(x_axis_label)
        axis_layout.addWidget(self.x_axis_dropdown)
        axis_layout.addWidget(y_axis_label)
        axis_layout.addWidget(self.y_axis_dropdown)
        axis_layout.addWidget(z_axis_label)
        axis_layout.addWidget(self.z_axis_dropdown)
        main_layout.addLayout(axis_layout)

        # Create a horizontal layout for Description, Material, LOD, Instance Number, and Type
        input_layout = QHBoxLayout()
        input_layout.addWidget(description_label)
        input_layout.addWidget(self.description_input)
        input_layout.addWidget(material_label)
        input_layout.addWidget(self.material_input)
        input_layout.addWidget(lod_label)
        input_layout.addWidget(self.lod_dropdown)
        input_layout.addWidget(instance_number_label)
        input_layout.addWidget(self.instance_number_input)
        input_layout.addWidget(type_label)
        input_layout.addWidget(self.type_dropdown)
        main_layout.addLayout(input_layout)

        # Add the rename button to the layout
        main_layout.addWidget(self.rename_button)

        # Create a central widget and set the layout
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def create_completer(self, tags):
        """
        Create and configure a completer for autocompletion.

        Args:
            tags (dict or list): Dictionary or list of tags for autocompletion.

        Returns:
            QCompleter: A configured QCompleter object.
        """
        if isinstance(tags, dict):
            # Convert dictionary values to a list
            completer = QCompleter(list(tags.keys()), self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)

            # Set tooltips for autocompletion suggestions
            model = completer.model()
            for index in range(model.rowCount()):
                item = model.data(model.index(index, 0))
                tooltip = tags.get(item)
                completer.model().setData(model.index(index, 0), tooltip, Qt.ToolTipRole)
        elif isinstance(tags, list):
            completer = QCompleter(tags, self)
            completer.setCaseSensitivity(Qt.CaseInsensitive)
        else:
            raise ValueError("Unsupported tags type. Supported types are dict and list.")

        return completer

    def rename_objects(self):
        user_inputs = []
        axis = ""
        separator = "_"
        result = ""

        asset_name = self.asset_name_input.text()
        x_axis = self.x_axis_dropdown.currentText()
        if x_axis:
            axis += x_axis
        y_axis = self.y_axis_dropdown.currentText()
        if y_axis:
            axis += y_axis
        z_axis = self.z_axis_dropdown.currentText()
        if z_axis:
            axis += z_axis

        description = self.description_input.text()
        # Check if the Description field is empty
        if not description:
            QMessageBox.warning(self, "Warning", "Description cannot be empty.")
            return

        if description:
            user_inputs.append(description)
        material = self.material_input.text()
        # Check if the Material field is empty
        if not material:
            QMessageBox.warning(self, "Warning", "Material cannot be empty.")
            return

        if material:
            user_inputs.append(material + "Mtl")
        lod = self.lod_dropdown.currentText()
        if lod:
            user_inputs.append(lod)
        instance_number = self.instance_number_input.text().zfill(3)
        if instance_number:
            user_inputs.append(instance_number)
        asset_type = self.type_dropdown.currentText()
        if asset_type:
            user_inputs.append(asset_type)

        if user_inputs:
            result = separator.join(user_inputs)
            if axis:
                result = axis + separator + result

        if result:
            selected_objects = pm.selected()

            for index, obj in enumerate(selected_objects):
                new_name = result
                if asset_name:
                    new_name = asset_name + separator + result

                # Check if the new name already exists
                while pm.ls(new_name):
                    index += 1
                    new_instance_number = str(index).zfill(3)
                    user_inputs[-2] = new_instance_number
                    result = separator.join(user_inputs)
                    if axis:
                        result = axis + separator + result
                    new_name = result
                    if asset_name:
                        new_name = asset_name + separator + result

                obj.rename(new_name)


def main():
    # Query asset names from Shotgun's current project
    asset_names = query_assets()

    try:
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        window = MainWindow(asset_names)
        window.show()
        sys.exit(app.exec_())
    except SystemExit:
        pass

# Run the UI
if __name__ == "__main__":
    main()
