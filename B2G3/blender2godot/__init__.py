# ##### BEGIN GPL LICENSE BLOCK #####
# Blender2Godot for blender is a blender addon for exporting Blender scenes to Godot Engine from Blender.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.
# ##### END GPL LICENSE BLOCK #####


"""
Blender To Godot

This is a simple exporter from blender to godot for testing purposes.

"""

import os
import subprocess
import shutil
import json
from fileinput import FileInput

import bpy

#from blender2godot import prefs

from blender2godot.addon_config import addon_config

from blender2godot.godot_project_properties import godot_project_properties

from blender2godot.display_properties import display_properties

from blender2godot.splash_properties import splash_properties

from blender2godot.b2g_tools import (
	advanced_tools,
	general_tools,
	)

from blender2godot.scene_properties import scene_properties

from blender2godot.player_properties import player_properties

from blender2godot.test_project import test_project

from blender2godot.game_export import game_export


bl_info = {
    "name": "Blender2Godot",
    "author": "Jaume Castells",
    "version": (0,1),
    "blender": (2, 82, 0),
    "location": "View 3D/Properties",
    "description": "Blender to godot easy exporter",
    "warning": "",
    "wiki_url": "https://zammedev.com",
    "tracker_url": "https://zammedev.com",
    "category": "Interface",
}


class ColliderProperties(bpy.types.PropertyGroup):
    """ Collider properties """
    collider_options = [
        ("none", "None", "", "NONE", 0),
        ("convex", "Convex", "", "CONVEX", 1),
        ("mesh", "Mesh", "", "MESH", 2),
        ("smart", "Smart", "", "SMART", 3)]


class PlayerObjects(bpy.types.PropertyGroup):
    """ Player Objects """
    player_objects = [
        ("none", "None", "", "NONE", 0),]

"""
def check_player_objects():
    if len(player_objects) != len(bpy.context.scene.objects):
        self.fill_player_object_menu(bpy.context)
"""

def fill_player_objects_menu(self, context):
    player_objects = []
    player_objects.clear()
    player_objects.append(("None", "None", "None"))
    for ob in bpy.context.scene.objects:
        if ob.type == "CAMERA":
            menu_item = (ob.name, ob.name, ob.name)
            player_objects.append(menu_item)
            #print("One item added:", menu_item)
    return player_objects

def update_player_objects(aa):
    pass


