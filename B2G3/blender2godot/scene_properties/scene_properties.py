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
from blender2godot.addon_config import addon_config # type: ignore

global object_types
object_types = [
    ("none", "None", "", 0),
    ("player_spawn_empty", "Player Spawn Point", "", 1),
    ("trigger_zone", "Trigger Zone", "", 2),
    ("entity", "Entity", "", 3),
]

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

global property_types
property_types = [
    ("boolean", "Boolean", "", "", 0),
    ("integer", "Integer", "", "", 1),
    ("float", "Float", "", "", 2),
    ("string", "String", "", "", 3)
]

def check_property_name(self, value):
    _new_value = value
    for _prop in bpy.context.scene.entity_properties:
        if _new_value == "none": # name "none" is not allowed
            _new_value = _prop["property_name"] + "0"
            _new_value = check_property_name(self, _new_value)
        if _prop != self:
            if _prop["property_name"] == _new_value:
                _new_value = _prop["property_name"] + "0"
                _new_value = check_property_name(self, _new_value)
    return _new_value

def get_property_name(self):
    return self["property_name"]

def set_property_name(self, value):
    _new_value = check_property_name(self, value)
    self["property_name"] = _new_value

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

class EntityProperty(bpy.types.PropertyGroup):
    property_name : bpy.props.StringProperty(name="Prop_Name", set=set_property_name, get=get_property_name) # type: ignore
    property_type : bpy.props.EnumProperty(items=property_types, name="Type") # type: ignore
    property_value : bpy.props.StringProperty(name="Default") # type: ignore
    #property_boolean : bpy.props.BoolProperty(name="Default") # type: ignore
    #property_float : bpy.props.FloatProperty(name="Default") # type: ignore
    #property_integer : bpy.props.IntProperty(name="Default") # type: ignore

class SceneType(bpy.types.PropertyGroup):
    """ Scene type """
    scene_type_options = scene_types

class AddObjectEntityPropertyOperator(bpy.types.Operator):
    bl_idname = "object.add_object_entity_property_operator"
    bl_label = "Add Property"
    bl_description = "Add a new property"
    bl_options = {"UNDO", "REGISTER"}

    property_name : bpy.props.StringProperty(name="Property Name", default="Property_Name") # type: ignore
    property_type : bpy.props.EnumProperty(items=property_types) # type: ignore
    
    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row0 = box.row()
        row0.prop(self, "property_name", text="Property Name")
        row1 = box.row()
        row1.prop(self, "property_type", text="Property Type")
        #for _prop in context.scene.entity_properties:
            #if _prop.property_name == self.property_name:
                #row2 = box.row()
                #row2.label(text="Prop name duplicated", icon="ERROR")
    
    def execute(self, context):
        _new_property = context.active_object.entity_properties.add()
        _new_property.property_name = self.property_name
        _new_property.property_type = self.property_type
        return {"FINISHED"}

class AddSceneEntityPropertyOperator(bpy.types.Operator):
    bl_idname = "scene.add_scene_entity_property_operator"
    bl_label = "Add Property"
    bl_description = "Add a new property"
    bl_options = {"UNDO", "REGISTER"}

    property_name : bpy.props.StringProperty(name="Property Name", default="Property_Name") # type: ignore
    property_type : bpy.props.EnumProperty(items=property_types) # type: ignore
    
    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        row0 = box.row()
        row0.prop(self, "property_name", text="Property Name")
        row1 = box.row()
        row1.prop(self, "property_type", text="Property Type")
        #for _prop in context.scene.entity_properties:
            #if _prop.property_name == self.property_name:
                #row2 = box.row()
                #row2.label(text="Prop name duplicated", icon="ERROR")
    
    def execute(self, context):
        _new_property = context.scene.entity_properties.add()
        _new_property.property_name = self.property_name
        _new_property.property_type = self.property_type
        return {"FINISHED"}

class RemoveObjectEntityPropertyOperator(bpy.types.Operator):
    bl_idname = "object.remove_object_entity_property_operator"
    bl_label = "Remove Property"
    bl_description = "Remove property"
    bl_options = {"UNDO", "REGISTER"}

    prop_to_remove_name : bpy.props.StringProperty(name="Propname") # type: ignore
   
    @classmethod
    def poll(cls, context):
        return True
   
    def execute(self, context):
        prop_to_remove_index = -1
        for _ind,_prop in enumerate(context.active_object.entity_properties):
            if _prop.property_name == self.prop_to_remove_name:
                prop_to_remove_index = _ind
                break
        if prop_to_remove_index > -1:
            context.active_object.entity_properties.remove(prop_to_remove_index)
        return {"FINISHED"}

