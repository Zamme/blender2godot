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

def get_scenes_names(self, context):
    _sc_names_purged = [("none", "None", "NONE", "", 0)]
    _sc_ind = 1
    for _sc in bpy.data.scenes:
        if _sc.name != "B2G_GameManager" and _sc != context.scene:
            if context.active_object.special_object_info.button_action_on_click == "load_stage" and _sc.scene_type == "stage":
                _sc_names_purged.append((_sc.name.lower(), _sc.name, _sc.name.upper(), "", _sc_ind))
                _sc_ind += 1
            elif context.active_object.special_object_info.button_action_on_click == "load_menu" and _sc.scene_type == "3dmenu":
                _sc_names_purged.append((_sc.name.lower(), _sc.name, _sc.name.upper(), "", _sc_ind))
                _sc_ind += 1
    return _sc_names_purged

def scene_camera_object_poll(self, object):
    return ((object.users_scene[0] == bpy.context.scene) and (object.type == 'CAMERA'))

class MenuSpecialObject(bpy.types.PropertyGroup):
    menu_object_type : bpy.props.EnumProperty(items=[("none", "None", "NONE", 0), 
                                                                      ("button", "Button", "BUTTON", 1),
                                                                      ("checkbox", "Checkbox", "CHECKBOX", 2)],
                                                                        name="Type") # type: ignore
    button_action_on_click : bpy.props.EnumProperty(items=[("none", "None", "NONE", 0), 
                                                                      ("load_stage", "Load Stage", "LOAD_STAGE", 1),
                                                                      ("load_menu", "Load Menu", "LOAD_MENU", 2),
                                                                      ("quit_game", "Quit Game", "QUIT_GAME", 3)],
                                                                        name="Action On Click") # type: ignore
    button_action_parameter : bpy.props.StringProperty(name="Parameter", default="") # type: ignore
    #scene_link : bpy.props.StringProperty(name="Stage Link") # type: ignore
    scene_link : bpy.props.EnumProperty(items=get_scenes_names, name="Stage Link") # type: ignore

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
        if hasattr(context.scene, "scene_type"):
            if (context.scene.scene_type == "3dmenu"):
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
                box4.prop(context.active_object.special_object_info, "menu_object_type")
                if context.active_object.special_object_info.menu_object_type == "button":
                    box4.prop(context.active_object.special_object_info, "button_action_on_click")
                    if context.active_object.special_object_info.button_action_on_click == "load_stage":
                        box4.prop(context.active_object.special_object_info, "scene_link")
                    elif context.active_object.special_object_info.button_action_on_click == "load_menu":
                        box4.prop(context.active_object.special_object_info, "scene_link")
            box3.prop(context.active_object, "godot_exportable")
                 

def init_properties():
    bpy.types.Scene.menu_camera_object = bpy.props.PointerProperty(type=bpy.types.Object, name="Menu Camera", poll=scene_camera_object_poll)
    bpy.types.Object.special_object_info = bpy.props.PointerProperty(type=MenuSpecialObject, name="Object Info")

def clear_properties():
    del bpy.types.Scene.menu_camera_object
    del bpy.types.Object.special_object_info

def register():
    bpy.utils.register_class(MenuSpecialObject)
    init_properties()
    bpy.utils.register_class(Menu3DPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(Menu3DPropertiesPanel)
    bpy.utils.unregister_class(MenuSpecialObject)
    clear_properties()


