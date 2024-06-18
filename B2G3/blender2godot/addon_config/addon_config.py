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
from bpy_extras.io_utils import ImportHelper
from bpy.utils import previews

import bpy


handle = object()
subscribe_to = bpy.types.Window, "scene"

global preview_collections
preview_collections = []


def check_godot(self, context):
    context.scene.godot_engine_ok = False
    print("Checking", self.godot_executable)
    if os.path.isfile(self.godot_executable):
        _filename = os.path.basename(self.godot_executable)
        if _filename.startswith("Godot"):
            _result = None
            try:
                _result = subprocess.run([self.godot_executable, "--version"], capture_output=True, text=True)
                #print("Type:", type(_result))
            except:
                context.scene.godot_engine_ok = False
            else:
                if type(_result) is subprocess.CompletedProcess:
                    if _result.returncode == 0:
                        if _result.stdout.startswith("3.5"):
                            print("Godot Engine version 3.5 OK")
                        elif _result.stdout.startswith("4."):
                            print("Godot Engine version 4.x OK")
                        context.scene.godot_engine_ok = True
                    else:
                        print("Godot Engine Error")
                        context.scene.godot_engine_ok = False
                else:
                    context.scene.godot_engine_ok = False

def load_custom_icons():
    custom_icons = previews.new()
    custom_icons_dirpath = ""
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "icons"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "icons")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            custom_icons_dirpath = p_path
            _list_dir = os.listdir(custom_icons_dirpath)
            for _list_item in _list_dir:
                _list_item_name = _list_item.removesuffix(".png")
                _list_item_path = os.path.join(custom_icons_dirpath,_list_item)
                if os.path.isfile(_list_item_path):
                    custom_icons.load(
                                name=_list_item_name,
                                path=_list_item_path,
                                path_type="IMAGE"
                                        )
                    #print("Icon item path:", _list_item_path)
                    #print("Icon name:", _list_item_name)
            break
    preview_collections.append(custom_icons)

def msgbus_callback(*args):
    bpy.context.scene.render.resolution_x = bpy.data.scenes["B2G_GameManager"].render.resolution_x
    bpy.context.scene.render.resolution_y = bpy.data.scenes["B2G_GameManager"].render.resolution_y

def init_properties():
    bpy.types.Scene.godot_executable = bpy.props.StringProperty(name="Godot Path", subtype="FILE_PATH", default="/usr/local/games/godot-engine", update=check_godot)  
    bpy.types.Scene.godot_engine_ok = bpy.props.BoolProperty(name="Godot OK", default=False)

def clear_properties():
    del bpy.types.Scene.godot_engine_ok
    del bpy.types.Scene.godot_executable
    for pcoll in preview_collections:
        bpy.utils.previews.remove(pcoll)
    preview_collections.clear()

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
        if context.scene.godot_exporting or context.scene.is_game_exporting:       
            layout.enabled = False
        else:
            layout.enabled = True

        scene = context.scene
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
            if not bpy.data.is_saved:
                box1 = box.box()     
                box1.label(text="Save blend file to continue", icon="ERROR")
                row2 = box1.row()
                row2.operator("scene.saveblendfile_operator", text="Save File")
            else:
                box.prop(scene, "godot_executable", icon="FILE")
                row3 = box.row()
                row3.alignment="CENTER"
                if context.scene.godot_engine_ok:
                    row3.label(text="Godot Engine OK", icon_value=preview_collections[0]["ok_green"].icon_id)
                else:
                    row3.label(text="Set godot executable path", icon_value=preview_collections[0]["error_yellow"].icon_id)

def register():
    bpy.msgbus.subscribe_rna(
        key=subscribe_to,
        owner=handle,
        args=(1, 2, 3),
        notify=msgbus_callback,
        options={"PERSISTENT"}
    )
    init_properties()
    load_custom_icons()
    bpy.utils.register_class(SaveBlendFileOperator)
    bpy.utils.register_class(CreateGameManagerOperator)
    bpy.utils.register_class(Blender2GodotPanel)

def unregister():
    bpy.utils.unregister_class(SaveBlendFileOperator)
    bpy.utils.unregister_class(Blender2GodotPanel)
    bpy.utils.unregister_class(CreateGameManagerOperator)
    clear_properties()
    bpy.msgbus.clear_by_owner(handle)
