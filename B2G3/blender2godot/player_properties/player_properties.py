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

import json
import os

import bpy

from blender2godot.addon_config import addon_config # type: ignore


current_template_controls = None


def scene_camera_object_poll(self, object):
    return ((object.users_scene[0] == bpy.context.scene) and (object.type == 'CAMERA'))

def scene_player_object_poll(self, object):
    return ((object.users_scene[0] == bpy.context.scene) and (object.type == 'MESH' or object.type == 'ARMATURE'))

def camera_update(self, context):
    context.scene.scene_exportable = (context.scene.camera_object != None)  

'''
def controls_update(self, context):
    pass
'''

def get_action_template(self, context):
    # Template name must be "<name>_template_actions.json"
    _return = None
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "action_templates"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "action_templates")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _filepath = os.path.join(p_path, context.scene.controls_template.replace("_template_controls.json", "_template_actions.json"))
            if os.path.isfile(_filepath):
                with open(_filepath, 'r') as outfile:
                    _return = json.load(outfile)
                    break
        else:
            pass
    return _return

def get_actions_list_array(self, context):
    _actions_list = None
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "b2g_misc"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "b2g_misc")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _filepath = os.path.join(p_path, "b2g_actions_list.json")
            if os.path.isfile(_filepath):
                with open(_filepath, 'r') as outfile:
                    _actions_list = json.load(outfile)
                    break
            else:
                pass
    _actions_list_array = []
    for _index,_action_key in enumerate(_actions_list.keys()):
        _tuple = (_action_key, _actions_list[_action_key]["ActionName"], _actions_list[_action_key]["ActionDescription"], _index)
        _actions_list_array.append(_tuple)
    #print(_actions_list_array)
    return _actions_list_array

def get_controls_list_array(_control_type):
    _controls_list = None
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "b2g_misc"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "b2g_misc")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _filepath = os.path.join(p_path, "b2g_controls_list.json")
            if os.path.isfile(_filepath):
                with open(_filepath, 'r') as outfile:
                    _controls_list = json.load(outfile)
                    break
            else:
                pass
    _controls_list_array = []
    for _index,_control_key in enumerate(_controls_list[_control_type.capitalize()].keys()):
        _tuple = (_control_key, _control_key, "", _index)
        _controls_list_array.append(_tuple)
    return _controls_list_array

def get_controls_settings(self):
    return self["controls_settings"]

def get_input_templates(self, context):
    # Template name must be "<name>_template_controls.json"
    input_templates = [("custom", "Custom", "", "", 0)]
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "input_templates"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "input_templates")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _listdir = os.listdir(p_path)
            for _i,_l in enumerate(_listdir):
                _input_name = _l.replace("_template_controls.json", "").replace("_", " ").capitalize()
                input_templates.append((_l, _input_name, _l, "", _i+1))
            return input_templates
        else:
            pass

def get_hud_scenes(self, context):
    _hud_scenes = [("none", "None", "", "NONE", 0)]
    _hs_index = 1
    for _sc in bpy.data.scenes:
        if _sc.scene_type == "hud":
            _hud_scenes.append((_sc.name, _sc.name, "", "", _hs_index))
            _hs_index += 1
    return _hud_scenes

'''
def get_template_controls(_control_type):
    current_template_controls = None
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "project_template", bpy.data.scenes["B2G_GameManager"].project_template),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "project_template", bpy.data.scenes["B2G_GameManager"].project_template)]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _filepath = os.path.join(p_path, "fps_template_controls.json")
            if os.path.isfile(_filepath):
                with open(_filepath, 'r') as outfile:
                    current_template_controls = json.load(outfile)
                    break
            else:
                pass
'''

