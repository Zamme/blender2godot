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
For 3d Menus 
"""

import bpy

'''
def button_scene_object_poll(self, scene):
    return (scene.name != "B2G_GameManager")
'''

def button_scene_object_poll():
    pass

def get_scene_parameter_name(self, context):
    _parameter_name = context.active_object.special_object_info.button_action_on_click.removeprefix("load_").capitalize()
    return _parameter_name

def scene_camera_object_poll(self, object):
    return ((object.users_scene[0] == bpy.context.scene) and (object.type == 'CAMERA'))

class Menu3DSpecialObject(bpy.types.PropertyGroup):
    """ Menu 3D Object Type """
    object_type_options = [
                            ("none", "None", "", 0), 
                            ("button", "Button", "", 1),
                            ("checkbox", "Checkbox", "", 2)
                            ]
    menu_object_type : bpy.props.EnumProperty(items=object_type_options, name="Type") # type: ignore

class Menu3DPropertiesPanel(bpy.types.Panel):
    """Menu 3D Properties Panel"""
    bl_label = "Menu 3D Properties"
    bl_idname = "MENU3DPROPERTIES_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 3
    
    _gamemanager_added = False
    _not_in_gamemanager = False

    @classmethod 
    def poll(self, context):
        _ret = False
        _gm_index = bpy.data.scenes.find(context.scene.gamemanager_scene_name)
        self._gamemanager_added = (_gm_index > -1)
        if self._gamemanager_added:
            if hasattr(context.scene, "scene_type"):
                if ((context.scene.scene_type == "3dmenu") and (context.scene.name != context.scene.gamemanager_scene_name)):
                    _ret = True
        return _ret
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="OUTLINER")        
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if not bpy.data.is_saved:       
            return

        # PROPERTIES
        row1 = layout.row()
        box1 = row1.box()
        # CAMERA
        box2 = box1.box()
        box2.prop(scene, "menu_camera_object")

        # ACTIVE OBJECT PROPERTIES
        if context.active_object is not None:
            row2 = box1.row()
            box3 = row2.box()
            _nl = "Active Object: " + context.active_object.name
            box3.label(text=_nl)
            box4 = box3.box()
            if context.active_object.type == "CAMERA":
                box4.prop(context.active_object.data, "angle")
            else:
                if hasattr(context.active_object, "special_object_info"):
                    box4.prop(context.active_object.special_object_info, "menu_object_type")
                    #if context.active_object.special_object_info.menu_object_type == "button":
                        #box4.prop(context.active_object.special_object_info, "button_action_on_click")
                        #_act = context.active_object.special_object_info.button_action_on_click
                        #if _act != "none" and _act != "quit_game":
                            #_param_name = get_scene_parameter_name(self, context)
                            #box4.prop(context.active_object.special_object_info, "scene_parameter", text=_param_name)
            box3.prop(context.active_object, "godot_exportable")
                 

def init_properties():
    bpy.types.Scene.menu_camera_object = bpy.props.PointerProperty(type=bpy.types.Object, name="Menu Camera", poll=scene_camera_object_poll)
    bpy.types.Object.special_object_info = bpy.props.PointerProperty(type=Menu3DSpecialObject)

def clear_properties():
    del bpy.types.Scene.menu_camera_object
    del bpy.types.Object.special_object_info

def register():
    bpy.utils.register_class(Menu3DSpecialObject)
    init_properties()
    bpy.utils.register_class(Menu3DPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(Menu3DPropertiesPanel)
    clear_properties()
    bpy.utils.unregister_class(Menu3DSpecialObject)