def init_properties():
    bpy.types.Scene.game_name = bpy.props.StringProperty(name="Name", default="NEW_GAME")
    bpy.types.Scene.game_folder = bpy.props.StringProperty(name="Folder", subtype="DIR_PATH", default=" ")
    bpy.types.Scene.game_icon = bpy.props.StringProperty(name="Icon", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.game_icon_image = bpy.props.PointerProperty(name="Game Icon Image", type=bpy.types.Image)
    bpy.types.Scene.project_folder = bpy.props.StringProperty(name="Project Folder", subtype="DIR_PATH", default=" ")
    
    bpy.types.Scene.godot_executable = bpy.props.StringProperty(name="Godot", subtype="FILE_PATH", default="/usr/local/games/godot-engine")
    #bpy.types.Scene.custom_godot = bpy.props.BoolProperty(name="Custom Godot", default=False)
    #bpy.types.Scene.godot_executable_downloaded_zip = bpy.props.StringProperty(name="Godot zip", subtype="FILE_PATH", default=".")
    
    bpy.types.Scene.colliders_filepath = bpy.props.StringProperty(name="Colliders", subtype="FILE_PATH", default=" ")
    
    bpy.types.Scene.android_template_filepath = bpy.props.StringProperty(name="Android Template", subtype="FILE_PATH", default=" ")
    
    bpy.types.Scene.godot_project_filepath = bpy.props.StringProperty(name="GPF", subtype="FILE_PATH", default=" ")

    # Display vars
    bpy.types.Scene.display_width = bpy.props.IntProperty(name="Width", default=1024)
    bpy.types.Scene.display_height = bpy.props.IntProperty(name="Height", default=768)
    bpy.types.Scene.display_resizable = bpy.props.BoolProperty(name="Resizable", default=True)
    bpy.types.Scene.display_borderless = bpy.props.BoolProperty(name="Borderless", default=False)
    bpy.types.Scene.display_fullscreen = bpy.props.BoolProperty(name="Fullscreen", default=False)
    bpy.types.Scene.display_alwaysontop = bpy.props.BoolProperty(name="Always on top", default=False)

    # Splash vars
    bpy.types.Scene.splash_showimage = bpy.props.BoolProperty(name="Show splash image", default=True)
    bpy.types.Scene.splash_imagefilepath = bpy.props.StringProperty(name="Splash Image Filepath", subtype="FILE_PATH", default="res://icon.png")
    bpy.types.Scene.splash_fullsize = bpy.props.BoolProperty(name="Full size", default=False)
    bpy.types.Scene.splash_usefilter = bpy.props.BoolProperty(name="Use filter", default=False)
    bpy.types.Scene.splash_bgcolor = bpy.props.FloatVectorProperty(name="BG Color", subtype = "COLOR", default = (0.0,0.0,0.0,1.0), min = 0.0, max = 1.0, size = 4)

    # Export vars
    # Checkboxes
    bpy.types.Scene.android_export = bpy.props.BoolProperty(name="Android", default=False)
    bpy.types.Scene.linux_export = bpy.props.BoolProperty(name="Linux", default=False)
    bpy.types.Scene.windows_export = bpy.props.BoolProperty(name="Windows", default=False)
    bpy.types.Scene.mac_export = bpy.props.BoolProperty(name="Mac", default=False)
    bpy.types.Scene.web_export = bpy.props.BoolProperty(name="Web", default=False)
    # Paths
    bpy.types.Scene.android_exe_filepath = bpy.props.StringProperty(name="AndroidExeFilepath", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.linux_exe_filepath = bpy.props.StringProperty(name="LinuxExeFilepath", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.windows_exe_filepath = bpy.props.StringProperty(name="WindowsExeFilepath", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.mac_exe_filepath = bpy.props.StringProperty(name="MacExeFilepath", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.web_exe_filepath = bpy.props.StringProperty(name="WebExeFilepath", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.current_version_compiling = bpy.props.StringProperty(name="CurrentVersionCompiling", default=" ")
    bpy.types.Scene.game_exports_path = bpy.props.StringProperty(name="GameExportsPath", default=" ")
    bpy.types.Scene.android_exports_path = bpy.props.StringProperty(name="AndroidExportPath", default=" ")
    bpy.types.Scene.linux_exports_path = bpy.props.StringProperty(name="LinuxExportPath", default=" ")
    bpy.types.Scene.windows_exports_path = bpy.props.StringProperty(name="WindowsExportPath", default=" ")
    bpy.types.Scene.mac_exports_path = bpy.props.StringProperty(name="MacExportPath", default=" ")
    bpy.types.Scene.web_exports_path = bpy.props.StringProperty(name="WebExportPath", default=" ")
    
    # Android environment vars
    bpy.types.Scene.android_sdk_dirpath = bpy.props.StringProperty(name="Android SDK Folder", subtype="DIR_PATH", default=" ")
    bpy.types.Scene.android_jdk_dirpath = bpy.props.StringProperty(name="JDK Folder", subtype="DIR_PATH", default=" ")
    bpy.types.Scene.android_debug_keystore_filepath = bpy.props.StringProperty(name="Debug Keystore", subtype="FILE_PATH", default=" ")
    
    bpy.types.Object.collider = bpy.props.EnumProperty(
        items = ColliderProperties.collider_options,
        name = "Collider Type",
        description = "Collider type",
        default = "convex")

    
    bpy.types.Object.godot_exportable = bpy.props.BoolProperty(name="Exportable", default=True)
    
    bpy.types.Scene.advanced_tools = bpy.props.BoolProperty(name="Advanced Tools", default=False)

    bpy.types.Scene.player_gravity_on = bpy.props.BoolProperty(name="Gravity", default=True)
    bpy.types.Scene.camera_inverted = bpy.props.BoolProperty(name="Camera Inverted", default=True)
    
    bpy.types.Scene.player_object = bpy.props.EnumProperty(items=fill_player_objects_menu, name="Player", description="Player Object")
    

    # Environment properties
    bpy.types.Scene.sky_on = bpy.props.BoolProperty(name="Sky", default=True)
    bpy.types.Scene.sky_energy = bpy.props.FloatProperty(name="Sky Energy", default=1.0, min=0.0, max=16.0, soft_min=0.0, soft_max=16.0)
    

def clear_properties():
    del bpy.types.Scene.player_object
    

def init_handlers():
    #bpy.app.handlers.depsgraph_update_post.append(update_player_objects)
    pass


def clear_handlers():
    #bpy.app.handlers.depsgraph_update_post.remove(update_player_objects)
    pass


def register():
    init_properties()
    bpy.utils.register_class(game_export.OpenGodotProjectFolderOperator)
    bpy.utils.register_class(game_export.OpenGodotBuildsFolderOperator)
    bpy.utils.register_class(game_export.MessageBoxOperator)
    bpy.utils.register_class(game_export.CompileSelectedVersionsOperator)
    bpy.utils.register_class(scene_properties.SetGodotProjectEnvironmentOperator)
    bpy.utils.register_class(general_tools.ExportProjectToGodotOperator)
    bpy.utils.register_class(game_export.BuildGameOperator)
    bpy.utils.register_class(godot_project_properties.DeleteProjectButtonOperator)
    bpy.utils.register_class(godot_project_properties.AreYouSureDeletingOperator)
    bpy.utils.register_class(godot_project_properties.DeleteProjectOperator)
    bpy.utils.register_class(advanced_tools.ExportGameOperator)
    bpy.utils.register_class(advanced_tools.OpenGodotProjectOperator)
    bpy.utils.register_class(test_project.TestGameOperator)
    bpy.utils.register_class(godot_project_properties.CreateGodotProjectOperator)
    bpy.utils.register_class(addon_config.Blender2GodotPanel)
    bpy.utils.register_class(godot_project_properties.GodotProjectPropertiesPanel)
    bpy.utils.register_class(splash_properties.SplashPropertiesPanel)
    bpy.utils.register_class(display_properties.DisplayPropertiesPanel)
    bpy.utils.register_class(scene_properties.ScenePropertiesPanel)
    bpy.utils.register_class(player_properties.PlayerPropertiesPanel)
    bpy.utils.register_class(advanced_tools.B2G_ToolsPanel)
    bpy.utils.register_class(test_project.TestGamePanel)
    bpy.utils.register_class(game_export.GameExportPanel)
    init_handlers()
    print("Blender2Godot addon loaded.")


def unregister():
    clear_handlers()
    clear_properties()
    bpy.utils.unregister_class(player_properties.PlayerPropertiesPanel)
    bpy.utils.unregister_class(game_export.GameExportPanel)
    bpy.utils.unregister_class(advanced_tools.B2G_ToolsPanel)
    bpy.utils.unregister_class(scene_properties.ScenePropertiesPanel)
    bpy.utils.unregister_class(display_properties.DisplayPropertiesPanel)
    bpy.utils.unregister_class(splash_properties.SplashPropertiesPanel)
    bpy.utils.unregister_class(godot_project_properties.GodotProjectPropertiesPanel)
    bpy.utils.unregister_class(addon_config.Blender2GodotPanel)
    bpy.utils.unregister_class(godot_project_properties.CreateGodotProjectOperator)
    bpy.utils.unregister_class(test_project.TestGamePanel)
    bpy.utils.unregister_class(test_project.TestGameOperator)
    bpy.utils.unregister_class(advanced_tools.OpenGodotProjectOperator)
    bpy.utils.unregister_class(advanced_tools.ExportGameOperator)
    bpy.utils.unregister_class(godot_project_properties.DeleteProjectOperator)
    bpy.utils.unregister_class(godot_project_properties.AreYouSureDeletingOperator)
    bpy.utils.unregister_class(godot_project_properties.DeleteProjectButtonOperator)
    bpy.utils.unregister_class(game_export.BuildGameOperator)
    bpy.utils.unregister_class(general_tools.ExportProjectToGodotOperator)
    bpy.utils.unregister_class(scene_properties.SetGodotProjectEnvironmentOperator)
    bpy.utils.unregister_class(game_export.CompileSelectedVersionsOperator)
    bpy.utils.unregister_class(game_export.MessageBoxOperator)
    bpy.utils.unregister_class(game_export.OpenGodotProjectFolderOperator)
    bpy.utils.unregister_class(game_export.OpenGodotBuildsFolderOperator)
    print("Blender2Godot addon unloaded.")