def update_controls_template(self, context):
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "input_templates"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "input_templates")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _filepath = os.path.join(p_path, context.scene.controls_template)
            if os.path.isfile(_filepath):
                with open(_filepath, 'r') as outfile:
                    current_template_controls = json.load(outfile)
                    context.scene.controls_settings.clear()
                    for _key in current_template_controls.keys():
                        _new_setting = context.scene.controls_settings.add()
                        _new_setting.motion_name = _key
                        for _ind,_input_type in enumerate(current_template_controls[_key]["DefaultInputsTypes"]):
                            _new_motion_input = _new_setting.motion_inputs.add()
                            _new_motion_input.motion_input_type = _input_type
                            _new_motion_input.motion_input_blender = current_template_controls[_key]["DefaultInputs"][_ind]
                            _bool_pass = ((current_template_controls[_key]["DefaultInputsModifiers"][_ind] == "on_press") or
                                          (current_template_controls[_key]["DefaultInputsModifiers"][_ind] == "on_move") or
                                          (current_template_controls[_key]["DefaultInputsModifiers"][_ind] == "positive"))
                            _new_motion_input.motion_input_modifier = _bool_pass
                # Update actions
                _actions_template = get_action_template(self,context)
                context.scene.actions_settings.clear()
                if _actions_template is not None:
                    for _key in _actions_template.keys():
                        _new_action = context.scene.actions_settings.add()
                        _new_action.action_id = _key
                        _new_action.action_process = _actions_template[_key]["ProcessID"]
                break
            else:
                break
    print("Input template selected:", context.scene.controls_template)

class GamepadInputType(bpy.types.PropertyGroup):
    """ Gamepad Input Type properties """
    gamepad_input_type_options = [
                        ("axis", "Axis", "", 0),
                        ("button", "Button", "", 1)]

class InputType(bpy.types.PropertyGroup):
    """ Input Type properties """
    input_type_options = [
                        ("keyboard", "Keyboard", "", 0),
                        ("gamepad", "Gamepad", "", 1),
                        ("mouse", "Mouse", "", 2),
                        ("other", "Other", "", 3)]

class MotionInputProperties(bpy.types.PropertyGroup):
    motion_input_type : bpy.props.EnumProperty(items=InputType.input_type_options) # type: ignore
    motion_input_blender: bpy.props.StringProperty(name="Blender Input", default="None") # type: ignore
    motion_input_modifier: bpy.props.BoolProperty(name="Blender Input Modifier") # type: ignore

class ActionsProperties(bpy.types.PropertyGroup):
    action_id : bpy.props.StringProperty(name="Action ID", default="None") # type: ignore
    action_process : bpy.props.EnumProperty(items=get_actions_list_array, name="Action Process") # type: ignore

class ControlsProperties(bpy.types.PropertyGroup):
    motion_name: bpy.props.StringProperty(name="Motion Name", default="Unknown") # type: ignore
    motion_inputs: bpy.props.CollectionProperty(type=MotionInputProperties, name="Motion Inputs") # type: ignore

class SCENE_OT_add_control(bpy.types.Operator):
    bl_idname = "scene.add_control"
    bl_label = "Add"
    bl_description = "Add a new control"
    bl_options = {"UNDO", "REGISTER"}

    current_input_item_index : bpy.props.IntProperty(name="Control Property Index") # type: ignore
    motion_input_index : bpy.props.IntProperty(name="Motion Index") # type: ignore
    control_type : bpy.props.EnumProperty(items=InputType.input_type_options, default=0) # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.prop(self, "control_type", text="Input Type")
    
    def execute(self, context):
        _new_input = context.scene.controls_settings[self.current_input_item_index].motion_inputs.add()
        _new_input.motion_input_type = self.control_type
        context.scene.controls_template = "custom"
        return {"FINISHED"}

class SCENE_OT_del_control(bpy.types.Operator):
    bl_idname = "scene.del_control"
    bl_label = "X"
    bl_description = "Delete control"
    bl_options = {"UNDO", "REGISTER"}

    current_input_item_index : bpy.props.IntProperty(name="Control Property Index") # type: ignore
    motion_input_index : bpy.props.IntProperty(name="Motion Index") # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        _new_input = context.scene.controls_settings[self.current_input_item_index].motion_inputs.remove(self.motion_input_index)
        context.scene.controls_template = "custom"
        return {"FINISHED"}

