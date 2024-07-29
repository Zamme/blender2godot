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
import os, json
import bpy
from blender2godot.addon_config import addon_config # type: ignore

'''
def button_scene_object_poll(self, scene):
    return (scene.name != "B2G_GameManager")
'''

def button_scene_object_poll():
    pass

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

def poll_menu3d_scene_buttons(self, _object):
    _valid = False
    for _scene_object in bpy.context.scene.objects:
        if _scene_object is _object:
            if _object.type == "MESH":
                if _object.special_object_info.menu_object_type == "button":
                    _valid = True
                    break
    return _valid

def get_menu3d_input_templates(self, context):
    # Template name must be "<name>_template_menu_controls.json"
    input_templates = [("custom", "Custom", "", "", 0)]
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "input_templates"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "input_templates")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _listdir = os.listdir(p_path)
            for _i,_l in enumerate(_listdir):
                if _l.endswith("menu_controls.json"):
                    _input_name = _l.replace("_template_menu_controls.json", "").replace("_", " ").capitalize() + " Menu Controls"
                    input_templates.append((_l, _input_name, _l, "", _i+1))
            return input_templates
        else:
            pass

def get_scene_parameter_name(self, context):
    _parameter_name = context.active_object.special_object_info.button_action_on_click.removeprefix("load_").capitalize()
    return _parameter_name

def scene_camera_object_poll(self, object):
    return ((object.users_scene[0] == bpy.context.scene) and (object.type == 'CAMERA'))

def update_menu3d_controls_template(self, context):
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "input_templates"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "input_templates")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _filepath = os.path.join(p_path, context.scene.menu3d_controls_template)
            if os.path.isfile(_filepath):
                with open(_filepath, 'r') as outfile:
                    #global current_template_controls
                    current_template_controls = json.load(outfile)
                    context.scene.menu3d_controls_settings.clear()
                    for _key in current_template_controls.keys():
                        _new_setting = context.scene.menu3d_controls_settings.add()
                        _new_setting.motion_name = _key
                        for _ind,_input_type in enumerate(current_template_controls[_key]["DefaultInputsTypes"]):
                            _new_motion_input = _new_setting.motion_inputs.add()
                            _new_motion_input.motion_input_type = _input_type
                            _new_motion_input.motion_input_blender = current_template_controls[_key]["DefaultInputs"][_ind]
                            _bool_pass = ((current_template_controls[_key]["DefaultInputsModifiers"][_ind] == "on_press") or
                                          (current_template_controls[_key]["DefaultInputsModifiers"][_ind] == "on_move") or
                                          (current_template_controls[_key]["DefaultInputsModifiers"][_ind] == "positive"))
                            _new_motion_input.motion_input_modifier = _bool_pass
                break
            else:
                break
    print("Input template selected:", context.scene.menu3d_controls_template)

class Menu3dInputType(bpy.types.PropertyGroup):
    """ Input Type properties """
    input_type_options = [
                        ("keyboard", "Keyboard", "", 0),
                        ("gamepad", "Gamepad", "", 1),
                        ("mouse", "Mouse", "", 2),
                        ("other", "Other", "", 3)]

class Menu3dMotionInputProperties(bpy.types.PropertyGroup):
    motion_input_type : bpy.props.EnumProperty(items=Menu3dInputType.input_type_options) # type: ignore
    motion_input_blender: bpy.props.StringProperty(name="Blender Input", default="None") # type: ignore
    motion_input_modifier: bpy.props.BoolProperty(name="Blender Input Modifier") # type: ignore

class Menu3dControlsProperties(bpy.types.PropertyGroup):
    motion_name: bpy.props.StringProperty(name="Motion Name", default="Unknown") # type: ignore
    motion_inputs: bpy.props.CollectionProperty(type=Menu3dMotionInputProperties, name="Menu Motion Inputs") # type: ignore

class Button3dNavigation(bpy.types.PropertyGroup):
    navigation_up : bpy.props.PointerProperty(type=bpy.types.Object, poll=poll_menu3d_scene_buttons) # type: ignore
    navigation_down : bpy.props.PointerProperty(type=bpy.types.Object, poll=poll_menu3d_scene_buttons) # type: ignore
    navigation_left : bpy.props.PointerProperty(type=bpy.types.Object, poll=poll_menu3d_scene_buttons) # type: ignore
    navigation_right : bpy.props.PointerProperty(type=bpy.types.Object, poll=poll_menu3d_scene_buttons) # type: ignore

class Menu3DSpecialObject(bpy.types.PropertyGroup):
    """ Menu 3D Object Type """
    object_type_options = [
                            ("none", "None", "", 0), 
                            ("button", "Button", "", 1),
                            ("checkbox", "Checkbox", "", 2)
                            ]
    menu_object_type : bpy.props.EnumProperty(items=object_type_options, name="Type") # type: ignore

