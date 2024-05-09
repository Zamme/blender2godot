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
For player behaviour
"""

import bpy
import json
import os


def scene_camera_object_poll(self, object):
    return ((object.users_scene[0] == bpy.context.scene) and (object.type == 'CAMERA'))

def scene_player_object_poll(self, object):
    return ((object.users_scene[0] == bpy.context.scene) and (object.type == 'MESH' or object.type == 'ARMATURE'))

def camera_update(self, context):
    context.scene.scene_exportable = (context.scene.camera_object != None)  

def controls_update(self, context):
    _template_path = ""
    _template_properties_path = ""
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "project_templates", bpy.data.scenes["B2G_GameManager"].project_template),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "project_templates", bpy.data.scenes["B2G_GameManager"].project_template)]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _template_path = p_path
    _template_properties_path = _template_path + "_properties.json"
    #print("Template path: ", _template_path)
    #print("Template properties path: ", _template_properties_path)
    _template_properties = {}
    with open(_template_properties_path) as f:
        _template_properties = json.load(f)
    _json_player_inputs = _template_properties["PlayerInputs"]
        
    context.scene.controls_settings.clear()

    if ((len(context.scene.controls_settings) == 0) or (len(context.scene.controls_settings) > len(_json_player_inputs.keys()))):
        context.scene.controls_settings.clear()
        for _key in _json_player_inputs.keys():
            _new_setting = context.scene.controls_settings.add()
            _new_setting.motion_name = _key
            _new_setting.motion_input_blender = _json_player_inputs[_key][0]
            _new_setting.motion_input_godot = _json_player_inputs[_key][1]

class AnimationTypeProperties(bpy.types.PropertyGroup):
    """ Animation Type properties """
    animation_type_options = [
        ("none", "None", "", 0),
        ("forward", "Forward", "", 1),
        ("backward", "Backward", "", 2),
        ("idle", "Idle", "", 3),
        ("jump", "Jump", "", 4)]

class ANIMATIONS_UL_armature_animations(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        custom_icon = 'OUTLINER_DATA_ARMATURE'
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon=custom_icon)
            layout.prop(item, "animation_type", text="", icon="NONE")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = custom_icon)

class CONTROLS_UL_player_input(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.motion_name, icon="POSE_HLT")
            layout.prop(item, "motion_input_blender", text="", event=True)
            #layout.label(text=item.motion_input_blender, icon="VIEW_PAN")
#            layout.prop(item, "motion_input", text="", icon="NONE")
            #layout.operator("scene.process_input").control_index = index
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = "POSE_HLT")

class ControlsProperties(bpy.types.PropertyGroup):
    motion_name: bpy.props.StringProperty(name="Motion Name", default="Unknown") # type: ignore
    motion_input_blender: bpy.props.StringProperty(name="Blender Input", default="None") # type: ignore
    motion_input_godot: bpy.props.StringProperty(name="Godot Input", default="None") # type: ignore

class ControlSettingsType(bpy.types.PropertyGroup):
    """ Control settings type """
    control_settings_type_options = [
        ("keyboard", "Keyboard", "", 0),
        ("joypad", "Joypad", "", 1)]

class ControlInputProperty(bpy.types.PropertyGroup):
    """ Control input property """
    control_input_options = []
    #for _control_item in bpy.types.KeyMap.keys():
        #print("Key key: ", _control_item)
    #    ("keyboard", "Keyboard", "", 0),
     #   ("joypad", "Joypad", "", 1)]

class SCENE_OT_get_input(bpy.types.Operator):
    """Get input key."""
    bl_idname = 'scene.process_input'
    bl_label = 'Edit'
    bl_options = {'REGISTER'}

    control_index : bpy.props.IntProperty(name="ControlIndex") # type: ignore

    def modal(self, context, event):
        if event.type == 'ESC':
            print("esc catched")
            return {'FINISHED'}
        elif event.value == "PRESS":
            context.scene.controls_settings[self.control_index].motion_input = event.type
            return {'FINISHED'}
        #elif event.ctrl:
            #pass # Input processing code.

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class PlayerPropertiesPanel(bpy.types.Panel):
    """Player Properties Panel"""
    bl_label = "Player Properties"
    bl_idname = "PLAYERPROPERTIES_PT_layout"
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
            if (context.scene.scene_type == "player"):
                _ret = True
        return _ret
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="ARMATURE_DATA")        
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if not bpy.data.is_saved:       
            return

        # INITIAL PROPERTIES
        row = layout.row()
        row.prop(scene, "player_object")

        if not scene.player_object:
            return

        # Player animations
        row = layout.row()
        box = row.box()
        box.label(text="Animations")
        if scene.player_object == None:
            box.label(text="No player object assigned", icon="ERROR")
        else:
            if scene.player_object.type != "ARMATURE":
                _mess = "No armature in player object."
                _ic = "ERROR"
                box.label(text=_mess, icon=_ic)
            else:
                _mess = "Player armature : " + scene.player_object.name
                _ic = "OUTLINER_OB_ARMATURE"
                box1 = box.box()
                box1.template_list("ANIMATIONS_UL_armature_animations", "PlayerAnimationsList", bpy.data, "actions", scene, "player_animation_sel")
                box.label(text=_mess, icon=_ic)

        # Player motion
        row = layout.row()
        box = row.box()
        box.label(text="Player Motion")
        
        # TODO : controls settings unfinished
        box2 = box.box()
        box2.prop(scene, "controls_settings_type")
        if scene.controls_settings_type == "keyboard":
            box2.template_list("CONTROLS_UL_player_input", "PlayerControlsList", context.scene, "controls_settings", scene, "controls_settings_sel")
        else:
            box2.label(text="Inputs:")

        box.prop(scene, "player_gravity_on")
        box.prop(scene, "camera_control_inverted")

        # Player camera
        row = layout.row()
        box = row.box()
        box.label(text="Camera Properties")
        box.prop(scene, "camera_object")
        if scene.camera_object == None:
            box.label(text="No camera object assigned", icon="ERROR")
        box.prop(scene, "camera_fov")

def init_properties():
    # Player properties
    bpy.types.Action.animation_type = bpy.props.EnumProperty(
        items = AnimationTypeProperties.animation_type_options,
        name = "Animation Type",
        description = "Animation type",
        default = "none")

    bpy.types.Scene.player_gravity_on = bpy.props.BoolProperty(name="Gravity", default=True)
    bpy.types.Scene.camera_control_inverted = bpy.props.BoolProperty(name="Camera Y Inverted", default=True)
    bpy.types.Scene.camera_object = bpy.props.PointerProperty(type=bpy.types.Object, name="Camera Object", description="Camera Object", poll=scene_camera_object_poll, update=camera_update)
    bpy.types.Scene.player_object = bpy.props.PointerProperty(type=bpy.types.Object, name="Player Object", description="Player Object", poll=scene_player_object_poll)
    bpy.types.Scene.camera_fov = bpy.props.FloatProperty(name="FOV", default=30.0, min=1.0, max=180.0)
    bpy.types.Scene.player_animation_sel = bpy.props.IntProperty(name="Player Selected Animation", default=0)

    bpy.types.Scene.controls_settings_type = bpy.props.EnumProperty(
        items = ControlSettingsType.control_settings_type_options,
        name = "Control Settings Type",
        description = "Control Settings Type",
        default = "keyboard",
        update=controls_update
    )

    bpy.types.Scene.controls_settings = bpy.props.CollectionProperty(type=ControlsProperties)
    bpy.types.Scene.controls_settings_sel = bpy.props.IntProperty(name="Input Selected", default=0)

def register():
    bpy.utils.register_class(ControlsProperties)
    init_properties()
    bpy.utils.register_class(CONTROLS_UL_player_input)
    bpy.utils.register_class(ANIMATIONS_UL_armature_animations)
    bpy.utils.register_class(SCENE_OT_get_input)
    bpy.utils.register_class(PlayerPropertiesPanel)
    #print(bpy.context.preferences.keymap.active_keyconfig)

def unregister():
    bpy.utils.unregister_class(PlayerPropertiesPanel)
    bpy.utils.unregister_class(SCENE_OT_get_input)
    bpy.utils.unregister_class(ANIMATIONS_UL_armature_animations)
    bpy.utils.unregister_class(ControlsProperties)
    bpy.utils.unregister_class(CONTROLS_UL_player_input)