class SCENE_OT_add_gamepad_input(bpy.types.Operator):
    bl_idname = "scene.add_gamepad_input"
    bl_label = "Add"
    bl_description = "Add a new gamepad input"
    bl_options = {"UNDO", "REGISTER"}

    current_input_item_index : bpy.props.IntProperty(name="Control Property Index") # type: ignore
    motion_input_index : bpy.props.IntProperty(name="Motion Index") # type: ignore
    gamepad_input : bpy.props.EnumProperty(items=get_controls_list_array("gamepad")) # type: ignore
    gamepad_input_modifier : bpy.props.BoolProperty(name="Gamepad Input Positive") # type: ignore
    
    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.prop(self, "gamepad_input", text="Input")
        if self.gamepad_input.find("AXIS") > -1:
            box.prop(self, "gamepad_input_modifier", text="+")
        elif self.gamepad_input.find("BUTTON") > -1:
            box.prop(self, "gamepad_input_modifier", text="release")
        else:
            pass
    
    def execute(self, context):
        context.scene.controls_settings[self.current_input_item_index].motion_inputs[self.motion_input_index].motion_input_blender = self.gamepad_input
        context.scene.controls_settings[self.current_input_item_index].motion_inputs[self.motion_input_index].motion_input_modifier = self.gamepad_input_modifier
        context.scene.controls_template = "custom"
        return {"FINISHED"}

class SCENE_OT_add_mouse_input(bpy.types.Operator):
    bl_idname = "scene.add_mouse_input"
    bl_label = "Add"
    bl_description = "Add a new mouse input"
    bl_options = {"UNDO", "REGISTER"}

    current_input_item_index : bpy.props.IntProperty(name="Control Property Index") # type: ignore
    motion_input_index : bpy.props.IntProperty(name="Motion Index") # type: ignore
    mouse_input : bpy.props.EnumProperty(items=get_controls_list_array("mouse")) # type: ignore

    @classmethod
    def poll(cls, context):
        return True

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        box = layout.box()
        box.prop(self, "mouse_input", text="Mouse Input", expand=True)
    
    def execute(self, context):
        context.scene.controls_settings[self.current_input_item_index].motion_inputs[self.motion_input_index].motion_input_blender = self.mouse_input
        context.scene.controls_template = "custom"
        return {"FINISHED"}

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

class ACTIONS_UL_player_actions(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row0 = layout.row(align=True)
            box0 = row0.box()
            _action_name_modified = item.action_id.capitalize()
            box0.label(text=_action_name_modified, icon="POSE_HLT")
            box0.label(text=item.action_process)
            #_prop = "actions_settings[" + str(index) + "]"
            #box0.prop(context.scene, "actions_settings")
            #box0.props_enum(context.scene, "action_settings[0]")
            box0.alignment = "EXPAND"
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = "POSE_HLT")

class CONTROLS_UL_player_input(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            row0 = layout.row(align=True)
            box0 = row0.box()
            _motion_name_modified = item.motion_name.replace("b2g_", "").replace("_", " ").capitalize()
            box0.label(text=_motion_name_modified, icon="POSE_HLT")
            box0.alignment = "EXPAND"
            for i_enum,_input_motion in enumerate(item.motion_inputs):
                box1 = box0.box()
                box1.alignment = "EXPAND"
                row1 = box1.row(align=True)
                _ops = None
                _ops1 = None
                _ops2 = None
                match _input_motion.motion_input_type:
                    case "keyboard":
                        _but_text = _input_motion.motion_input_blender
                        if _input_motion.motion_input_modifier:
                            _but_text += " (On release)"
                        else:
                            _but_text += " (On press)"
                        _ops = row1.operator("scene.process_input", text=_but_text, icon_value=addon_config.preview_collections[0]["keyboard_icon"].icon_id)
                        _ops1 = row1.operator("scene.del_control", text="", icon="CANCEL")
                    case "gamepad":
                        _but_text = _input_motion.motion_input_blender
                        if "AXIS" in _but_text:
                            if _input_motion.motion_input_modifier:
                                _but_text += " (+ Axis)"
                            else:
                                _but_text += " (- Axis)"
                        else:
                            if _input_motion.motion_input_modifier:
                                _but_text += " (On release)"
                            else:
                                _but_text += " (On press)"
                        _ops = row1.operator("scene.add_gamepad_input", text=_but_text, icon_value=addon_config.preview_collections[0]["gamepad_icon"].icon_id)
                        _ops1 = row1.operator("scene.del_control", text="", icon="CANCEL")
                    case "mouse":
                        _ops = row1.operator("scene.add_mouse_input", text=_input_motion.motion_input_blender, icon_value=addon_config.preview_collections[0]["mouse_icon"].icon_id)
                        _ops1 = row1.operator("scene.del_control", text="", icon="CANCEL")
                    case "other":
                        row1.label(text="Other entry")
                        _ops1 = row1.operator("scene.del_control", text="", icon="CANCEL")
                if _ops:
                    _ops.current_input_item_index = index
                    _ops.motion_input_index = i_enum
                if _ops1:
                    _ops1.current_input_item_index = index
                    _ops1.motion_input_index = i_enum
                if _ops2:
                    _ops2.current_input_item_index = index
                    _ops2.motion_input_index = i_enum
            box0.operator("scene.add_control", text="Add", icon="PLUS").current_input_item_index=index
            box0.separator()
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = "POSE_HLT")


