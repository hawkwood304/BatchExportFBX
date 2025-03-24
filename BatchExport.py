# import math
# import os
# from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

import os
import maya.cmds as cm
# import pymel.core as pm
import maya.OpenMaya as om
import maya.OpenMayaUI as omui

from PySide2 import QtWidgets, QtCore, QtGui
from maya.mel import eval


# import sys


class QHLine(QtWidgets.QFrame):

    def __init__(self):
        super(QHLine, self).__init__()
        self.setFrameShape(self.HLine)
        self.setFrameShadow(self.Sunken)


class QVLine(QtWidgets.QFrame):

    def __init__(self):
        super(QVLine, self).__init__()
        self.setFrameShape(self.VLine)
        self.setFrameShadow(self.Sunken)


class QHLineName(QtWidgets.QGridLayout):

    def __init__(self, name):
        super(QHLineName, self).__init__()
        name_lb = QtWidgets.QLabel(name)
        name_lb.setAlignment(QtCore.Qt.AlignCenter)
        name_lb.setStyleSheet("font: italic 9pt;" "color: azure;")
        self.addWidget(name_lb, 0, 0, 1, 1)
        self.addWidget(QHLine(), 0, 1, 1, 2)


# noinspection PyAttributeOutsideInit
class BatchExport(QtWidgets.QWidget):
    fbxVersions = {
        '2016': 'FBX201600',
        '2014': 'FBX201400',
        '2013': 'FBX201300',
        '2017': 'FBX201700',
        '2018': 'FBX201800',
        '2019': 'FBX201900'
    }

    def __init__(self):
        super(BatchExport, self).__init__()

        self.create_widgets()
        self.create_layouts()
        self.create_connections()

    def create_widgets(self):
        self.drill_path_lb = QtWidgets.QLabel("Drill path: ")
        self.drill_path_le = QtWidgets.QLineEdit()

        self.export_path_lb = QtWidgets.QLabel("Export path: ")
        self.export_path_le = QtWidgets.QLineEdit()

        self.drill_file_path_btn = QtWidgets.QPushButton('')
        self.drill_file_path_btn.setIcon(QtGui.QIcon(':fileOpen.png'))
        self.drill_file_path_btn.setToolTip('Select File')

        self.export_file_path_btn = QtWidgets.QPushButton('')
        self.export_file_path_btn.setIcon(QtGui.QIcon(':fileOpen.png'))
        self.export_file_path_btn.setToolTip('Select File')

        self.fbx_name_lb = QtWidgets.QLabel("Fbx obj name: ")
        self.fbx_name_le = QtWidgets.QLineEdit()

        self.abc_name_lb = QtWidgets.QLabel("Abc obj name: ")
        self.abc_name_le = QtWidgets.QLineEdit()

        self.fbx_export_btn = QtWidgets.QPushButton("FBX Export")
        self.fbx_export_btn.setStyleSheet('QPushButton {background-color: lightsteelblue; color: black;}')
        self.abc_export_btn = QtWidgets.QPushButton("ABC Export")
        self.abc_export_btn.setStyleSheet('QPushButton {background-color: lightsteelblue; color: black;}')
        self.combine_export_btn = QtWidgets.QPushButton("Combine Export")
        self.combine_export_btn.setStyleSheet('QPushButton {background-color: palegreen; color: black;}')

    def create_layouts(self):

        patch_option_layout = QtWidgets.QGridLayout()
        patch_option_layout.addWidget(self.drill_path_lb, 0, 0)
        patch_option_layout.addWidget(self.drill_path_le, 0, 1)
        patch_option_layout.addWidget(self.drill_file_path_btn, 0, 2)
        patch_option_layout.addWidget(self.export_path_lb, 1, 0)
        patch_option_layout.addWidget(self.export_path_le, 1, 1)
        patch_option_layout.addWidget(self.export_file_path_btn, 1, 2)

        name_option_layout = QtWidgets.QGridLayout()
        name_option_layout.addWidget(self.fbx_name_lb, 0, 0)
        name_option_layout.addWidget(self.fbx_name_le, 0, 1)
        name_option_layout.addWidget(self.abc_name_lb, 1, 0)
        name_option_layout.addWidget(self.abc_name_le, 1, 1)

        execution_layout = QtWidgets.QHBoxLayout()
        execution_layout.addWidget(self.fbx_export_btn)
        execution_layout.addWidget(self.abc_export_btn)
        execution_layout.addWidget(self.combine_export_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(QHLineName("Patch option"))
        main_layout.addLayout(patch_option_layout)
        main_layout.addLayout(QHLineName("Name option"))
        main_layout.addLayout(name_option_layout)
        main_layout.addLayout(QHLineName("Execution"))
        main_layout.addLayout(execution_layout)


    def create_connections(self):
        self.drill_file_path_btn.clicked.connect(self.drill_show_file_select_dialog)
        self.export_file_path_btn.clicked.connect(self.export_show_file_select_dialog)

    def drill_show_file_select_dialog(self):
        self.drill_file_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')

        self.drill_path_le.setText(self.drill_file_path)

    def export_show_file_select_dialog(self):
        self.export_file_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory')

        self.export_path_le.setText(self.export_file_path)

    def export_option(self, path):
        # Get maya version and fbx version
        self.version_fbx = "2020"

        # Option
        eval("FBXExportSmoothingGroups -v true")
        eval("FBXExportHardEdges -v false")
        eval("FBXExportTangents -v false")
        eval("FBXExportSmoothMesh -v true")
        eval("FBXExportInstances -v false")
        eval("FBXExportReferencedAssetsContent -v false")

        eval('FBXExportBakeComplexAnimation -v true')

        eval("FBXExportBakeComplexStep -v 1")

        eval("FBXExportUseSceneName -v false")
        eval("FBXExportQuaternion -v euler")
        eval("FBXExportShapes -v true")
        eval("FBXExportSkins -v true")

        # Constraints
        eval("FBXExportConstraints -v false")
        # Cameras
        eval("FBXExportCameras -v true")
        # Lights
        eval("FBXExportLights -v true")
        # Embed Media
        eval("FBXExportEmbeddedTextures -v false")
        # Connections
        eval("FBXExportInputConnections -v true")
        # Axis Conversion
        eval("FBXExportUpAxis y")
        # Version
        eval('FBXExportFileVersion -v {}'.format(self.version_fbx))

        # Export!
        eval('FBXExport -f "{0}" -s'.format(path))

    def get_path_file(self):
        """

        Returns: List of path to fbx file

        """
        # Get path of folder
        path = self.filepath_le.text()

        # Get all files path
        files = os.listdir(path)

        maya_file_path = []

        # Loop through all files path
        for f in files:

            # Check if file is fbx or not
            if f.endswith(".ma"):
                maya_file = (os.path.join(path, f)).replace(os.sep, '/')
                maya_file_path.append(maya_file)

            elif f.endswith(".mb"):
                maya_file = (os.path.join(path, f)).replace(os.sep, '/')
                maya_file_path.append(maya_file)
            else:
                continue

        # Return list of fbx files path and maya file
        return maya_file_path

    def get_list_character_name(self):
        if self.fbx_name_le.text():
            list_character_name_raw = self.fbx_name_le.text()
            list_character_name_raw = list_character_name_raw.replace(" ", "")
            list_character_name = list_character_name_raw.split(",")
            return list_character_name
        else:
            list_character_name = []
            return list_character_name

    def get_list_abc_mesh_name(self):
        if self.abc_name_le.text():
            list_mesh_name_raw = self.abc_name_le.text()
            list_mesh_name_raw = list_mesh_name_raw.replace(" ", "")
            list_mesh_name = list_mesh_name_raw.split(",")
            return list_mesh_name
        else:
            list_mesh_name = []
            return list_mesh_name

    @staticmethod
    def get_time_range():

        min_time = cm.playbackOptions(q=True, min=True)
        max_time = cm.playbackOptions(q=True, max=True)

        return min_time, max_time

    def fbx_export(self):
        filepath = self.get_convert_file_path()
        shot_name = self.get_shot_name()
        list_character_name = self.get_list_character_name()
        min_time, max_time = self.get_time_range()

        list_export = cm.ls(sl=True)

        new_filepath = (os.path.join(filepath, shot_name)).replace(os.sep, '/')

        if not os.path.isdir(new_filepath):
            os.mkdir(new_filepath)

        # Cam export

        if len(list_export) != 0:
            for obj in list_export:

                children = cm.listRelatives(obj, children=True, fullPath=True) or []

                if len(children) == 1:
                    child = children[0]
                    obj_type = cm.objectType(child)

                else:
                    obj_type = cm.objectType(obj)

                if obj_type == 'camera':
                    new_cam = cm.camera()
                    cm.parentConstraint(obj, new_cam[0], mo=0)
                    cm.connectAttr("{0}.focalLength".format(children[0]), "{0}.focalLength".format(new_cam[1]), f=1)
                    cm.select(new_cam[0])
                    eval(
                        'bakeResults -simulation true -t "{0}:{1}" -sampleBy 1 -oversamplingRate 1 '
                        '-disableImplicitControl true -preserveOutsideKeys true -sparseAnimCurveBake false '
                        '-removeBakedAttributeFromLayer false -removeBakedAnimFromLayer false -bakeOnOverrideLayer '
                        'false -minimizeRotation true -controlPoints false -shape false;'.format(
                            min_time, max_time))
                    cm.select("{0}.focalLength".format(new_cam[1]))
                    eval(
                        'bakeResults -simulation true -t "{0}:{1}" -sampleBy 1 -oversamplingRate 1 '
                        '-disableImplicitControl true -preserveOutsideKeys true -sparseAnimCurveBake false '
                        '-removeBakedAttributeFromLayer false -removeBakedAnimFromLayer false -bakeOnOverrideLayer '
                        'false -minimizeRotation true -controlPoints false -shape true;'.format(
                            min_time, max_time))

                    cm.keyframe(new_cam[0], edit=True, relative=True, timeChange=-min_time)

                    cm.select(new_cam[0])
                    cam_name = '{0}_cam.fbx'.format(obj)
                    cam_part = (os.path.join(str(new_filepath), str(cam_name))).replace(os.sep, '/')
                    self.fbx_export_option(path=cam_part)
                    cm.delete(new_cam[0])

                # else:
                #     namespace = obj.split(":")[0]
                #     name_character = namespace.split("|")[-1]
                #     if len(list_character_name) != 0:
                #         for name in list_character_name:
                #             if str(name) in str(name_character):
                #                 name_character = "{}_anim".format(name)
                #             else:
                #                 name_character = name_character
                #     fbx_name = '{0}_{1}.fbx'.format(shot_name, name_character)
                #     path = (os.path.join(str(new_filepath), str(fbx_name))).replace(os.sep, '/')
                #
                #     cm.select(obj)
                #     self.fbx_export_option(path=path)

        list_name_space_raw = cm.ls()
        list_name_space = []

        for i in list_name_space_raw:
            if "DeformationSystem" in str(i):
                name_space = i.rpartition(":")[0]

                for y in list_character_name:
                    if str(y) in str(name_space):
                        list_name_space.append(name_space)

        list_name_space = list(set(list_name_space))
        for name in list_name_space:
            for z in list_character_name:
                if str(z) in str(name):
                    file_name = "{}_anim".format(z)

                    fbx_name = '{0}_{1}.fbx'.format(shot_name, file_name)
                    path = (os.path.join(str(new_filepath), str(fbx_name))).replace(os.sep, '/')

                    cm.select("{}:DeformationSystem".format(name), "{}:Geometry".format(name))
                    self.fbx_export_option(path=path)


# noinspection PyMethodMayBeStatic,PyAttributeOutsideInit,PyMethodOverriding
class MainWindow(QtWidgets.QDialog):
    WINDOW_TITLE = "Batch Export"

    SCRIPTS_DIR = cm.internalVar(userScriptDir=True)
    ICON_DIR = os.path.join(SCRIPTS_DIR, 'Thi/Icon')

    dlg_instance = None

    @classmethod
    def display(cls):
        if not cls.dlg_instance:
            cls.dlg_instance = MainWindow()

        if cls.dlg_instance.isHidden():
            cls.dlg_instance.show()

        else:
            cls.dlg_instance.raise_()
            cls.dlg_instance.activateWindow()

    @classmethod
    def maya_main_window(cls):
        """

        Returns: The Maya main window widget as a Python object

        """
        main_window_ptr = omui.MQtUtil.mainWindow()
        return wrapInstance(int(main_window_ptr), QtWidgets.QWidget)

    def __init__(self):
        super(MainWindow, self).__init__(self.maya_main_window())

        self.setWindowTitle(self.WINDOW_TITLE)
        self.setWindowFlags(self.windowFlags() ^ QtCore.Qt.WindowContextHelpButtonHint)

        self.geometry = None

        self.setMinimumSize(400, 300)
        self.setMaximumSize(400, 300)
        self.create_widget()
        self.create_layouts()
        self.create_connections()

    def create_widget(self):
        self.content_layout = QtWidgets.QHBoxLayout()
        self.content_layout.addWidget(BatchExport())

        self.close_btn = QtWidgets.QPushButton("Close")

    def create_layouts(self):
        button_layout = QtWidgets.QHBoxLayout()
        button_layout.addWidget(self.close_btn)

        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.addLayout(self.content_layout)
        main_layout.addLayout(button_layout)

    def create_connections(self):
        self.close_btn.clicked.connect(self.close)

    def showEvent(self, e):
        super(MainWindow, self).showEvent(e)

        if self.geometry:
            self.restoreGeometry(self.geometry)

    def closeEvent(self, e):
        super(MainWindow, self).closeEvent(e)

        self.geometry = self.saveGeometry()