class SCENE_OT_menu3d_add_control(bpy.types.Operator):
    bl_idname = "scene.add_menu3d_control"
    bl_label = "Add"
    bl_description = "Add a new control"
    bl_options = {"UNDO", "REGISTER"}

    current_input_item_index : bpy.props.IntProperty(name="Control Property Index") # type: ignore
    motion_input_index : bpy.props.IntProperty(name="Motion Index") # type: ignore
    control_type : bpy.props.EnumProperty(items=Menu3dInputType.input_type_options, default=0) # type: ignore

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

class SCENE_OT_menu3d_del_control(bpy.types.Operator):
    bl_idname = "scene.del_menu3d_control"
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

class SCENE_OT_menu3d_add_gamepad_input(bpy.types.Operator):
    bl_idname = "scene.add_menu3d_gamepad_input"
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

class SCENE_OT_menu3d_add_mouse_input(bpy.types.Operator):
    bl_idname = "scene.add_menu3d_mouse_input"
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

class CONTROLS_UL_menu3d_input(bpy.types.UIList):
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
        row3 = box1.row()
        row3.prop(context.scene, "menu3d_default_button_selected", text="Default Button Selected")
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
                    box6 = box3.box()
                    row14 = box6.row()
                    row14.label(text="Navigation:")
                    row15 = box6.row()
                    row15.label(text="", icon="TRIA_UP")
                    row15.prop(context.active_object.menu3d_button_navigation_properties, "navigation_up", text="GO UP")
                    row16 = box6.row()
                    row16.label(text="", icon="TRIA_DOWN")
                    row16.prop(context.active_object.menu3d_button_navigation_properties, "navigation_down", text="GO DOWN")
                    row17 = box6.row()
                    row17.label(text="", icon="TRIA_LEFT")
                    row17.prop(context.active_object.menu3d_button_navigation_properties, "navigation_left", text="GO LEFT")
                    row18 = box6.row()
                    row18.label(text="", icon="TRIA_RIGHT")
                    row18.prop(context.active_object.menu3d_button_navigation_properties, "navigation_right", text="GO RIGHT")

            box3.prop(context.active_object, "godot_exportable")
                 
class Menu3DManagementPanel(bpy.types.Panel):
    """Menu 3D Controls Panel"""
    bl_label = "Menu 3D Controls"
    bl_idname = "MENU3DMANAGEMENT_PT_layout"
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

        # MENU PROPERTIES BOX
        row13 = layout.row()
        box6 = row13.box()
        box6.label(text="Menu Controls")
        box6.prop(scene, "menu3d_controls_template", text="Template")
        box6.template_list("CONTROLS_UL_menu3d_input", "Menu3dControlsList", context.scene, "menu3d_controls_settings", scene, "menu3d_controls_settings_sel")



def init_properties():
    bpy.types.Scene.menu_camera_object = bpy.props.PointerProperty(type=bpy.types.Object, name="Menu Camera", poll=scene_camera_object_poll)
    bpy.types.Object.special_object_info = bpy.props.PointerProperty(type=Menu3DSpecialObject)
    bpy.types.Object.menu3d_button_navigation_properties = bpy.props.PointerProperty(type=Button3dNavigation)
    bpy.types.Scene.menu3d_controls_template = bpy.props.EnumProperty(items=get_menu3d_input_templates, default=0, update=update_menu3d_controls_template)
    bpy.types.Scene.menu3d_controls_settings = bpy.props.CollectionProperty(type=Menu3dControlsProperties)
    bpy.types.Scene.menu3d_controls_settings_sel = bpy.props.IntProperty(name="Input Selected", default=0)
    bpy.types.Scene.menu3d_default_button_selected = bpy.props.PointerProperty(type=bpy.types.Object, poll=poll_menu3d_scene_buttons)

def clear_properties():
    del bpy.types.Scene.menu_camera_object
    del bpy.types.Object.special_object_info
    del bpy.types.Object.menu3d_button_navigation_properties
    del bpy.types.Scene.menu3d_controls_template
    del bpy.types.Scene.menu3d_controls_settings
    del bpy.types.Scene.menu3d_controls_settings_sel
    del bpy.types.Scene.menu3d_default_button_selected

def register():
    bpy.utils.register_class(Menu3DSpecialObject)
    bpy.utils.register_class(Menu3dInputType)
    bpy.utils.register_class(Menu3dMotionInputProperties)
    bpy.utils.register_class(Menu3dControlsProperties)
    bpy.utils.register_class(Button3dNavigation)
    bpy.utils.register_class(CONTROLS_UL_menu3d_input)
    init_properties()
    bpy.utils.register_class(Menu3DPropertiesPanel)
    bpy.utils.register_class(Menu3DManagementPanel)

def unregister():
    bpy.utils.unregister_class(Menu3DPropertiesPanel)
    clear_properties()
    bpy.utils.unregister_class(CONTROLS_UL_menu3d_input)
    bpy.utils.unregister_class(Button3dNavigation)
    bpy.utils.unregister_class(Menu3dControlsProperties)
    bpy.utils.unregister_class(Menu3dMotionInputProperties)
    bpy.utils.unregister_class(Menu3dInputType)
    bpy.utils.unregister_class(Menu3DSpecialObject)