'''
class ControlSettingsType(bpy.types.PropertyGroup):
    """ Control settings type """
    control_settings_type_options = [
        ("keyboard", "Keyboard", "", 0),
        ("gamepad", "Gamepad", "", 1),
        ("mouse", "Mouse", "", 2),
        ("other", "Other", "", 3)]
'''

class SCENE_OT_get_input(bpy.types.Operator):
    """Get input key."""
    bl_idname = 'scene.process_input'
    bl_label = 'Edit'
    bl_options = {'REGISTER'}

    current_input_item_index : bpy.props.IntProperty(name="Control Index") # type: ignore
    motion_input_index : bpy.props.IntProperty(name="Motion Index") # type: ignore
    last_touched = None

    def modal(self, context, event):
        if event.type == 'ESC':
            context.scene.controls_settings[self.current_input_item_index].motion_inputs[self.motion_input_index].motion_input_blender = self.last_touched
            return {'FINISHED'}
        elif event.value == "PRESS":
            context.scene.controls_settings[self.current_input_item_index].motion_inputs[self.motion_input_index].motion_input_blender = event.type
            context.scene.controls_template = "custom"
            return {'FINISHED'}

        return {'PASS_THROUGH'}

    def invoke(self, context, event):
        self.last_touched = context.scene.controls_settings[self.current_input_item_index].motion_inputs[self.motion_input_index].motion_input_blender
        context.scene.controls_settings[self.current_input_item_index].motion_inputs[self.motion_input_index].motion_input_blender = "Press..."
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class PlayerActionsPanel(bpy.types.Panel):
    """Player Actions Panel"""
    bl_label = "Player Actions"
    bl_idname = "PLAYERACTIONS_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 6
    
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

        # Player actions
        row1 = layout.row(align=True)
        box1 = row1.box()
        box1.alignment = "EXPAND"
        box1.label(text="Actions")
        box2 = box1.box()
        box2.template_list("ACTIONS_UL_player_actions", "PlayerActionsList", context.scene, "actions_settings", scene, "actions_settings_sel")


class PlayerAnimationsPanel(bpy.types.Panel):
    """Player Animations Panel"""
    bl_label = "Player Animations"
    bl_idname = "PLAYERANIMATIONS_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 5
    
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

        # Player animations
        box2 = layout.box()
        box2.label(text="Animations")
        if scene.player_object == None:
            box2.label(text="No player object assigned", icon="ERROR")
        else:
            if scene.player_object.type != "ARMATURE":
                _mess = "No armature in player object."
                _ic = "ERROR"
                box2.label(text=_mess, icon=_ic)
            else:
                _mess = "Player armature : " + scene.player_object.name
                _ic = "OUTLINER_OB_ARMATURE"
                box2.template_list("ANIMATIONS_UL_armature_animations", "PlayerAnimationsList", bpy.data, "actions", scene, "player_animation_sel")
                box2.label(text=_mess, icon=_ic)


