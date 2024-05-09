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
For menus 
"""

import bpy


def button_scene_object_poll(self, scene):
    return (scene.name != "B2G_GameManager")

def scene_camera_object_poll(self, object):
    return ((object.users_scene[0] == bpy.context.scene) and (object.type == 'CAMERA'))

class MenuPropertiesPanel(bpy.types.Panel):
    """Menu Properties Panel"""
    bl_label = "Menu Properties"
    bl_idname = "MENUPROPERTIES_PT_layout"
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
        if hasattr(context.scene, "scene_type"):
            if (context.scene.scene_type == "menu"):
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
            box4.prop(context.active_object, "menu_object_type")
            if context.active_object.menu_object_type == "button":
                box4.prop(context.active_object, "button_action_on_click")
                if context.active_object.button_action_on_click == "load_scene":
                    box4.prop(context.active_object, "button_action_parameter", text="")
            box4.prop(context.active_object, "godot_exportable")
                 

def init_properties():
    bpy.types.Scene.menu_camera_object = bpy.props.PointerProperty(type=bpy.types.Object, name="Menu Camera", poll=scene_camera_object_poll)
    bpy.types.Object.menu_object_type = bpy.props.EnumProperty(items=[("none", "None", "NONE"), 
                                                                      ("button", "Button", "BUTTON"),
                                                                      ("checkbox", "Checkbox", "CHECKBOX")],
                                                                        name="Type")
    bpy.types.Object.button_action_on_click = bpy.props.EnumProperty(items=[("none", "None", "NONE"), 
                                                                      ("load_scene", "Load Scene", "LOAD_SCENE"),
                                                                      ("quit_game", "Quit Game", "QUIT_GAME")],
                                                                        name="Action On Click")
    bpy.types.Object.button_action_parameter = bpy.props.PointerProperty(type=bpy.types.Scene, name="Parameter", poll=button_scene_object_poll)

def clear_properties():
    pass

def register():
    init_properties()
    bpy.utils.register_class(MenuPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(MenuPropertiesPanel)
    clear_properties()


