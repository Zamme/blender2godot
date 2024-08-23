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
Scene properties panel
"""

import bpy
from bpy.app.handlers import persistent

global scene_types
scene_types = [
    ("none", "None", "", 0),
    ("stage", "Stage", "", 1),
    ("player", "Player", "", 2),
    ("3dmenu", "3D Menu", "", 3),
    ("2dmenu", "2D Menu", "", 4),
    ("hud", "HUD", "", 5),
    ("loading", "Loading", "", 6),
    ("npc", "NPC", "", 7),
    ("overlay_menu", "Overlay Menu", "", 8),
    ]

def get_physics_groups(self, context):
    _pgs = []
    '''
    [
        ("none", "None", "NONE"),
    ]
    '''
    for _pg in bpy.data.scenes["B2G_GameManager"].physics_groups:
        _pgs.append((_pg.name, _pg.name, _pg.name))
    return _pgs

def on_object_physics_groups_update(self, context):
    pass

def show_error_popup(message = [], title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        for _error in message:
           self.layout.label(text=_error, icon="ERROR")
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def scene_emptyobject_poll(self, object):
    return object.type == 'EMPTY'

def scene_type_update(self, context):
    # ADAPT SCENE RESOLUTION TO DISPLAY SETTINGS
    context.scene.render.resolution_x = bpy.data.scenes["B2G_GameManager"].render.resolution_x
    context.scene.render.resolution_y = bpy.data.scenes["B2G_GameManager"].render.resolution_y
    # INITIALIZE SOME SCENE TYPES ON SCENE TYPE CRITERIA
    match context.scene.scene_type:
        case "player":
            if (len(context.scene.controls_settings) == 0):
                print("controls updated")
                context.scene.controls_settings.clear()
                _new_setting = context.scene.controls_settings.add()
                _new_setting.motion_name = "b2g_go_forward"
                _new_setting = context.scene.controls_settings.add()
                _new_setting.motion_name = "b2g_go_backward"
                _new_setting = context.scene.controls_settings.add()
                _new_setting.motion_name = "b2g_strafe_left"
                _new_setting = context.scene.controls_settings.add()
                _new_setting.motion_name = "b2g_strafe_right"
                _new_setting = context.scene.controls_settings.add()
                _new_setting.motion_name = "b2g_rotate_left"
                _new_setting = context.scene.controls_settings.add()
                _new_setting.motion_name = "b2g_rotate_right"
                _new_setting = context.scene.controls_settings.add()
                _new_setting.motion_name = "b2g_rotate_up"
                _new_setting = context.scene.controls_settings.add()
                _new_setting.motion_name = "b2g_rotate_down"
                _new_setting = context.scene.controls_settings.add()
                _new_setting.motion_name = "b2g_action_0"
                _new_setting = context.scene.controls_settings.add()
                _new_setting.motion_name = "b2g_action_1"
                _new_setting = context.scene.controls_settings.add()
                _new_setting.motion_name = "b2g_action_2"
                _new_setting = context.scene.controls_settings.add()
                _new_setting.motion_name = "b2g_action_3"
                _new_setting = context.scene.controls_settings.add()
                _new_setting.motion_name = "b2g_pause_game"

def update_scene_exportable(self, context):
    if bpy.data.scenes[self.name].scene_type == "player":
        if bpy.data.scenes[self.name].player_object != None:
            print("Updating player scene exportable")
            if bpy.data.scenes[self.name].camera_object == None:
                if bpy.data.scenes[self.name].scene_exportable:
                    bpy.data.scenes[self.name].scene_exportable = False
                    show_error_popup(["Set camera object in player"], "Error detected", "CANCEL")

class SceneType(bpy.types.PropertyGroup):
    """ Scene type """
    scene_type_options = scene_types

class ScenePropertiesPanel(bpy.types.Panel):
    """Scene Properties Panel"""
    bl_label = "Scene Properties"
    bl_idname = "SCENEPROPERTIES_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    #bl_options = {"DEFAULT_CLOSED"}
    bl_order = 2

    _gamemanager_added = False
    _not_in_gamemanager = False

    @classmethod 
    def poll(self, context):
        _gm_index = bpy.data.scenes.find(context.scene.gamemanager_scene_name)
        self._gamemanager_added = (_gm_index > -1)
        self._not_in_gamemanager = (context.scene.name != context.scene.gamemanager_scene_name)
        return (self._not_in_gamemanager and self._gamemanager_added)
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="SEQ_PREVIEW")
    
    def draw(self, context):
        layout = self.layout
        
        if not bpy.data.is_saved:       
            return
        
        # SCENE PROPERTIES
        row = layout.row()
        row.alignment = "EXPAND"
        column1 = row.column()
        if hasattr(context.scene, "scene_type"):
            column1.prop(context.scene, "scene_type")
        column2 = row.column(align=True)
        column2.ui_units_x = 5.0
        if hasattr(context.scene, "scene_exportable"):
            column2.prop(context.scene, "scene_exportable")

def init_properties():
    # Scene props
    bpy.types.Scene.scene_type = bpy.props.EnumProperty(
        items = SceneType.scene_type_options,
        name = "Scene Type",
        description = "Scene type",
        default = 0,
        update=scene_type_update)
    bpy.types.Scene.scene_exportable = bpy.props.BoolProperty(name="Export", default=False, update=update_scene_exportable) # SCENE EXPORTABLE
    #bpy.types.Scene.scene_environment = bpy.props.PointerProperty(type=bpy.types.World, name="Environment")
    # Object props
    bpy.types.Object.godot_exportable = bpy.props.BoolProperty(name="Export", default=True) # OBJECT EXPORTABLE
    #bpy.types.Object.physics_group = bpy.props.StringProperty(name="Physics Group", default="") # OBJECT GROUP FOR COLLISIONS
    bpy.types.Object.physics_group = bpy.props.EnumProperty(items=get_physics_groups, name="Physics Groups", options={"ENUM_FLAG"}, update=on_object_physics_groups_update) # OBJECT GROUPS FOR COLLISIONS

def clear_properties():
    #del bpy.types.Scene.scene_environment
    del bpy.types.Scene.scene_type
    del bpy.types.Scene.scene_exportable
    del bpy.types.Object.godot_exportable
    del bpy.types.Object.physics_group

def register():
    init_properties()
    bpy.utils.register_class(ScenePropertiesPanel)

def unregister():
    bpy.utils.unregister_class(ScenePropertiesPanel)
    clear_properties()