class PlayerControlsPanel(bpy.types.Panel):
    """Player Controls Panel"""
    bl_label = "Player Controls"
    bl_idname = "PLAYERCONTROLS_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 4
    
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

        box1 = layout.box()
        box1.label(text="Player Controls")
        box1.prop(scene, "controls_template", text="Template")
        box1.template_list("CONTROLS_UL_player_input", "PlayerControlsList", context.scene, "controls_settings", scene, "controls_settings_sel")

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
        row1 = layout.row()
        box1 = row1.box()
        box1.prop(scene, "player_object")

        if not scene.player_object:
            return

        box3 = box1.box()
        box3.prop(scene, "player_gravity_on")
        box3.prop(scene, "camera_control_inverted")

        # Player camera
        box5 = box1.box()
        box5.label(text="Camera Properties")
        box5.prop(scene, "camera_object")
        if scene.camera_object == None:
            box5.label(text="No camera object assigned", icon="ERROR")
        else:
            box5.prop(scene.camera_object.data, "angle")

        # Player HUD
        box6 = box1.box()
        box6.label(text="Player HUD")
        box6.prop(scene, "player_hud_scene", text="HUD scene")


def clear_properties():
    del bpy.types.Action.animation_type
    del bpy.types.Scene.player_gravity_on
    del bpy.types.Scene.camera_control_inverted
    del bpy.types.Scene.camera_object
    del bpy.types.Scene.player_object
    del bpy.types.Scene.player_animation_sel
    del bpy.types.Scene.actions_settings
    del bpy.types.Scene.actions_settings_sel

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
    bpy.types.Scene.player_animation_sel = bpy.props.IntProperty(name="Player Selected Animation", default=0)
    bpy.types.Scene.player_hud_scene = bpy.props.EnumProperty(items=get_hud_scenes)

    bpy.types.Scene.controls_template = bpy.props.EnumProperty(items=get_input_templates, default=0, update=update_controls_template)
    bpy.types.Scene.controls_settings = bpy.props.CollectionProperty(type=ControlsProperties)
    bpy.types.Scene.controls_settings_sel = bpy.props.IntProperty(name="Input Selected", default=0)

    bpy.types.Scene.actions_settings = bpy.props.CollectionProperty(type=ActionsProperties)
    bpy.types.Scene.actions_settings_sel = bpy.props.IntProperty(name="Action Selected", default=0)

def register():
    #bpy.utils.register_class(ControlSettingsType)
    bpy.utils.register_class(InputType)
    bpy.utils.register_class(GamepadInputType)
    bpy.utils.register_class(SCENE_OT_add_control)
    bpy.utils.register_class(SCENE_OT_del_control)
    bpy.utils.register_class(MotionInputProperties)
    bpy.utils.register_class(ControlsProperties)
    bpy.utils.register_class(ActionsProperties)
    init_properties()
    bpy.utils.register_class(ACTIONS_UL_player_actions)
    bpy.utils.register_class(CONTROLS_UL_player_input)
    bpy.utils.register_class(ANIMATIONS_UL_armature_animations)
    bpy.utils.register_class(SCENE_OT_get_input)
    bpy.utils.register_class(SCENE_OT_add_gamepad_input)
    bpy.utils.register_class(SCENE_OT_add_mouse_input)
    bpy.utils.register_class(PlayerActionsPanel)
    bpy.utils.register_class(PlayerAnimationsPanel)
    bpy.utils.register_class(PlayerControlsPanel)
    bpy.utils.register_class(PlayerPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(PlayerPropertiesPanel)
    bpy.utils.unregister_class(PlayerControlsPanel)
    bpy.utils.unregister_class(PlayerAnimationsPanel)
    bpy.utils.unregister_class(PlayerActionsPanel)
    bpy.utils.unregister_class(SCENE_OT_add_mouse_input)
    bpy.utils.unregister_class(SCENE_OT_add_gamepad_input)
    bpy.utils.unregister_class(SCENE_OT_get_input)
    bpy.utils.unregister_class(ANIMATIONS_UL_armature_animations)
    bpy.utils.unregister_class(CONTROLS_UL_player_input)
    bpy.utils.unregister_class(ControlsProperties)
    bpy.utils.unregister_class(ACTIONS_UL_player_actions)
    bpy.utils.unregister_class(MotionInputProperties)
    bpy.utils.unregister_class(SCENE_OT_add_control)
    bpy.utils.unregister_class(SCENE_OT_del_control)
    bpy.utils.unregister_class(InputType)
    bpy.utils.unregister_class(GamepadInputType)
    bpy.utils.unregister_class(ActionsProperties)
    clear_properties()

