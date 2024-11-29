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
import maya.mel as mel
from maya import OpenMayaUI
from PySide2.QtWidgets import (QApplication, QMainWindow, QCompleter, QLineEdit, QVBoxLayout,
                               QWidget, QLabel, QComboBox, QCheckBox, QHBoxLayout, QPushButton, QMessageBox, QSizePolicy, QSpacerItem)
from PySide2.QtCore import QFile, Qt
from PySide2.QtUiTools import QUiLoader
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


class MainWindow(QMainWindow, Ui_Form):
    def __init__(self):
        main_window_ptr = OpenMayaUI.MQtUtil.mainWindow()
        main_window = wrapInstance(int(main_window_ptr), QWidget)

        super(MainWindow, self).__init__(main_window)

        self.setWindowTitle("Clean Up")
        self.load_ui()


    def load_ui(self):
        loader = QUiLoader()
        #path = os.path.join(os.path.dirname(__file__), "clean_up_ui.ui")
        path = r'E:\my_jobs\reflectrions\clean_up_ui.ui'
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui = loader.load(ui_file, self)
        ui_file.close()
        self.connects()

    def connects(self):
        self.ui.five_sided_mesh.clicked.connect(self.poly_clean_up)
        self.ui.rename_group.clicked.connect(self.group_rename)

    def poly_clean_up(self):
        #TODO add a message box, in checkbox selection, run on polyCleanUpArgList, at submit button, run polyClean

        print('poly clean up')
        clean_args = mel.eval('polyCleanupArgList 4 { "0","1","1","0","0","0","0","0","0","1e-005","0","1e-005","0","1e-005","0","-1","1","0" };')
        if not clean_args:
            print('No mesh likely candidate for clean up.')
            return
        node = mel.eval('polyClean ' + ' '.join(cleanArgs))
        return node

    def group_rename(self):
        #cmds.rename(current_name, new_name)

    def cleanup_objects(self):
        user_inputs = []
        axis = ""
        separator = "_"
        result = ""

        asset_name = self.asset_name_input.text()
        x_axis = self.reference_shared_in_folder_checkbox.currentText()
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
    try:
        if not QApplication.instance():
            app = QApplication([])
        else:
            app = QApplication.instance()
        window = MainWindow()
        window.show()
        sys.exit(app.exec_())
    except SystemExit:
        pass

# Run the UI
if __name__ == "__main__":
    main()