class RemoveSceneEntityPropertyOperator(bpy.types.Operator):
    bl_idname = "scene.remove_scene_entity_property_operator"
    bl_label = "Remove Property"
    bl_description = "Remove property"
    bl_options = {"UNDO", "REGISTER"}

    prop_to_remove_name : bpy.props.StringProperty(name="Propname") # type: ignore
   
    @classmethod
    def poll(cls, context):
        return True
   
    def execute(self, context):
        prop_to_remove_index = -1
        for _ind,_prop in enumerate(context.scene.entity_properties):
            if _prop.property_name == self.prop_to_remove_name:
                prop_to_remove_index = _ind
                break
        if prop_to_remove_index > -1:
            context.scene.entity_properties.remove(prop_to_remove_index)
        return {"FINISHED"}

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
        scene = context.scene
        row = layout.row()
        row.alignment = "EXPAND"
        column1 = row.column()
        if hasattr(context.scene, "scene_type"):
            column1.prop(context.scene, "scene_type")
        column2 = row.column(align=True)
        column2.ui_units_x = 5.0
        if hasattr(context.scene, "scene_exportable"):
            column2.prop(context.scene, "scene_exportable")
        # Entity properties
        if scene.scene_type != "none":
            row1 = layout.row()
            box4 = row1.box()
            row4 = box4.row()
            row4.label(text="Scene Properties:", icon_value=addon_config.preview_collections[0]["properties_icon"].icon_id)
            for _property in scene.entity_properties:
                box2 = box4.box()
                row5 = box2.row()
                column0 = row5.column()
                column0.prop(_property, "property_name", text="Name")
                column1 = row5.column()
                column1.prop(_property, "property_type")
                #column2 = row5.column()
                #column2.prop(_property, "property_value")
                column3 = row5.column()
                column3.operator(operator="scene.remove_scene_entity_property_operator", text="X").prop_to_remove_name = _property.property_name
            row6 = box4.row()
            row6.operator("scene.add_scene_entity_property_operator")

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
    bpy.types.Object.physics_group = bpy.props.EnumProperty(items=get_physics_groups, name="Physics Groups", options={"ENUM_FLAG"}, update=on_object_physics_groups_update) # OBJECT GROUPS FOR COLLISIONS
    bpy.types.Scene.entity_properties = bpy.props.CollectionProperty(type=EntityProperty, name="SceneEntityProperties")
    bpy.types.Scene.entity_property_sel = bpy.props.IntProperty(name="Scene Entity Property Selected", default=0)
    bpy.types.Object.entity_properties = bpy.props.CollectionProperty(type=EntityProperty, name="ObjectEntityProperties")
    bpy.types.Object.entity_property_sel = bpy.props.IntProperty(name="Object Entity Property Selected", default=0)
    bpy.types.Object.object_type = bpy.props.EnumProperty(items=object_types, name="Object Type")
    bpy.types.Object.is_visible = bpy.props.BoolProperty(name="Visible", default=True)

def clear_properties():
    #del bpy.types.Scene.scene_environment
    del bpy.types.Scene.scene_type
    del bpy.types.Scene.scene_exportable
    del bpy.types.Object.godot_exportable
    del bpy.types.Object.physics_group
    del bpy.types.Scene.entity_properties
    del bpy.types.Scene.entity_property_sel
    del bpy.types.Object.entity_properties
    del bpy.types.Object.entity_property_sel
    del bpy.types.Object.object_type
    del bpy.types.Object.is_visible

def register():
    bpy.utils.register_class(EntityProperty)
    bpy.utils.register_class(AddObjectEntityPropertyOperator)
    bpy.utils.register_class(AddSceneEntityPropertyOperator)
    bpy.utils.register_class(RemoveSceneEntityPropertyOperator)
    bpy.utils.register_class(RemoveObjectEntityPropertyOperator)
    init_properties()
    bpy.utils.register_class(ScenePropertiesPanel)

def unregister():
    bpy.utils.unregister_class(ScenePropertiesPanel)
    clear_properties()
    bpy.utils.unregister_class(RemoveObjectEntityPropertyOperator)
    bpy.utils.unregister_class(RemoveSceneEntityPropertyOperator)
    bpy.utils.unregister_class(AddObjectEntityPropertyOperator)
    bpy.utils.unregister_class(AddSceneEntityPropertyOperator)
    bpy.utils.unregister_class(EntityProperty)

