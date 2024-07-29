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
For menus 2D
"""

import os, math, json
import bpy
from blender2godot.addon_config import addon_config # type: ignore

'''
shape_options = [("square", "Square", "Square shape", addon_config.preview_collections[0]["square_icon"].icon_id, 0),
                ("round", "Round", "Round shape", addon_config.preview_collections[0]["round_icon"].icon_id, 1),
                ("triangle", "Triangle", "Triangle shape", addon_config.preview_collections[0]["triangle_icon"].icon_id, 2)
                ]
'''
shape_options = [("square", "Square", "Square shape", "", 0),
                ("round", "Round", "Round shape", "", 1),
                ("triangle", "Triangle", "Triangle shape", "", 2)
                ]
#'''

def get_action_scenes(self, context):
    _scenes = [("none", "None", "", "NONE", 0)]
    _index = 1
    for _sc in bpy.data.scenes:
        if hasattr(context.active_object, "menu2d_object_properties"):
            if _sc.scene_type == context.active_object.menu2d_object_properties.button_action.removeprefix("load_"):
                if _sc.scene_exportable:
                    _scenes.append((_sc.name, _sc.name, "", "", _index))
                    _index += 1
    return _scenes

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

def get_menu2d_input_templates(self, context):
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

def get_menu2d_scene_buttons(self, context):
    _buttons = [("none", "None", "", "", 0)]
    return _buttons

def poll_menu2d_scene_buttons(self, _object):
    _valid = False
    for _scene_object in bpy.context.scene.objects:
        if _scene_object is _object:
            if _object.type == "GPENCIL":
                if _object.menu2d_object_properties.menu2d_object_type == "button":
                    _valid = True
                    break
    return _valid

def get_scene_parameter_name(self, context):
    _parameter_name = ""
    if hasattr(context.active_object, "menu2d_object_properties"):
        _parameter_name = context.active_object.menu2d_object_properties.button_action.removeprefix("load_").capitalize()
    return _parameter_name

def has_text_child(self, context):
    _has_text = False
    for _child in context.active_object.children:
        if _child.type == "FONT":
            _has_text = True
            break
    return _has_text

def on_depth_update(self, context):
    context.active_object.location.z = float(self.object_depth)

def update_action_parameter(self, context):
    context.active_object.menu2d_object_properties.action_parameter = context.active_object.menu2d_object_properties.scene_parameter

def update_menu2d_controls_template(self, context):
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "input_templates"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "input_templates")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _filepath = os.path.join(p_path, context.scene.menu2d_controls_template)
            if os.path.isfile(_filepath):
                with open(_filepath, 'r') as outfile:
                    #global current_template_controls
                    current_template_controls = json.load(outfile)
                    context.scene.menu2d_controls_settings.clear()
                    for _key in current_template_controls.keys():
                        _new_setting = context.scene.menu2d_controls_settings.add()
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
    print("Input template selected:", context.scene.menu2d_controls_template)

class Menu2dInputType(bpy.types.PropertyGroup):
    """ Input Type properties """
    input_type_options = [
                        ("keyboard", "Keyboard", "", 0),
                        ("gamepad", "Gamepad", "", 1),
                        ("mouse", "Mouse", "", 2),
                        ("other", "Other", "", 3)]

class Menu2dMotionInputProperties(bpy.types.PropertyGroup):
    motion_input_type : bpy.props.EnumProperty(items=Menu2dInputType.input_type_options) # type: ignore
    motion_input_blender: bpy.props.StringProperty(name="Blender Input", default="None") # type: ignore
    motion_input_modifier: bpy.props.BoolProperty(name="Blender Input Modifier") # type: ignore

class Menu2dControlsProperties(bpy.types.PropertyGroup):
    motion_name: bpy.props.StringProperty(name="Motion Name", default="Unknown") # type: ignore
    motion_inputs: bpy.props.CollectionProperty(type=Menu2dMotionInputProperties, name="Menu Motion Inputs") # type: ignore

class Menu2DSpecialObject(bpy.types.PropertyGroup):
    """ Menu 2D Object Type """
    object_type_options = [
                            ("none", "None", "", 0), 
                            ("button", "Button", "", 1),
                            ("button_content", "Button Content", "", 2),
                            #("checkbox", "Checkbox", "", 2)
                            ]
    menu2d_object_type : bpy.props.EnumProperty(items=object_type_options, name="Type") # type: ignore
    object_depth : bpy.props.IntProperty(name="Object Depth", default=0, update=on_depth_update) # type: ignore

class Button2dNavigation(bpy.types.PropertyGroup):
    navigation_up : bpy.props.PointerProperty(type=bpy.types.Object, poll=poll_menu2d_scene_buttons) # type: ignore
    navigation_down : bpy.props.PointerProperty(type=bpy.types.Object, poll=poll_menu2d_scene_buttons) # type: ignore
    navigation_left : bpy.props.PointerProperty(type=bpy.types.Object, poll=poll_menu2d_scene_buttons) # type: ignore
    navigation_right : bpy.props.PointerProperty(type=bpy.types.Object, poll=poll_menu2d_scene_buttons) # type: ignore

class Button2dProperties(bpy.types.PropertyGroup):
    button_name : bpy.props.StringProperty(name="New button name", default="NewButton") # type: ignore
    button_border_color : bpy.props.FloatVectorProperty(name="Button Border Color", size=4, subtype="COLOR") # type: ignore
    button_fill_color : bpy.props.FloatVectorProperty(name="Button Fill Color", size=4, subtype="COLOR") # type: ignore
    button_shape : bpy.props.EnumProperty(items=shape_options, name="Button shape") # type: ignore
    radius_parameter : bpy.props.FloatProperty(name="Button Radius", min=1.0, max=10.0, default=3.0) # type: ignore
    segments_parameter : bpy.props.IntProperty(name="Button Segments", min=8, max=64, default=12) # type: ignore
    width_parameter : bpy.props.FloatProperty(name="Button Width", min=2.0, max=10.0, default=3.0) # type: ignore
    height_parameter : bpy.props.FloatProperty(name="Button Height", min=2.0, max=10.0, default=3.0) # type: ignore

class SCENE_OT_menu2d_add_control(bpy.types.Operator):
    bl_idname = "scene.add_menu2d_control"
    bl_label = "Add"
    bl_description = "Add a new control"
    bl_options = {"UNDO", "REGISTER"}

    current_input_item_index : bpy.props.IntProperty(name="Control Property Index") # type: ignore
    motion_input_index : bpy.props.IntProperty(name="Motion Index") # type: ignore
    control_type : bpy.props.EnumProperty(items=Menu2dInputType.input_type_options, default=0) # type: ignore

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

class SCENE_OT_menu2d_del_control(bpy.types.Operator):
    bl_idname = "scene.del_menu2d_control"
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

class SCENE_OT_menu2d_add_gamepad_input(bpy.types.Operator):
    bl_idname = "scene.add_menu2d_gamepad_input"
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

class SCENE_OT_menu2d_add_mouse_input(bpy.types.Operator):
    bl_idname = "scene.add_menu2d_mouse_input"
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

class CONTROLS_UL_menu2d_input(bpy.types.UIList):
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
                        _ops1 = row1.operator("scene.del_menu2d_control", text="", icon="CANCEL")
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
                        _ops = row1.operator("scene.add_menu2d_gamepad_input", text=_but_text, icon_value=addon_config.preview_collections[0]["gamepad_icon"].icon_id)
                        _ops1 = row1.operator("scene.del_menu2d_control", text="", icon="CANCEL")
                    case "mouse":
                        _ops = row1.operator("scene.add_menu2d_mouse_input", text=_input_motion.motion_input_blender, icon_value=addon_config.preview_collections[0]["mouse_icon"].icon_id)
                        _ops1 = row1.operator("scene.del_menu2d_control", text="", icon="CANCEL")
                    case "other":
                        row1.label(text="Other entry")
                        _ops1 = row1.operator("scene.del_menu2d_control", text="", icon="CANCEL")
                if _ops:
                    _ops.current_input_item_index = index
                    _ops.motion_input_index = i_enum
                if _ops1:
                    _ops1.current_input_item_index = index
                    _ops1.motion_input_index = i_enum
                if _ops2:
                    _ops2.current_input_item_index = index
                    _ops2.motion_input_index = i_enum
            box0.operator("scene.add_menu2d_control", text="Add", icon="PLUS").current_input_item_index=index
            box0.separator()
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = "POSE_HLT")

class CreateMenu2dButtonTextOperator(bpy.types.Operator):
    bl_idname = "scene.create_menu2d_button_text_operator"
    bl_label = "Create Menu 2D Button Text"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _last_active = context.active_object
        bpy.ops.object.text_add()
        _text_object = context.active_object
        context.active_object.parent = _last_active
        context.active_object.name = context.active_object.parent.name + "_Text"
        _text_object.delta_location = (0.0,0.0,1.0)
        _text_object.data.align_x = "CENTER"
        _text_object.data.align_y = "CENTER"
        bpy.context.view_layer.objects.active = _last_active
        return {'FINISHED'}

class CreateMenu2dBaseButtonOperator(bpy.types.Operator):
    bl_idname = "scene.create_menu2d_base_button_operator"
    bl_label = "Create Menu 2D Base Button"
    bl_options = {'REGISTER', 'UNDO'}

    new_button_props : bpy.props.PointerProperty(type=Button2dProperties) # type: ignore

    def draw(self, context):
        layout = self.layout
        row0 = layout.row()
        box0 = row0.box()
        row1 = box0.row()
        box1 = row1.box()
        row2 = box1.row()
        row2.prop(self.new_button_props, "button_name", text="Name")
        #row3 = box1.row()
        #row3.prop(self.new_button_props, "button_border_color")
        #row4 = box1.row()
        #row4.prop(self.new_button_props, "button_fill_color")
        row5 = box1.row()
        row5.prop_tabs_enum(self.new_button_props, "button_shape")
        box2 = box1.box()
        row6 = box2.row()
        match self.new_button_props.button_shape:
            case "square":
                row6.prop(self.new_button_props, "width_parameter")
                row7 = box2.row()
                row7.prop(self.new_button_props, "height_parameter")
            case "round":
                row6.prop(self.new_button_props, "radius_parameter")
                row7 = box2.row()
                row7.prop(self.new_button_props, "segments_parameter")
            case "triangle":
                row6.prop(self.new_button_props, "width_parameter")
                row7 = box2.row()
                row7.prop(self.new_button_props, "height_parameter")
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        print("Creating menu 2d base button...")
        bpy.ops.object.gpencil_add(type="EMPTY")
        context.active_object.name = self.new_button_props.button_name
        context.active_object.data.name = context.active_object.name
        gp_name = bpy.context.object.name
        gp = bpy.data.grease_pencils[gp_name]
        # Reference grease pencil layer or create one of none exists
        if gp.layers:
            gpl = gp.layers[0]
        else:
            gpl = gp.layers.new('gpl', set_active = True )
        # Reference active GP frame or create one of none exists    
        if gpl.frames:
            fr = gpl.active_frame
        else:
            fr = gpl.frames.new(1) 
        # Create a new stroke
        str = fr.strokes.new()
        str.display_mode = '3DSPACE'
        # Add points
        match self.new_button_props.button_shape:
            case "square":
                str.points.add(count = 4)
                points = str.points
                _width = self.new_button_props.width_parameter/2.0
                _height = self.new_button_props.height_parameter/2.0
                points[0].co = (-_width,-_height,0.0)
                points[1].co = (_width,-_height,0.0)
                points[2].co = (_width,_height,0.0)
                points[3].co = (-_width,_height,0.0)
            case "round":
                segments = self.new_button_props.segments_parameter
                r = self.new_button_props.radius_parameter
                str.points.add(count = segments)
                points = str.points
                for ii in range(segments):
                    theta = 2.0 * 3.1415926 * float(ii) / float(segments)
                    x = r * math.cos(theta) 
                    y = r * math.sin(theta)
                    points[ii].co = (x, y, 0.0)
            case "triangle":
                _width = self.new_button_props.width_parameter/2.0
                _height = self.new_button_props.height_parameter/2.0
                str.points.add(count = 3 )
                points = str.points
                points[0].co = (0.0,-_height, 0.0)
                points[1].co = (_width, _height, 0.0)
                points[2].co = (-_width,_height,0.0)
        str.use_cyclic = True
        gpl.line_change = 50
        bpy.context.object.active_material.grease_pencil.color = self.new_button_props.button_border_color
        bpy.context.object.active_material.grease_pencil.show_fill = True
        bpy.context.object.active_material.grease_pencil.fill_color = self.new_button_props.button_fill_color
        bpy.context.object.menu2d_object_properties.menu2d_object_type = "button"

        return {'FINISHED'}
    
class CreateMenu2dViewOperator(bpy.types.Operator):
    bl_idname = "scene.create_menu2d_view_operator"
    bl_label = "Create Menu 2D View"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("Creating menu 2d view...")
        bpy.ops.object.camera_add(align="WORLD", location=(0.0, 0.0, 50.0), rotation=(0.0,0.0,0.0))
        bpy.ops.view3d.object_as_camera()
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        return {'FINISHED'}

class Menu2DPropertiesPanel(bpy.types.Panel):
    """Menu 2D Properties Panel"""
    bl_label = "Menu 2D Properties"
    bl_idname = "MENU2DPROPERTIES_PT_layout"
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
                if ((context.scene.scene_type == "2dmenu") and (context.scene.name != context.scene.gamemanager_scene_name)):
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
        row13 = layout.row()
        row9 = layout.row()
        row1 = layout.row()
        row13.prop(context.scene, "menu2d_default_button_selected", text="Default Button Selected")
        # TOOLS BOX
        box2 = row9.box()
        row10 = box2.row()
        row10.label(text="Tools:")
        row8 = box2.row()
        if len(context.scene.objects) < 1:
            row8.operator("scene.create_menu2d_view_operator")
            return
        else:
            row8.operator("scene.create_menu2d_base_button_operator")

        # ACTIVE OBJECT PROPERTIES BOX
        if context.active_object is not None:
            box1 = row1.box()
            row2 = box1.row()
            box3 = row2.box()
            _nl = "Active Object: " + context.active_object.name
            box3.label(text=_nl)
            match context.active_object.type:
                case "GPENCIL":
                    gpl = context.active_object.data.layers[0]
                    box5 = box3.box()
                    row11 = box5.row()
                    row11.prop(context.active_object.menu2d_object_properties, "object_depth")
                    row3 = box5.row()
                    row3.prop(gpl, "line_change", text="Border thickness")
                    row4 = box5.row()
                    row4.prop(context.active_object.active_material.grease_pencil, "color", text="Border color")
                    row6 = box5.row()
                    row6.prop(context.active_object.active_material.grease_pencil, "show_fill", text="Fill")
                    if context.active_object.active_material.grease_pencil.show_fill:
                        row5 = box5.row()
                        row5.prop(context.active_object.active_material.grease_pencil, "fill_color", text="Fill color")
                    if not has_text_child(self, context):
                        row7 = box5.row()
                        row7.operator("scene.create_menu2d_button_text_operator", text="Add text")
                case "FONT":
                    row7 = box3.row()
                    row7.prop(context.active_object.data, "font", text="Font", slider=True)
                    row8 = box3.row()
                    row8.prop(context.active_object.data, "size", text="Font Size")
            box4 = box3.box()
            box4.prop(context.active_object.menu2d_object_properties, "menu2d_object_type")
            if context.active_object.menu2d_object_properties.menu2d_object_type == "button":
                box6 = box3.box()
                row14 = box6.row()
                row14.label(text="Navigation:")
                row15 = box6.row()
                row15.label(text="", icon="TRIA_UP")
                row15.prop(context.active_object.menu2d_button_navigation_properties, "navigation_up", text="GO UP")
                row16 = box6.row()
                row16.label(text="", icon="TRIA_DOWN")
                row16.prop(context.active_object.menu2d_button_navigation_properties, "navigation_down", text="GO DOWN")
                row17 = box6.row()
                row17.label(text="", icon="TRIA_LEFT")
                row17.prop(context.active_object.menu2d_button_navigation_properties, "navigation_left", text="GO LEFT")
                row18 = box6.row()
                row18.label(text="", icon="TRIA_RIGHT")
                row18.prop(context.active_object.menu2d_button_navigation_properties, "navigation_right", text="GO RIGHT")

            ''' DEBUG
            if context.active_object.type == "GPENCIL":
                for _point_index,_point in enumerate(context.active_object.data.layers[0].active_frame.strokes[0].points):
                    if _point.select:
                        _point_text = "Stroke point: " + str(_point_index)
                        box3.label(text=_point_text)
                        box3.prop(_point, "co")
            '''                
            box3.prop(context.active_object, "godot_exportable")
                 
class Menu2DManagementPanel(bpy.types.Panel):
    """Menu 2D Controls Panel"""
    bl_label = "Menu 2D Controls"
    bl_idname = "MENU2DMANAGEMENT_PT_layout"
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
                if ((context.scene.scene_type == "2dmenu") and (context.scene.name != context.scene.gamemanager_scene_name)):
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
        box6.prop(scene, "menu2d_controls_template", text="Template")
        box6.template_list("CONTROLS_UL_menu2d_input", "Menu2dControlsList", context.scene, "menu2d_controls_settings", scene, "menu2d_controls_settings_sel")


def init_properties():
    bpy.types.Object.menu2d_button_navigation_properties = bpy.props.PointerProperty(type=Button2dNavigation)
    bpy.types.Object.menu2d_object_properties = bpy.props.PointerProperty(type=Menu2DSpecialObject)
    bpy.types.Scene.menu2d_controls_template = bpy.props.EnumProperty(items=get_menu2d_input_templates, default=0, update=update_menu2d_controls_template)
    bpy.types.Scene.menu2d_controls_settings = bpy.props.CollectionProperty(type=Menu2dControlsProperties)
    bpy.types.Scene.menu2d_controls_settings_sel = bpy.props.IntProperty(name="Input Selected", default=0)
    bpy.types.Scene.menu2d_default_button_selected = bpy.props.PointerProperty(type=bpy.types.Object, poll=poll_menu2d_scene_buttons)

def clear_properties():
    del bpy.types.Scene.menu2d_controls_template
    del bpy.types.Scene.menu2d_controls_settings
    del bpy.types.Scene.menu2d_controls_settings_sel
    del bpy.types.Object.menu2d_object_properties
    del bpy.types.Object.menu2d_button_navigation_properties

def register():
    bpy.utils.register_class(Button2dNavigation)
    bpy.utils.register_class(Button2dProperties)
    bpy.utils.register_class(Menu2dInputType)
    bpy.utils.register_class(Menu2dMotionInputProperties)
    bpy.utils.register_class(Menu2dControlsProperties)
    bpy.utils.register_class(CreateMenu2dButtonTextOperator)
    bpy.utils.register_class(Menu2DSpecialObject)
    bpy.utils.register_class(CONTROLS_UL_menu2d_input)
    bpy.utils.register_class(SCENE_OT_menu2d_add_control)
    bpy.utils.register_class(SCENE_OT_menu2d_add_gamepad_input)
    bpy.utils.register_class(SCENE_OT_menu2d_add_mouse_input)
    bpy.utils.register_class(SCENE_OT_menu2d_del_control)
    init_properties()
    bpy.utils.register_class(CreateMenu2dViewOperator)
    bpy.utils.register_class(CreateMenu2dBaseButtonOperator)
    bpy.utils.register_class(Menu2DPropertiesPanel)
    bpy.utils.register_class(Menu2DManagementPanel)

def unregister():
    bpy.utils.unregister_class(Menu2DManagementPanel)
    bpy.utils.unregister_class(Menu2DPropertiesPanel)
    bpy.utils.unregister_class(CreateMenu2dBaseButtonOperator)
    bpy.utils.unregister_class(CreateMenu2dViewOperator)
    clear_properties()
    bpy.utils.unregister_class(SCENE_OT_menu2d_add_control)
    bpy.utils.unregister_class(SCENE_OT_menu2d_add_gamepad_input)
    bpy.utils.unregister_class(SCENE_OT_menu2d_add_mouse_input)
    bpy.utils.unregister_class(SCENE_OT_menu2d_del_control)
    bpy.utils.unregister_class(Menu2DSpecialObject)
    bpy.utils.unregister_class(CONTROLS_UL_menu2d_input)
    bpy.utils.unregister_class(CreateMenu2dButtonTextOperator)
    bpy.utils.unregister_class(Menu2dControlsProperties)
    bpy.utils.unregister_class(Menu2dMotionInputProperties)
    bpy.utils.unregister_class(Menu2dInputType)
    bpy.utils.unregister_class(Button2dProperties)
    bpy.utils.unregister_class(Button2dNavigation)



