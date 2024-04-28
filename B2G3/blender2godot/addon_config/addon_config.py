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
Editor main panel
"""

import os
import subprocess
import shutil
import json
from fileinput import FileInput
from bpy_extras.io_utils import ImportHelper

import bpy


class ProjectTemplatesProperties(bpy.types.PropertyGroup):
    """ Project templates properties """
    project_templates_options = [
        ("blank_template", "Blank", "", "BLANK", 0),
        ("walker_template", "Walker", "", "WALKER", 1),
        ("fps_template", "Fps", "", "FPS", 2)]

class SceneToAddItem(bpy.types.PropertyGroup):
    scene_name: bpy.props.StringProperty(name="Scene Name", default="Unknown")
    scene_exportable: bpy.props.BoolProperty(name="", default=False)
    scene_type : bpy.props.IntProperty(name="", default=0)

def init_properties():
    print("Initiating properties...")
    # Project props
    bpy.types.Scene.game_name = bpy.props.StringProperty(name="Name", default="NEW_GAME")
    bpy.types.Scene.game_folder = bpy.props.StringProperty(name="Game Folder", subtype="DIR_PATH", default=" ")
    bpy.types.Scene.game_icon = bpy.props.StringProperty(name="Game Icon", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.game_icon_image = bpy.props.PointerProperty(name="Game Icon Image", type=bpy.types.Image)
    bpy.types.Scene.project_folder = bpy.props.StringProperty(name="Project Folder", subtype="DIR_PATH", default=" ")
    bpy.types.Scene.godot_executable = bpy.props.StringProperty(name="Godot Path", subtype="FILE_PATH", default="/usr/local/games/godot-engine")
    #bpy.types.Scene.custom_godot = bpy.props.BoolProperty(name="Custom Godot", default=False)
    #bpy.types.Scene.godot_executable_downloaded_zip = bpy.props.StringProperty(name="Godot zip", subtype="FILE_PATH", default=".")
    bpy.types.Scene.colliders_filepath = bpy.props.StringProperty(name="Colliders", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.android_template_filepath = bpy.props.StringProperty(name="Android Template", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.godot_project_filepath = bpy.props.StringProperty(name="GPF", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.project_template = bpy.props.EnumProperty(items = fill_project_templates, name = "Project Template", description = "Project type")#, default = "blank_template")
    bpy.types.Scene.scenes_added_index = bpy.props.IntProperty(name = "Index for my_list", default = 0)
    bpy.types.Scene.startup_scene = bpy.props.PointerProperty(type=bpy.types.Scene, name="Startup Scene")
    
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

    # Scene props
    bpy.types.Scene.scene_exportable = bpy.props.BoolProperty(name="", default=False)
    bpy.types.Scene.scene_type = bpy.props.IntProperty(name="Type", default=0)

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
    
    # Panels checkboxes
    bpy.types.Scene.advanced_tools = bpy.props.BoolProperty(name="Advanced Tools", default=False)
    
    print("Properties initiated.")

def clear_properties():
    #del bpy.types.Scene.player_object
    #del bpy.types.Scene.scenes_added
    del bpy.types.Scene.scenes_added_index

"""
def check_player_objects():
    if len(player_objects) != len(bpy.context.scene.objects):
        self.fill_player_object_menu(bpy.context)
"""

def fill_project_templates(self, context):
    _templates = []
    _templates.clear()
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "project_templates"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "project_templates")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _dirs_list = os.listdir(p_path)
            _index = 0
            for _dir_name in _dirs_list:
                _name = _dir_name.removesuffix("_template")
                _new_template = (_dir_name, _name.capitalize(), _name.upper())
                _templates.append(_new_template)
                _index += 1
    return _templates

def update_player_objects(aa):
    pass

class CreateGameManagerOperator(bpy.types.Operator):
    """Create Game Manager Operator"""
    bl_idname = "scene.create_gamemanager_operator"
    bl_label = "Create Game Manager"


    def execute(self, context):
        print("Creating Game Manager")
        _new_scene = bpy.data.scenes.new(context.scene.gamemanager_scene_name)
        context.window.scene = _new_scene
        return {'FINISHED'}


class SaveBlendFileOperator(bpy.types.Operator, ImportHelper):
    bl_idname = "scene.saveblendfile_operator"
    bl_label = "Save Blend File"

    def execute(self, context):
        if self.filepath.endswith(".blend"):
            pass
        else:
            self.filepath += ".blend"
        bpy.ops.wm.save_as_mainfile(filepath=self.filepath, check_existing=True, filter_blender=True)
        return {'FINISHED'}

class Blender2GodotPanel(bpy.types.Panel):
    """Blender2Godot Panel"""
    bl_label = "B2G Configuration"
    bl_idname = "BLENDER2GODOT_PT_layout"
    bl_description = "Main Blender2Godot Panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_order = 0

    _gamemanager_added = False
    _in_gamemanager = False

    @classmethod 
    def poll(self, context):
        _gm_index = bpy.data.scenes.find(context.scene.gamemanager_scene_name)
        self._gamemanager_added = (_gm_index > -1)
        self._in_gamemanager = (context.scene.name == context.scene.gamemanager_scene_name)
        return (self._in_gamemanager or not self._gamemanager_added)

    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="PLUGIN")        
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        blend_data = context.blend_data
        if not self._gamemanager_added:
            row = layout.row()
            box = row.box()
            box.operator("scene.create_gamemanager_operator")
        else:
            # Addon settings
            row = layout.row()
            box = row.box()
            box.label(text="Main Config:")
            row = box.row()
            box = box.box()        
            box.prop(scene, "godot_executable", icon="FILE")
            if not bpy.data.is_saved:
                box1 = box.box()     
                box1.label(text="Save blend file to continue", icon="ERROR")
                row2 = box1.row()
                row2.operator("scene.saveblendfile_operator", text="Save File")	

def register():
    bpy.utils.register_class(SceneToAddItem)
    init_properties()
    bpy.utils.register_class(SaveBlendFileOperator)
    bpy.utils.register_class(CreateGameManagerOperator)
    bpy.utils.register_class(Blender2GodotPanel)

def unregister():
    clear_properties()
    bpy.utils.unregister_class(SaveBlendFileOperator)
    bpy.utils.unregister_class(Blender2GodotPanel)
    bpy.utils.unregister_class(CreateGameManagerOperator)
    bpy.utils.unregister_class(SceneToAddItem)
