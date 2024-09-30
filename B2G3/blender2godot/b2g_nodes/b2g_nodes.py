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
For B2G Nodes
"""

import os, json
import bpy
from bpy.types import Context, NodeTree, Node, NodeSocket, NodeSocketFloat, NodeSocketInt, NodeSocketString, NodeSocketBool, NodeSocketInterface, bpy_prop_array
from blender2godot.stage_properties import stage_properties # type: ignore
from blender2godot.addon_config import addon_config # type: ignore


animation_operations = [
        ("none", "None", "NONE"),
        ("play_forward", "Play Forward", "PLAY_FORWARD"),
        ("play_backward", "Play Backward", "PLAY_BACKWARD"),
]

execution_behaviors = [
    ("once", "Once", "ONCE"),
    ("always", "Always", "ALWAYS"),
]

string_operations = [
        ("none", "None", "NONE"),
        ("concat", "Concat", "CONCAT"),
    ]

math_operations = [
        ("none", "None", "NONE"),
        ("add", "Add", "ADD"),
        ("sub", "Sub", "SUB"),
        ("mul", "Mul", "MUL"),
        ("div", "Div", "DIV"),
    ]

bool_operations = [
        ("none", "None", "NONE"),
        ("or", "OR", "OR"),
    ]

menu_button_action_type_options = [("none", "None", "", 0), 
                        ("load_stage", "Load Stage", "", 1),
                        ("load_2dmenu", "Load Menu 2D", "", 2),
                        ("load_3dmenu", "Load Menu 3D", "", 3),
                        ("quit_game", "Quit Game", "", 4)
                        ]

overlay_button_action_type_options = [("none", "None", "", 0), 
                        ("close_overlay", "Close Overlay", "", 5),
                        ("load_stage", "Load Stage", "", 1),
                        ("load_2dmenu", "Load Menu 2D", "", 2),
                        ("load_3dmenu", "Load Menu 3D", "", 3),
                        ("quit_game", "Quit Game", "", 4),
                        ]

property_node_sockets = {
    "boolean" : "B2G_Boolean_SocketType",
    "string" : "B2G_String_SocketType",
    "integer" : "B2G_Integer_SocketType",
    "float" : "B2G_Float_SocketType"
}

trigger_conditions = [
    ("on_enter", "OnEnter", "", 0),
    ("on_stay", "OnStay", "", 1),
    ("on_exit", "OnExit", "", 2),
]

scene_node_sockets = {
    "load_stage" : "B2G_Stage_SocketType",
    "load_2dmenu" : "B2G_2dmenu_SocketType",
    "load_3dmenu" : "B2G_3dmenu_SocketType",
}

'''
def get_action_template(self, context, _player_scene):
    # Template name must be "<name>_template_actions.json"
    _return = None
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "action_templates"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "action_templates")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _filepath = os.path.join(p_path, _player_scene.controls_template.replace("_template_controls.json", "_template_actions.json"))
            if os.path.isfile(_filepath):
                with open(_filepath, 'r') as outfile:
                    _return = json.load(outfile)
                    break
        else:
            pass
    return _return
'''

def get_action_scenes(self, context):
    _sc_names_purged = [("none", "None", "", "", 0)]
    _sc_ind = 1
    for _sc in bpy.data.scenes:
        if hasattr(context.active_object, "special_object_info"):
            if _sc.scene_type == context.active_object.special_object_info.button_action_on_click.removeprefix("load_"):
                if _sc.scene_exportable:
                    _sc_names_purged.append((_sc.name, _sc.name, "", "", _sc_ind))
                    _sc_ind += 1
    return _sc_names_purged

def get_actions_list_array(self, context):
    _actions_list = None
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "b2g_misc"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "b2g_misc")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _filepath = os.path.join(p_path, "b2g_game_actions_list.json")
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

def get_controls_template(self, context, _player_scene):
    current_template_controls = None
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "input_templates"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "input_templates")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _filepath = os.path.join(p_path, _player_scene.controls_template)
            if os.path.isfile(_filepath):
                with open(_filepath, 'r') as outfile:
                    current_template_controls = json.load(outfile)
    return current_template_controls

def player_spawns_poll(self, _object):
    _node_scene = bpy.data.scenes[self.node_properties.source_scene_name]
    return ((_node_scene.objects.find(_object.name) > -1) and ((_object.type == 'EMPTY')))

def update_action_parameter(self, context):
    context.active_object.special_object_info.action_parameter = context.active_object.special_object_info.scene_parameter

def on_button_action_update(self, context):
    #print("Update button action click", self.button_node_name)
    bpy.data.node_groups["GameManager"].nodes[self.button_node_name].update()

class ActionProperty(bpy.types.PropertyGroup):
    action_id : bpy.props.StringProperty(name="Action ID", default="None") # type: ignore
    action_process : bpy.props.EnumProperty(items=get_actions_list_array, name="Action Process") # type: ignore

class ButtonAction(bpy.types.PropertyGroup):
    button_node_name : bpy.props.StringProperty(name="Button Node") # type: ignore
    button_name : bpy.props.StringProperty(name="Button Name") # type: ignore
    button_action_on_click : bpy.props.EnumProperty(items=menu_button_action_type_options, name="Action On Click", update=on_button_action_update) # type: ignore
    action_parameter : bpy.props.StringProperty(name="Action Parameter", default="") # type: ignore
    scene_parameter : bpy.props.EnumProperty(items=get_action_scenes, name="Scene Parameter", default=0, update=update_action_parameter) # type: ignore

class OverlayButtonAction(bpy.types.PropertyGroup):
    button_node_name : bpy.props.StringProperty(name="Button Node") # type: ignore
    button_name : bpy.props.StringProperty(name="Button Name") # type: ignore
    button_action_on_click : bpy.props.EnumProperty(items=overlay_button_action_type_options, name="Action On Click", update=on_button_action_update) # type: ignore
    action_parameter : bpy.props.StringProperty(name="Action Parameter", default="") # type: ignore
    scene_parameter : bpy.props.EnumProperty(items=get_action_scenes, name="Scene Parameter", default=0, update=update_action_parameter) # type: ignore

'''
class HudSettings(bpy.types.PropertyGroup):
    visibility_type : bpy.props.EnumProperty(items=[
                                    ("always", "Always", "ALWAYS", "", 0),
                                    ("conditional", "Conditional", "CONDITIONAL", "", 1)
                                        ], name="Visibility", description="HUD visibility behavior") # type: ignore
    show_transition_type : bpy.props.EnumProperty(items=[
                                    ("none", "None", "NONE", "", 0),
                                    ("fade_in", "Fade In", "FADE IN", "", 1)
                                        ], name="Showing HUD effect") # type: ignore
    show_transition_time : bpy.props.FloatProperty(name="Show Transition Time") # type: ignore
    hide_transition_type : bpy.props.EnumProperty(items=[
                                    ("none", "None", "NONE", "", 0),
                                    ("fade_in", "Fade In", "FADE IN", "", 1)
                                        ], name="Hiding HUD effect") # type: ignore
    hide_transition_time : bpy.props.FloatProperty(name="Hide Transition Time") # type: ignore

class PlayerEntityProperty(bpy.types.PropertyGroup):
    property_name : bpy.props.StringProperty(name="Prop_Name") # type: ignore
    property_type : bpy.props.StringProperty(name="Type") # type: ignore
    property_string : bpy.props.StringProperty(name="Value") # type: ignore
    property_boolean : bpy.props.BoolProperty(name="Value") # type: ignore
    property_float : bpy.props.FloatProperty(name="Value") # type: ignore
    property_integer : bpy.props.IntProperty(name="Value") # type: ignore
'''

class StageObject(bpy.types.PropertyGroup):
    object_name : bpy.props.StringProperty(name="Stage Object Name") # type: ignore
    object_type : bpy.props.StringProperty(name="Stage Object Type") # type: ignore

class ChangeEntityStringPropertyNodeProperties(bpy.types.PropertyGroup):
    source_node_name : bpy.props.StringProperty(default="") # type: ignore
    entity_name : bpy.props.StringProperty(default="") # type: ignore
    operation_selected : bpy.props.EnumProperty(items=string_operations) # type: ignore
    property_selected : bpy.props.StringProperty(default="none") # type: ignore
    operation_parameter : bpy.props.StringProperty(default="") # type: ignore

class ChangeEntityIntegerPropertyNodeProperties(bpy.types.PropertyGroup):
    source_node_name : bpy.props.StringProperty(default="") # type: ignore
    entity_name : bpy.props.StringProperty(default="") # type: ignore
    operation_selected : bpy.props.EnumProperty(items=math_operations) # type: ignore
    property_selected : bpy.props.StringProperty(default="none") # type: ignore
    operation_parameter : bpy.props.IntProperty(default=1) # type: ignore

class ChangeEntityFloatPropertyNodeProperties(bpy.types.PropertyGroup):
    source_node_name : bpy.props.StringProperty(default="") # type: ignore
    entity_name : bpy.props.StringProperty(default="") # type: ignore
    operation_selected : bpy.props.EnumProperty(items=math_operations) # type: ignore
    property_selected : bpy.props.StringProperty(default="none") # type: ignore
    operation_parameter : bpy.props.FloatProperty(default=1.0) # type: ignore

class ChangeEntityBoolPropertyNodeProperties(bpy.types.PropertyGroup):
    source_node_name : bpy.props.StringProperty(default="") # type: ignore
    entity_name : bpy.props.StringProperty(default="") # type: ignore
    operation_selected : bpy.props.EnumProperty(items=bool_operations) # type: ignore
    property_selected : bpy.props.StringProperty(default="none") # type: ignore
    operation_parameter : bpy.props.BoolProperty(default=False) # type: ignore

class ValueNodeProperties(bpy.types.PropertyGroup):
    value : bpy.props.StringProperty(default="") # type: ignore

class GetSceneEntityNodeProperties(bpy.types.PropertyGroup):
    source_node_name : bpy.props.StringProperty(default="") # type: ignore
    entity_name : bpy.props.StringProperty(default="") # type: ignore

class GetHUDContentNodeProperties(bpy.types.PropertyGroup):
    source_node_name : bpy.props.StringProperty(default="") # type: ignore
    content_name : bpy.props.StringProperty(default="") # type: ignore

class GetEntityPropertiesNodeProperties(bpy.types.PropertyGroup):
    source_node_name : bpy.props.StringProperty(default="") # type: ignore
    property_name : bpy.props.StringProperty(default="") # type: ignore

class PlayEntityAnimationNodeProperties(bpy.types.PropertyGroup):
    source_node_name : bpy.props.StringProperty(default="") # type: ignore
    entity_name : bpy.props.StringProperty(default="") # type: ignore
    operation_selected : bpy.props.EnumProperty(items=animation_operations) # type: ignore
    animation_selected : bpy.props.StringProperty(default="none") # type: ignore
    operation_parameter : bpy.props.FloatProperty(default=1.0) # type: ignore

class StageSceneNodeProperties(bpy.types.PropertyGroup):
    source_scene_name : bpy.props.StringProperty(default="") # type: ignore
    player_spawn_object_name : bpy.props.StringProperty(default="") # type: ignore

class TriggerActionNodeProperties(bpy.types.PropertyGroup):
    source_node_name : bpy.props.StringProperty(default="") # type: ignore
    trigger_name : bpy.props.StringProperty(default="") # type: ignore

class PlayerSceneNodeProperties(bpy.types.PropertyGroup):
    source_scene_name : bpy.props.StringProperty(default="") # type: ignore

class HUDSceneNodeProperties(bpy.types.PropertyGroup):
    source_scene_name : bpy.props.StringProperty(default="") # type: ignore
    visibility_type : bpy.props.EnumProperty(items=[
                                    ("always", "Always", "ALWAYS", "", 0),
                                    ("conditional", "Conditional", "CONDITIONAL", "", 1)
                                        ], name="Visibility", description="HUD visibility behavior") # type: ignore
    show_transition_type : bpy.props.EnumProperty(items=[
                                    ("none", "None", "NONE", "", 0),
                                    ("fade_in", "Fade In", "FADE IN", "", 1)
                                        ], name="Showing HUD effect") # type: ignore
    show_transition_time : bpy.props.FloatProperty(name="Show Transition Time") # type: ignore
    hide_transition_type : bpy.props.EnumProperty(items=[
                                    ("none", "None", "NONE", "", 0),
                                    ("fade_in", "Fade In", "FADE IN", "", 1)
                                        ], name="Hiding HUD effect") # type: ignore
    hide_transition_time : bpy.props.FloatProperty(name="Hide Transition Time") # type: ignore

class Menu2dSceneNodeProperties(bpy.types.PropertyGroup):
    source_scene_name : bpy.props.StringProperty(default="") # type: ignore

class Menu3dSceneNodeProperties(bpy.types.PropertyGroup):
    source_scene_name : bpy.props.StringProperty(default="") # type: ignore

class NPCSceneNodeProperties(bpy.types.PropertyGroup):
    source_scene_name : bpy.props.StringProperty(default="") # type: ignore

class OverlaySceneNodeProperties(bpy.types.PropertyGroup):
    source_scene_name : bpy.props.StringProperty(default="") # type: ignore

# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class GameManagerTree(NodeTree):
    # Description string
    '''A custom node tree type that will show up in the editor type list'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'GameManagerTreeType'
    # Label for nice name display
    bl_label = "GameManager Node Tree"
    # Icon identifier
    bl_icon = 'NODETREE'

    def init(self, context):
        print("HEY")


# Custom socket type
class MyCustomSocket(NodeSocket):
    # Description string
    """Custom node socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomSocketType'
    # Label for nice name display
    bl_label = "GameManager Node Socket"

    # Enum items list
    my_items = (
        ('DOWN', "Down", "Where your feet are"),
        ('UP', "Up", "Where your head should be"),
        ('LEFT', "Left", "Not right"),
        ('RIGHT', "Right", "Not left"),
    )

    my_enum_prop: bpy.props.EnumProperty(
        name="Direction",
        description="Just an example",
        items=my_items,
        default='UP',
    ) # type: ignore

    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "my_enum_prop", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.0, 0.4, 0.216, 0.5)


# Mix-in class for all custom nodes in this tree type.
# Defines a poll function to enable instantiation.
class MyCustomTreeNode:
    @classmethod
    def poll(cls, ntree):
        return ntree.bl_idname == 'GameManagerTreeType'


# Derived from the Node base type.
class MyCustomNode(MyCustomTreeNode, Node):
    '''A custom node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomNodeType'
    # Label for nice name display
    bl_label = "Custom Node"
    # Icon identifier
    bl_icon = 'SOUND'

    my_string_prop: bpy.props.StringProperty() # type: ignore
    my_float_prop: bpy.props.FloatProperty(default=3.1415926) # type: ignore

    def init(self, context):
        self.inputs.new('CustomSocketType', "Hello")
        self.inputs.new('NodeSocketFloat', "World")
        self.inputs.new('NodeSocketVector', "!")

        self.outputs.new('NodeSocketColor', "How")
        self.outputs.new('NodeSocketColor', "are")
        self.outputs.new('NodeSocketFloat', "you")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        layout.label(text="Node settings")
        layout.prop(self, "my_float_prop")

    def draw_buttons_ext(self, context, layout):
        layout.prop(self, "my_float_prop")
        # my_string_prop button will only be visible in the sidebar
        layout.prop(self, "my_string_prop")

    def draw_label(self):
        return "I am a custom node"

# --- SOCKETS ---
class B2G_Float_Socket(NodeSocketFloat):
    # Description string
    """float socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Float_SocketType'
    # Label for nice name display
    bl_label = "Float Socket"
    
    default_value : bpy.props.FloatProperty(default=0.0) # type: ignore
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.5, 0.5, 0.0, 1.0)

class B2G_Integer_Socket(NodeSocketInt):
    # Description string
    """integer socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Integer_SocketType'
    # Label for nice name display
    bl_label = "Integer Socket"
    
    default_value : bpy.props.IntProperty(default=0) # type: ignore
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.94,0.97,1.00, 1.0)

class B2G_Boolean_Socket(NodeSocketBool):
    # Description string
    """boolean socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Boolean_SocketType'
    # Label for nice name display
    bl_label = "Boolean Socket"
    
    default_value : bpy.props.BoolProperty(default=False) # type: ignore
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.5, 0.5, 0.0, 1.0)

class B2G_String_Socket(NodeSocketString):
    # Description string
    """string socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_String_SocketType'
    # Label for nice name display
    bl_label = "String Socket"
    
    default_value : bpy.props.StringProperty(default="empty") # type: ignore
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.prop(self, "default_value", text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.0, 0.5, 0.5, 1.0)
    
    def update(self, context):
        self.hide_value = False


'''
class B2G_Custom_Socket_Interface(NodeSocketInterface):
    bl_socket_idname = "B2G_String_Socket"

    def draw(self, context, layout):
        pass

    def draw_color(self, context: Context):
        return (0.1,1,1)
'''

class B2G_Pipeline_Socket(NodeSocket):
    # Description string
    """Pipeline socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Pipeline_SocketType'
    # Label for nice name display
    bl_label = "Pipeline Socket"
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.0, 1.0, 0.0, 1.0)

class B2G_Stage_Socket(NodeSocket):
    # Description string
    """Stage socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Stage_SocketType'
    # Label for nice name display
    bl_label = "Stage Socket"
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.0, 1.0, 0.0, 1.0)

class B2G_2dmenu_Socket(NodeSocket):
    # Description string
    """2d menu socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_2dmenu_SocketType'
    # Label for nice name display
    bl_label = "2D Menu Socket"
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.0, 1.0, 0.0, 1.0)

class B2G_OverlayMenu_Socket(NodeSocket):
    # Description string
    """overlay menu socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_OverlayMenu_SocketType'
    # Label for nice name display
    bl_label = "Overlay Menu Socket"
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.00,0.60,0.80, 1.0)

class B2G_3dmenu_Socket(NodeSocket):
    # Description string
    """3d menu socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_3dmenu_SocketType'
    # Label for nice name display
    bl_label = "3D Menu Socket"
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.0, 1.0, 0.0, 1.0)

class B2G_Player_Socket(NodeSocket):
    # Description string
    """player socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Player_SocketType'
    # Label for nice name display
    bl_label = "Player Socket"
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.00,0.80,0.60, 1.0)

class B2G_HUD_Socket(NodeSocket):
    # Description string
    """ hud socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_HUD_SocketType'
    # Label for nice name display
    bl_label = "HUD Socket"
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (1.00,0.75,0.00, 1.00)

class B2G_Trigger_Socket(NodeSocket):
    # Description string
    """triggger socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Trigger_SocketType'
    # Label for nice name display
    bl_label = "Trigger Socket"
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.1,0.8,0.2, 1.0)

# --- END SOCKETS ---

# --- PIPELINE NODES ---
class B2G_Start_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Start_NodeType'
    # Label for nice name display
    bl_label = "Start"
    # Icon identifier
    bl_icon = 'NODE'
    
    def init(self, context):
        _new_socket = self.outputs.new("B2G_Pipeline_SocketType", "Go")
        #_new_socket.display_shape="SQUARE"
        #_new_socket.description = "Pipeline socket"
        _new_socket.link_limit = 1
        #self.use_custom_color = True
        #self.color = (1.0,1.0,1.0)

    #def draw_header(self, context):
        #layout = self.layout
        #layout.label(icon_value=addon_config.preview_collections[0]["pipeline_icon"].icon_id)        

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        #layout.label(text="Start")
        pass

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Start"

    def update(self):
        '''Called when node graph is changed'''
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        pass

class B2G_Finish_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Finish_NodeType'
    # Label for nice name display
    bl_label = "Finish"
    # Icon identifier
    bl_icon = 'NODE'

    def init(self, context):
        _new_input = self.inputs.new("B2G_Pipeline_SocketType", "Go")
        _new_input.link_limit = 0

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        #layout.label(text="Finish")
        pass

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Finish"

# --- END PIPELINE NODES ---

# --- MATH NODES ---
# --- END MATH NODES ---

# --- VARIABLE NODES ---
class B2G_Float_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Float_NodeType'
    # Label for nice name display
    bl_label = "B2G Float Node"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0
    bl_description = "Float Variable Node"

    node_properties : bpy.props.PointerProperty(type=ValueNodeProperties) # type: ignore

    def on_my_value_update(self, context):
        self.node_properties.value = str(self.my_value)

    my_value : bpy.props.FloatProperty(name="MyFloat", update=on_my_value_update) # type: ignore

    def init(self, context):
        self.outputs.new("B2G_Float_SocketType", "Value")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "my_value", text="")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Float"
    
    def update_inputs(self):
        pass

    def update_outputs(self):
        pass

class B2G_Integer_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Integer_NodeType'
    # Label for nice name display
    bl_label = "B2G Integer Node"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=ValueNodeProperties) # type: ignore

    def on_my_value_update(self, context):
        self.node_properties.value = str(self.my_value)

    my_value : bpy.props.IntProperty(name="MyInt", update=on_my_value_update) # type: ignore

    def init(self, context):
        self.outputs.new("B2G_Integer_SocketType", "Value")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "my_value", text="")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Integer"
    
    def update_inputs(self):
        pass

    def update_outputs(self):
        pass

class B2G_String_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_String_NodeType'
    # Label for nice name display
    bl_label = "B2G String Node"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=ValueNodeProperties) # type: ignore

    def on_my_value_update(self, context):
        self.node_properties.value = str(self.my_value)

    my_value : bpy.props.StringProperty(name="MyString", update=on_my_value_update) # type: ignore

    def init(self, context):
        self.outputs.new("B2G_String_SocketType", "Value")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "my_value", text="")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "String"
    
    def update_inputs(self):
        pass

    def update_outputs(self):
        pass

class B2G_Boolean_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Boolean_NodeType'
    # Label for nice name display
    bl_label = "B2G Boolean Node"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=ValueNodeProperties) # type: ignore

    def on_my_value_update(self, context):
        self.node_properties.value = str(self.my_value)

    my_value : bpy.props.BoolProperty(name="MyBoolean", update=on_my_value_update) # type: ignore

    def init(self, context):
        self.outputs.new("B2G_Boolean_SocketType", "Value")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "my_value", text="")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "String"
    
    def update_inputs(self):
        pass

    def update_outputs(self):
        pass

# --- END VARIABLE NODES ---

# --- SCENE NODES ---
class B2G_Stage_Scene_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Stage_Scene_NodeType'
    # Label for nice name display
    bl_label = "Stage Scene"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    def on_player_spawn_enum_update(self, context):
        self.node_properties.player_spawn_object_name = self.player_spawn_enum.name
    
    node_properties : bpy.props.PointerProperty(type=StageSceneNodeProperties) # type: ignore
    player_spawn_enum : bpy.props.PointerProperty(type=bpy.types.Object, name="Player Spawn", poll=player_spawns_poll, update=on_player_spawn_enum_update) # type: ignore

    def on_update_scene(self, context):
        # Clear inputs/outputs
        self.inputs.clear()
        self.outputs.clear()
        if self.scene:
            self.node_properties.source_scene_name = self.scene.name
            self.outputs.new("B2G_Player_SocketType", "Stage_REF")
            self.inputs.new("B2G_Pipeline_SocketType", "Go")
            self.inputs.new("B2G_Player_SocketType", "Player")
            self.inputs.new("B2G_HUD_SocketType", "HUD")
            self.inputs.new("B2G_OverlayMenu_SocketType", "Pause Menu")
            for _property in self.scene.entity_properties:
                self.inputs.new(property_node_sockets[_property.property_type], _property.property_name)
        else:
            self.node_properties.source_scene_name = ""

    def poll_scenes(self, object):
        return object.scene_type == "stage"
    
    scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Scene", update=on_update_scene, poll=poll_scenes) # type: ignore

    def create_output_socket(self, _socket_name):
        _socket_found = False
        _output_socket_name = _socket_name + "_REF"
        for _output in self.outputs:
            if _output.name == _output_socket_name:
                _socket_found = True
                break
        if not _socket_found:
            self.outputs.new("B2G_Player_SocketType", _output_socket_name)

    def delete_output_socket(self, _socket_name):
        for _socket in self.outputs:
            if _socket.name == (_socket_name + "_REF"):
                self.outputs.remove(_socket)
                break

    def is_input_socket_linked(self, _socket_name):
        _linked = False
        for _socket in self.inputs:
            if _socket.name == _socket_name:
                if _socket.is_linked:
                    _linked = True
                    break
        return _linked

    def init(self, context):
        pass
        #_new_output = self.outputs.new("B2G_Pipeline_SocketType", "Go")
        #_new_output.link_limit = 1

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "scene", text="Scene")
        if self.scene:
            # Player link
            if self.inputs[1].is_linked:
                row3 = box1.row()
                row3.prop(self, "player_spawn_enum", text="Spawn Empty")
                if not self.player_spawn_enum:
                    row2 = box1.row()
                    row2.label(text="Player spawn not set", icon="INFO")
            else:
                row2 = box1.row()
                row2.label(text="Player not set", icon="INFO")
            # Go link
            if self.inputs[0].is_linked:
                pass
            else:
                row2 = box1.row()
                row2.label(text="Stage not in pipeline", icon="INFO")
        else:
            row2 = box1.row()
            row2.label(text="Stage scene not set", icon="INFO")


        # EXPORT PROPERTY
        #if self.scene:
            #layout.prop(self.scene, "scene_exportable", text="Export")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(Stage)")
        else:
            return "Stage"
    
    def update(self):
        '''Called when node graph is changed'''
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.mark_invalid_links)

    def update_sockets(self):
        _optional_sockets = ["Player", "HUD", "Pause Menu"]
        if self.scene:
            self.create_output_socket("Stage")
            for _opt_socket in _optional_sockets:
                if self.is_input_socket_linked(_opt_socket):
                    self.create_output_socket(_opt_socket)
                else:
                    self.delete_output_socket(_opt_socket)


    def mark_invalid_links(self):
        pass
        '''Mark invalid links, must be called from a timer'''
        '''
        if len(self.inputs) > 0:
            _input_player = self.inputs[0]
            for _link in _input_player.links:
                _valid_link = False
                if type(_link.from_node).__name__ == "B2G_Player_Scene_Node":
                    _valid_link = True
                else:
                    _valid_link = False
                _link.is_valid = _valid_link
            _input_go = self.inputs[1]
            for _link in _input_go.links:
                _valid_link = False
                if ((type(_link.from_socket).__name__ == "B2G_Pipeline_Socket") or (type(_link.from_socket).__name__ == "B2G_Stage_Socket")):
                    _valid_link = True
                else:
                    _valid_link = False
                _link.is_valid = _valid_link
    '''
        
class B2G_Player_Scene_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Player_Scene_NodeType'
    # Label for nice name display
    bl_label = "Player Scene"
    # Icon identifier
    bl_icon = 'OUTLINER_OB_ARMATURE'
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=PlayerSceneNodeProperties) # type: ignore
    actions_settings : bpy.props.CollectionProperty(type=ActionProperty) # type: ignore

    def poll_scenes(self, object):
        return object.scene_type == "player"
    
    def on_update_scene(self, context):
        if self.scene:
            self.node_properties.source_scene_name = self.scene.name
        else:
            self.node_properties.source_scene_name = ""
        # Update actions
        self.actions_settings.clear()
        if self.scene:
            _actions_template = get_controls_template(self, context, self.scene)
            if _actions_template is not None:
                for _control_property in self.scene.controls_settings:
                    _new_action_setting = self.actions_settings.add()
                    _new_action_setting.action_id = _control_property.motion_name
                    for _key in _actions_template.keys():
                        #print(_key, " versus ", _new_action_setting.action_id)
                        if _key == _new_action_setting.action_id:
                            _new_action_setting.action_process = _actions_template[_key]["ActionID"]
                            break
            else:
                print("No template")
                for _control_property in self.scene.controls_settings:
                    _new_action_setting = self.actions_settings.add()
                    _new_action_setting.action_id = _control_property.motion_name
        # Update entity properties
        self.outputs.clear()
        self.inputs.clear()
        if self.scene:
            self.outputs.new("B2G_Player_SocketType", "Player")
        # Load entity properties as new inputs/outputs
        if self.scene:
            for _entity_property in self.scene.entity_properties:
                _new_socket = self.inputs.new(property_node_sockets[_entity_property.property_type], _entity_property.property_name)
                match _entity_property.property_type:
                    case "boolean":
                        #_new_socket.default_value = bool(_entity_property.property_value)
                        _new_socket.default_value = False
                    case "string":
                        #_new_socket.default_value = _entity_property.property_value
                        _new_socket.default_value = ""
                    case "integer":
                        #_new_socket.default_value = int(_entity_property.property_value)
                        _new_socket.default_value = 0
                    case "float":
                        #_new_socket.default_value = float(_entity_property.property_value)
                        _new_socket.default_value = 0.0
                #self.outputs.new(property_node_sockets[_entity_property.property_type], _entity_property.property_name)

    scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Scene", poll=poll_scenes, update=on_update_scene) # type: ignore

    def init(self, context):
        pass

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "scene", text="Scene")
        if self.scene:
            box2 = box1.box()
            row2 = box2.row()
            row2.label(text="Player Actions")
            for _player_action in self.actions_settings:
                if _player_action.action_id.find("action") < 0:
                    continue
                row3 = box2.row()
                _action_rename = _player_action.action_id.replace("b2g_", "")
                _name_parts = _action_rename.split("_")
                for _p_index,_name_part in enumerate(_name_parts):
                    _name_parts[_p_index] = _name_part.capitalize()
                _action_rename = " ".join(_name_parts)
                row3.prop(_player_action, "action_process", text=_action_rename)
            '''
            box3 = box1.box()
            row4 = box3.row()
            row4.label(text="Player Properties")
            for _player_property in self.entity_properties:
                row5 = box3.row()
                match _player_property.property_type:
                    case "boolean":
                        row5.prop(_player_property, "property_boolean", text=_player_property.property_name)
                    case "string":
                        row5.prop(_player_property, "property_string", text=_player_property.property_name)
                    case "integer":
                        row5.prop(_player_property, "property_integer", text=_player_property.property_name)
                    case "float":
                        row5.prop(_player_property, "property_float", text=_player_property.property_name)
            '''
            #box1.prop(self.scene, "scene_exportable", text="Export")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(Player)")
        else:
            return "Player"
    
    def update(self):
        '''Called when node graph is changed'''
        #print("Update", self.name)
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        '''Mark invalid links, must be called from a timer'''
        #print("Update", self.name, "links")
        pass
        '''
        _output_player = self.outputs[2]
        for _link in _output_player.links:
            _valid_link = False
            if type(_link.from_socket).__name__ == "B2G_HUD_Socket":
                _valid_link = True
            else:
                _valid_link = False
            _link.is_valid = _valid_link
        '''
    
class B2G_HUD_Scene_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_HUD_Scene_NodeType'
    # Label for nice name display
    bl_label = "HUD Scene"
    # Icon identifier
    bl_icon = 'DESKTOP'
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=HUDSceneNodeProperties) # type: ignore

    def poll_scenes(self, object):
        return object.scene_type == "hud"
    
    def on_update_scene(self, context):
        self.outputs.clear()
        if self.scene:
            self.outputs.new("B2G_Player_SocketType", "HUD")
            self.node_properties.source_scene_name = self.scene.name
        else:
            self.node_properties.source_scene_name = ""
        # Clean inputs on change scene
        self.inputs.clear()
        # Load entity properties as new inputs
        if self.scene:
            for _object in self.scene.objects:
                #print(_entity_property.property_name)
                if hasattr(_object, "hud_element_properties"):
                    match _object.hud_element_properties.element_type:
                        case "text_content":
                            self.inputs.new("B2G_String_SocketType", _object.name)
                        case "horizontal_content":
                            self.inputs.new("B2G_Float_SocketType", _object.name)
                        case "vertical_content":
                            self.inputs.new("B2G_Float_SocketType", _object.name)
        else:
            self.inputs.clear()

    scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Scene", poll=poll_scenes, update=on_update_scene) # type: ignore
    #settings : bpy.props.PointerProperty(type=HudSettings, name="HudSettings") # type: ignore
    
    def init(self, context):
        pass

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "scene", text="Scene")
        if self.scene:
            row2 = box1.row()
            row2.prop(self.node_properties, "visibility_type", text="Visibility")
            row2 = box1.row()
            row2.prop(self.node_properties, "show_transition_type", text="Show Transition Type")
            row2 = box1.row()
            row2.prop(self.node_properties, "show_transition_time", text="Show Transition Time")
            row2 = box1.row()
            row2.prop(self.node_properties, "hide_transition_type", text="Hide Transition Type")
            row2 = box1.row()
            row2.prop(self.node_properties, "hide_transition_time", text="Hide Transition Time")
            #layout.prop(self.scene, "scene_exportable", text="Export")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(HUD)")
        else:
            return "HUD"

    def update(self):
        '''Called when node graph is changed'''
        #print("Update", self.name, "links")
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        pass
        '''
        valid_sockets = ["B2G_Float_Socket", "B2G_Integer_Socket", "B2G_Boolean_Socket", "B2G_String_Socket"]
        for _input in self.inputs:
            if type(_input).__name__ != "B2G_HUD_Socket":
                for _link in _input.links:
                    _valid_link = False
                    #print(type(_link.from_socket).__name__)
                    if type(_link.from_socket).__name__ in valid_sockets:
                        _valid_link = True
                    else:
                        _valid_link = False
                        print("Invalidating:", _link)
                    _link.is_valid = _valid_link
        '''

class B2G_NPC_Scene_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_NPC_Scene_NodeType'
    # Label for nice name display
    bl_label = "NPC Scene"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    def poll_scenes(self, object):
        return object.scene_type == "npc"
    
    scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Scene", poll=poll_scenes) # type: ignore
    
    def init(self, context):
        self.inputs.new("B2G_Pipeline_SocketType", "Go")
        self.outputs.new("B2G_Pipeline_SocketType", "Go")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "scene", text="Scene")
        if self.scene:
            row2 = box1.row()
            layout.prop(self.scene, "scene_exportable", text="Export")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(NPC)")
        else:
            return "NPC"

class B2G_2dMenu_Scene_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_2dMenu_Scene_NodeType'
    # Label for nice name display
    bl_label = "Menu 2D Scene"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_prpperties : bpy.props.PointerProperty(type=Menu2dSceneNodeProperties) # type: ignore

    def poll_scenes(self, object):
        return object.scene_type == "2dmenu"

    def on_update_scene(self, context):
        if self.scene:
            self.node_properties.source_scene_name = self.scene.name
        else:
            self.node_properties.source_scene_name = ""
        # Clean new outputs on change scene
        self.outputs.clear()
        #self.new_outputs.clear()
        # Load entity properties as new outputs
        if self.scene:
            self.special_objects.clear()
            for _object in self.scene.objects:
                if _object.menu2d_object_properties.menu2d_object_type == "button":
                    _new_special_object = self.special_objects.add()
                    _new_special_object.button_node_name = self.name
                    _new_special_object.button_name = _object.name
        else:
            self.outputs.clear()
            #for _new_output in self.new_outputs:
                #self.outputs.remove(_new_output)
            #self.new_outputs.clear()

    scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Scene", poll=poll_scenes, update=on_update_scene) # type: ignore
    
    def init(self, context):
        self.inputs.new("B2G_Pipeline_SocketType", "Go")
        

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "scene", text="Scene")
        if self.scene:
            row2 = box1.row()
            box2 = row2.box()
            #row3 = box2.row()
            #row3.label(text=_object.name)
            for _special_object in self.special_objects:
                box3 = box2.box()
                row4 = box3.row()
                row4.label(text=_special_object.button_name)
                row5 = box3.row()
                row5.prop(_special_object, "button_action_on_click")
            layout.prop(self.scene, "scene_exportable", text="Export")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(Menu 2D)")
        else:
            return "Menu 2D"

    def update(self):
        '''Called when node graph is changed'''
        #print("Update", self.name)
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        '''Mark invalid links, must be called from a timer'''
        _input_go = self.inputs[0]
        for _link in _input_go.links:
            _valid_link = False
            if ((type(_link.from_socket).__name__ == "B2G_Pipeline_Socket") or (type(_link.from_socket).__name__ == "B2G_2dmenu_Socket")):
                _valid_link = True
            else:
                _valid_link = False
            _link.is_valid = _valid_link

    def update_sockets(self):
        #print("Update", self.name, "links")
        for _special_object in self.special_objects:
            match _special_object.button_action_on_click:
                    case "none":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index > -1:
                            self.outputs.remove(self.outputs[_special_object.button_name])
                    case "load_stage":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index == -1:
                            _new_socket = self.outputs.new("B2G_Stage_SocketType", _special_object.button_name)
                            _new_socket.link_limit = 1
                            #self.new_outputs.append(self.outputs.new("B2G_Stage_SocketType", _special_object.button_name))
                        else:
                            if type(self.outputs[_output_index]).__name__ != "B2G_Stage_Socket":
                                self.outputs.remove(self.outputs[_special_object.button_name])
                                self.outputs.new("B2G_Stage_SocketType", _special_object.button_name)
                    case "load_2dmenu":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index == -1:
                            _new_socket = self.outputs.new("B2G_2dmenu_SocketType", _special_object.button_name)
                            _new_socket.link_limit = 1
                        else:
                            if type(self.outputs[_output_index]).__name__ != "B2G_2dmenu_Socket":
                                self.outputs.remove(self.outputs[_special_object.button_name])
                                self.outputs.new("B2G_2dmenu_SocketType", _special_object.button_name)
                    case "load_3dmenu":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index == -1:
                            _new_socket = self.outputs.new("B2G_3dmenu_SocketType", _special_object.button_name)
                            _new_socket.link_limit = 1
                        else:
                            if type(self.outputs[_output_index]).__name__ != "B2G_3dmenu_Socket":
                                self.outputs.remove(self.outputs[_special_object.button_name])
                                self.outputs.new("B2G_3dmenu_SocketType", _special_object.button_name)
                    case "quit_game":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index > -1:
                            self.outputs.remove(self.outputs[_special_object.button_name])

class B2G_OverlayMenu_Scene_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_OverlayMenu_Scene_NodeType'
    # Label for nice name display
    bl_label = "Menu Overlay Scene"
    # Icon identifier
    bl_icon = 'NODE_COMPOSITING'
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=OverlaySceneNodeProperties) # type: ignore

    def poll_scenes(self, object):
        return object.scene_type == "overlay_menu"

    def on_update_scene(self, context):
        if self.scene:
            self.node_properties.source_scene_name = self.scene.name
        else:
            self.node_properties.source_scene_name = ""
        # Clean outputs
        self.inputs.clear()
        # Set default outputs
        self.inputs.new("B2G_OverlayMenu_SocketType", "Overlay")
        # Clean new outputs on change scene
        self.outputs.clear()
        #self.new_outputs.clear()
        # Load entity properties as new outputs
        if self.scene:
            self.overlay_special_objects.clear()
            for _object in self.scene.objects:
                if _object.menu_overlay_object_properties.menu_overlay_object_type == "button":
                    _new_special_object = self.overlay_special_objects.add()
                    _new_special_object.button_node_name = self.name
                    _new_special_object.button_name = _object.name
        else:
            self.outputs.clear()
            #for _new_output in self.new_outputs:
                #self.outputs.remove(_new_output)
            #self.new_outputs.clear()

    scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Scene", poll=poll_scenes, update=on_update_scene) # type: ignore
    
    def init(self, context):
        self.inputs.new("B2G_OverlayMenu_SocketType", "Overlay")
        

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "scene", text="Scene")
        row3 = box1.row()
        row3.prop(self, "with_pause", text="Pause Game")
        if self.scene:
            row2 = box1.row()
            box2 = row2.box()
            #row3 = box2.row()
            #row3.label(text=_object.name)
            for _special_object in self.overlay_special_objects:
                box3 = box2.box()
                row4 = box3.row()
                row4.label(text=_special_object.button_name)
                row5 = box3.row()
                row5.prop(_special_object, "button_action_on_click")
            layout.prop(self.scene, "scene_exportable", text="Export")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(Menu Overlay)")
        else:
            return "Menu Overlay"

    def update(self):
        '''Called when node graph is changed'''
        #print("Update", self.name)
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        '''Mark invalid links, must be called from a timer'''
        _input_go = self.inputs[0]
        for _link in _input_go.links:
            _valid_link = False
            if ((type(_link.from_socket).__name__ == "B2G_Pipeline_Socket") or (type(_link.from_socket).__name__ == "B2G_OverlayMenu_Socket")):
                _valid_link = True
            else:
                _valid_link = False
            _link.is_valid = _valid_link

    def update_sockets(self):
        #print("Update", self.name, "links")
        for _special_object in self.overlay_special_objects:
            match _special_object.button_action_on_click:
                    case "none":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index > -1:
                            self.outputs.remove(self.outputs[_special_object.button_name])
                    case "load_stage":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index == -1:
                            _new_socket = self.outputs.new("B2G_Stage_SocketType", _special_object.button_name)
                            _new_socket.link_limit = 1
                        else:
                            if type(self.outputs[_output_index]).__name__ != "B2G_Stage_Socket":
                                self.outputs.remove(self.outputs[_special_object.button_name])
                                self.outputs.new("B2G_Stage_SocketType", _special_object.button_name)
                    case "load_2dmenu":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index == -1:
                            _new_socket = self.outputs.new("B2G_2dmenu_SocketType", _special_object.button_name)
                            _new_socket.link_limit = 1
                        else:
                            if type(self.outputs[_output_index]).__name__ != "B2G_2dmenu_Socket":
                                self.outputs.remove(self.outputs[_special_object.button_name])
                                self.outputs.new("B2G_2dmenu_SocketType", _special_object.button_name)
                    case "load_3dmenu":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index == -1:
                            _new_socket = self.outputs.new("B2G_3dmenu_SocketType", _special_object.button_name)
                            _new_socket.link_limit = 1
                        else:
                            if type(self.outputs[_output_index]).__name__ != "B2G_3dmenu_Socket":
                                self.outputs.remove(self.outputs[_special_object.button_name])
                                self.outputs.new("B2G_3dmenu_SocketType", _special_object.button_name)
                    case "quit_game":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index > -1:
                            self.outputs.remove(self.outputs[_special_object.button_name])

class B2G_3dMenu_Scene_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_3dMenu_Scene_NodeType'
    # Label for nice name display
    bl_label = "Menu 3D Scene"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    new_outputs = []
    node_properties : bpy.props.PointerProperty(type=Menu3dSceneNodeProperties) # type: ignore

    def poll_scenes(self, object):
        return object.scene_type == "3dmenu"

    def on_update_scene(self, context):
        if self.scene:
            self.node_properties.source_scene_name = self.scene.name
        else:
            self.node_properties.source_scene_name = ""
        # Clean new outputs on change scene
        self.outputs.clear()
        self.new_outputs.clear()
        # Load entity properties as new outputs
        if self.scene:
            self.special_objects.clear()
            for _object in self.scene.objects:
                if _object.special_object_info.menu_object_type == "button":
                    _new_special_object = self.special_objects.add()
                    _new_special_object.button_node_name = self.name
                    _new_special_object.button_name = _object.name
        else:
            for _new_output in self.new_outputs:
                self.outputs.remove(_new_output)
            self.new_outputs.clear()

    scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Scene", poll=poll_scenes, update=on_update_scene) # type: ignore
    
    def init(self, context):
        self.inputs.new("B2G_Pipeline_SocketType", "Go")
        

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "scene", text="Scene")
        if self.scene:
            row2 = box1.row()
            box2 = row2.box()
            #row3 = box2.row()
            #row3.label(text=_object.name)
            for _special_object in self.special_objects:
                box3 = box2.box()
                row4 = box3.row()
                row4.label(text=_special_object.button_name)
                row5 = box3.row()
                row5.prop(_special_object, "button_action_on_click")
            #row4.prop(_object.special_object_info, "button_action_on_click", text="Action")
            layout.prop(self.scene, "scene_exportable", text="Export")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(Menu 3D)")
        else:
            return "Menu 3D"

    def update(self):
        '''Called when node graph is changed'''
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        '''Mark invalid links, must be called from a timer'''
        _input_go = self.inputs[0]
        for _link in _input_go.links:
            print(type(_link.from_socket).__name__)
            _valid_link = False
            if ((type(_link.from_socket).__name__ == "B2G_Pipeline_Socket") or (type(_link.from_socket).__name__ == "B2G_3dmenu_Socket")):
                _valid_link = True
            else:
                _valid_link = False
            _link.is_valid = _valid_link

    def update_sockets(self):
        #print("Update", self.name, "links")
        for _special_object in self.special_objects:
            match _special_object.button_action_on_click:
                    case "none":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index > -1:
                            self.outputs.remove(self.outputs[_special_object.button_name])
                    case "load_stage":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index == -1:
                            _new_socket = self.outputs.new("B2G_Stage_SocketType", _special_object.button_name)
                            _new_socket.link_limit = 1
                        else:
                            if type(self.outputs[_output_index]).__name__ != "B2G_Stage_Socket":
                                self.outputs.remove(self.outputs[_special_object.button_name])
                                self.outputs.new("B2G_Stage_SocketType", _special_object.button_name)
                    case "load_2dmenu":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index == -1:
                            _new_socket = self.outputs.new("B2G_2dmenu_SocketType", _special_object.button_name)
                            _new_socket.link_limit = 1
                        else:
                            if type(self.outputs[_output_index]).__name__ != "B2G_2dmenu_Socket":
                                self.outputs.remove(self.outputs[_special_object.button_name])
                                self.outputs.new("B2G_2dmenu_SocketType", _special_object.button_name)
                    case "load_3dmenu":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index == -1:
                            _new_socket = self.outputs.new("B2G_3dmenu_SocketType", _special_object.button_name)
                            _new_socket.link_limit = 1
                        else:
                            if type(self.outputs[_output_index]).__name__ != "B2G_3dmenu_Socket":
                                self.outputs.remove(self.outputs[_special_object.button_name])
                                self.outputs.new("B2G_3dmenu_SocketType", _special_object.button_name)
                    case "quit_game":
                        _output_index = self.outputs.find(_special_object.button_name)
                        if _output_index > -1:
                            self.outputs.remove(self.outputs[_special_object.button_name])

# --- END SCENE NODES ---

# --- ACTION NODES ---
class B2G_Change_Property_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Change_Property_NodeType'
    # Label for nice name display
    bl_label = "Change Property"
    # Icon identifier
    bl_icon = 'LINENUMBERS_ON'
    bl_width_default = 200.0
    bl_height_default = 100.0

    entity_props = [
            ("none", "None", "NONE"),
    ]
    properties_operations = {
        "float" : [
            ("none", "None", "NONE"),
            ("add", "Add", "ADD"),
            ("sub", "Sub", "SUB")
        ],
        "integer" : [
            ("none", "None", "NONE"),
            ("add", "Add", "ADD"),
            ("sub", "Sub", "SUB")
        ],
        "boolean" : [
            ("none", "None", "NONE"),
            ("neg", "Neg", "NEG"),
        ],
        "string" : [
            ("none", "None", "NONE"),
            ("concat", "Concat", "CONCAT"),
        ]
    }

    current_property_type : bpy.props.StringProperty(name="Current Property Type", default="") # type: ignore

    source_node_name : bpy.props.StringProperty(name="Source Node Name", default="") # type: ignore

    def get_entity_props(self, context):
        return self.entity_props
    
    def get_operations(self, context):
        _operations = [("none", "None", "NONE"),]
        if self.current_property_type == "":
            return _operations
        else:
            return self.properties_operations[self.current_property_type]

    def on_update_property_selected(self, context):
        self.operation_selected = "none"
        print("Source node name:", self.source_node_name)
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.source_node_name]
                if hasattr(_source_node, "scene"):
                    for _prop in _source_node.scene.entity_properties:
                        if _prop.property_name == self.property_selected:
                            self.current_property_type = _prop.property_type
                            '''
                            if len(self.inputs) < 3:
                                self.inputs.new(property_node_sockets[self.current_property_type], "Param")
                            else:
                                self.inputs.remove(self.inputs[2])
                                self.inputs.new(property_node_sockets[self.current_property_type], "Param")
                            '''
                            break
                        #print("Prop:", _prop)
                else:
                    print("Has no scene attr", self.source_node.name)
            #else:
                #print(self, "Not self.source_node")

    property_selected : bpy.props.EnumProperty(items=get_entity_props, update=on_update_property_selected, name="Property selected") # type: ignore
    operation_selected : bpy.props.EnumProperty(items=get_operations, name="Operation selected") # type: ignore

    #float_param : bpy.props.FloatProperty(default=0.0) # type: ignore
    #integer_param : bpy.props.IntProperty(default=0) # type: ignore
    #string_param : bpy.props.StringProperty(default="") # type: ignore
    #boolean_param : bpy.props.BoolProperty(default=False) # type: ignore
    
    def init(self, context):
        self.inputs.new("B2G_Pipeline_SocketType", "Do")
        self.inputs.new("B2G_Player_SocketType", "Entity Ref")
        self.update()

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        if self.inputs[1].is_linked:
            row1 = layout.row()
            row1.prop(self, "property_selected", text="Property")
            #print("Self source name:", self.source_node_name)
            if self.property_selected == "none":
                pass
            else:
                for _node in bpy.data.node_groups["GameManager"].nodes:
                    if _node.name == self.source_node_name:
                        _source_node = bpy.data.node_groups["GameManager"].nodes[self.source_node_name]
                        if hasattr(_source_node, "scene"):
                            #row2 = layout.row()
                            for _prop in _source_node.scene.entity_properties:
                                #print("Property", _prop.property_name, "vs", self.property_selected)
                                if _prop.property_name == self.property_selected:
                                    row3 = layout.row()
                                    row3.prop(self, "operation_selected", text="Operation")
                                    break
                        break

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Change Property"

    def update(self):
        '''Called when node graph is changed'''
        if not self.inputs[1].is_linked:
            self.property_selected = "none"
            self.operation_selected = "none"
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.update_buttons)
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        pass
        '''Mark invalid links, must be called from a timer
        _input_go = self.inputs[0]
        for _link in _input_go.links:
            print(type(_link.from_socket).__name__)
            _valid_link = False
            if ((type(_link.from_socket).__name__ == "B2G_Pipeline_Socket") or (type(_link.from_socket).__name__ == "B2G_3dmenu_Socket")):
                _valid_link = True
            else:
                _valid_link = False
            _link.is_valid = _valid_link'''

    def update_buttons(self):
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.source_node_name]
                break
            else:
                _source_node = None

        if _source_node:
            if self.inputs[1].is_linked:
                self.source_node_name = self.inputs[1].links[0].from_node.name
                for _input in _source_node.inputs:
                    if (_input.name + " REF") == self.inputs[1].links[0].from_socket.name:
                        _source_node = _input.links[0].from_node
                        self.source_node_name = _source_node.name
                        break
                if _source_node.scene:
                    #print("Node scene found")
                    if hasattr(_source_node.scene, "entity_properties"):
                        self.entity_props.clear()
                        #print("Node scene", _source_node.scene.name, "has entity_properties")
                        self.entity_props.append(("none", "None", "NONE"))
                        for _prop in _source_node.scene.entity_properties:
                            self.entity_props.append((_prop.property_name, _prop.property_name, _prop.property_name))
                        #print("Properties:", self.entity_props)
                    else:
                        print("Node hasn't entity_properties")
            else:
                print("Inputs not linked")

    def update_sockets(self):
        match self.current_property_type:
            case "float":
                pass
                #if len(self.inputs) > 2:

class B2G_Change_Entity_String_Property_Node(MyCustomTreeNode, Node):
    bl_idname = 'B2G_Change_Entity_String_Property_NodeType'
    bl_label = "Change Entity String Property"
    bl_icon = 'LINENUMBERS_ON'
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=ChangeEntityStringPropertyNodeProperties) # type: ignore

    new_source_node_name : bpy.props.StringProperty(default="") # type: ignore
    
    def get_entity_props(self, context):
        entity_props = [
                ("none", "None", "NONE"),
        ]
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.node_properties.source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.node_properties.source_node_name]
                if len(_source_node.inputs[0].links) > 0:
                    _remote_node = _source_node.inputs[0].links[0].from_node
                    if hasattr(_remote_node, "scene"):
                        for _obj in _remote_node.scene.objects:
                            if _obj.name == _source_node.node_properties.entity_name:
                                for _prop in _obj.entity_properties:
                                    if _prop.property_type == "string":
                                        entity_props.append((_prop.property_name, _prop.property_name, _prop.property_name))
        return entity_props

    def on_update_property_selected_enum(self, context):
        self.node_properties.property_selected = self.property_selected_enum

    property_selected_enum : bpy.props.EnumProperty(items=get_entity_props, update=on_update_property_selected_enum) # type: ignore
    
    def check_source_node_name_changed(self):
        _source_node = None
        self.new_source_node_name = self.inputs[1].links[0].from_node.name
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.new_source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.new_source_node_name]
                break
        if _source_node:
            for _input in _source_node.inputs:
                if (_input.name + "_REF") == self.inputs[1].links[0].from_socket.name:
                    _source_node = _input.links[0].from_node
                    self.new_source_node_name = _source_node.name
                    break
                else:
                    pass
        return (self.node_properties.source_node_name != self.new_source_node_name)

    def init(self, context):
        self.inputs.new("B2G_Pipeline_SocketType", "Do")
        self.inputs.new("B2G_Player_SocketType", "Entity Ref")
        self.update()

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        if self.inputs[1].is_linked:
            row1 = layout.row()
            row1.prop(self, "property_selected_enum", text="Property")
            if self.property_selected_enum == "none":
                pass
            else:
                row3 = layout.row()
                row3.prop(self.node_properties, "operation_selected", text="Operation")
                if self.node_properties.operation_selected != "none":
                    row4 = layout.row()
                    row4.prop(self.node_properties, "operation_parameter", text="Parameter")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Change Entity String Property"

    def update(self):
        '''Called when node graph is changed'''
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.update_buttons)
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        pass
        '''Mark invalid links, must be called from a timer
        _input_go = self.inputs[0]
        for _link in _input_go.links:
            print(type(_link.from_socket).__name__)
            _valid_link = False
            if ((type(_link.from_socket).__name__ == "B2G_Pipeline_Socket") or (type(_link.from_socket).__name__ == "B2G_3dmenu_Socket")):
                _valid_link = True
            else:
                _valid_link = False
            _link.is_valid = _valid_link'''

    def socket_value_update(self, context):
        print("Socket value update")

    def update_buttons(self):
        if self.inputs[1].is_linked:
            if self.check_source_node_name_changed():
                self.node_properties.property_selected = "none"
                self.node_properties.property_selected_enum = "none"
                self.node_properties.source_node_name = self.new_source_node_name
        else:
            self.node_properties.source_node_name = ""
            self.node_properties.property_selected = "none"
            self.node_properties.property_selected_enum = "none"

    def update_sockets(self):
        if self.inputs[1].is_linked:
            if self.inputs[1].links[0].is_valid:
                self.inputs[1].name = self.inputs[1].links[0].from_socket.name
            else:
                self.inputs[1].name = "Not valid"
        else:
            self.property_selected_enum = "none"
            self.inputs[1].name = "Entity Ref"

class B2G_Change_Scene_String_Property_Node(MyCustomTreeNode, Node):
    bl_idname = 'B2G_Change_Scene_String_Property_NodeType'
    bl_label = "Change Scene String Property"
    bl_icon = 'LINENUMBERS_ON'
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=ChangeEntityStringPropertyNodeProperties) # type: ignore

    new_source_node_name : bpy.props.StringProperty(default="") # type: ignore
    
    def get_entity_props(self, context):
        entity_props = [
                ("none", "None", "NONE"),
        ]
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.node_properties.source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.node_properties.source_node_name]
                if hasattr(_source_node, "scene"):
                    for _prop in _source_node.scene.entity_properties:
                        if _prop.property_type == "string":
                            entity_props.append((_prop.property_name, _prop.property_name, _prop.property_name))
        return entity_props

    def on_update_property_selected_enum(self, context):
        self.node_properties.property_selected = self.property_selected_enum

    property_selected_enum : bpy.props.EnumProperty(items=get_entity_props, update=on_update_property_selected_enum) # type: ignore
    
    '''
    def on_update_property_selected(self, context):
        self.operation_selected = "none"
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.source_node_name]
                if hasattr(_source_node, "scene"):
                    for _prop in _source_node.scene.entity_properties:
                        if _prop.property_name == self.property_selected:
                            self.current_property_type = _prop.property_type
                            break
                else:
                    print("Has no scene attr", self.source_node.name)
    '''

    def check_source_node_name_changed(self):
        _source_node = None
        self.new_source_node_name = self.inputs[1].links[0].from_node.name
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.new_source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.new_source_node_name]
                break
        if _source_node:
            for _input in _source_node.inputs:
                if (_input.name + "_REF") == self.inputs[1].links[0].from_socket.name:
                    _source_node = _input.links[0].from_node
                    self.new_source_node_name = _source_node.name
                    break
                else:
                    pass
        return (self.node_properties.source_node_name != self.new_source_node_name)

    def init(self, context):
        self.inputs.new("B2G_Pipeline_SocketType", "Do")
        self.inputs.new("B2G_Player_SocketType", "Entity Ref")
        self.update()

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        if self.inputs[1].is_linked:
            row1 = layout.row()
            row1.prop(self, "property_selected_enum", text="Property")
            if self.property_selected_enum == "none":
                pass
            else:
                row3 = layout.row()
                row3.prop(self.node_properties, "operation_selected", text="Operation")
                if self.node_properties.operation_selected != "none":
                    row4 = layout.row()
                    row4.prop(self.node_properties, "operation_parameter", text="Parameter")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Change Scene String Property"

    def update(self):
        '''Called when node graph is changed'''
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.update_buttons)
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        pass
        '''Mark invalid links, must be called from a timer
        _input_go = self.inputs[0]
        for _link in _input_go.links:
            print(type(_link.from_socket).__name__)
            _valid_link = False
            if ((type(_link.from_socket).__name__ == "B2G_Pipeline_Socket") or (type(_link.from_socket).__name__ == "B2G_3dmenu_Socket")):
                _valid_link = True
            else:
                _valid_link = False
            _link.is_valid = _valid_link'''

    def socket_value_update(self, context):
        print("Socket value update")

    def update_buttons(self):
        if self.inputs[1].is_linked:
            if self.check_source_node_name_changed():
                self.node_properties.property_selected = "none"
                self.node_properties.property_selected_enum = "none"
                self.node_properties.source_node_name = self.new_source_node_name
        else:
            self.node_properties.source_node_name = ""
            self.node_properties.property_selected = "none"
            self.node_properties.property_selected_enum = "none"

    def update_sockets(self):
        if self.inputs[1].is_linked:
            if self.inputs[1].links[0].is_valid:
                self.inputs[1].name = self.inputs[1].links[0].from_socket.name
            else:
                self.inputs[1].name = "Not valid"
        else:
            self.inputs[1].name = "Scene Ref"

class B2G_Change_Entity_Integer_Property_Node(MyCustomTreeNode, Node):
    bl_idname = 'B2G_Change_Entity_Integer_Property_NodeType'
    bl_label = "Change Entity Integer Property"
    bl_icon = 'LINENUMBERS_ON'
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=ChangeEntityIntegerPropertyNodeProperties) # type: ignore
    #source_node_name : bpy.props.StringProperty(default="") # type: ignore
    new_source_node_name : bpy.props.StringProperty(default="") # type: ignore
    
    def get_entity_props(self, context):
        entity_props = [
                ("none", "None", "NONE"),
        ]
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.node_properties.source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.node_properties.source_node_name]
                if hasattr(_source_node, "scene"):
                    for _prop in _source_node.scene.entity_properties:
                        if _prop.property_type == "integer":
                            entity_props.append((_prop.property_name, _prop.property_name, _prop.property_name))
        return entity_props

    def on_update_property_selected_enum(self, context):
        self.node_properties.property_selected = self.property_selected_enum

    property_selected_enum : bpy.props.EnumProperty(items=get_entity_props, update=on_update_property_selected_enum) # type: ignore
    #operation_selected : bpy.props.EnumProperty(items=integer_operations) # type: ignore

    def on_update_property_selected(self, context):
        self.node_properties.operation_selected = "none"
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.node_properties.source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.node_properties.source_node_name]
                if hasattr(_source_node, "scene"):
                    for _prop in _source_node.scene.entity_properties:
                        if _prop.property_name == self.node_properties.property_selected:
                            self.current_property_type = _prop.property_type
                            '''
                            if len(self.inputs) < 3:
                                self.inputs.new(property_node_sockets[self.current_property_type], "Param")
                            else:
                                self.inputs.remove(self.inputs[2])
                                self.inputs.new(property_node_sockets[self.current_property_type], "Param")
                            '''
                            break
                else:
                    pass
                    #print("Has no scene attr", self.source_node.name)

    #property_selected : bpy.props.EnumProperty(items=get_entity_props, update=on_update_property_selected) # type: ignore

    #operation_parameter : bpy.props.IntProperty(default=0) # type: ignore
    
    def check_source_node_name_changed(self):
        _source_node = None
        self.new_source_node_name = self.inputs[1].links[0].from_node.name
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.new_source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.new_source_node_name]
                break
        if _source_node:
            for _input in _source_node.inputs:
                if (_input.name + "_REF") == self.inputs[1].links[0].from_socket.name:
                    _source_node = _input.links[0].from_node
                    self.new_source_node_name = _source_node.name
                    break
                else:
                    pass
        return (self.node_properties.source_node_name != self.new_source_node_name)

    def init(self, context):
        self.inputs.new("B2G_Pipeline_SocketType", "Do")
        self.inputs.new("B2G_Player_SocketType", "Entity Ref")
        self.update()

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        if self.inputs[1].is_linked:
            row1 = layout.row()
            row1.prop(self, "property_selected_enum", text="Property")
            if self.node_properties.property_selected == "none":
                pass
            else:
                for _node in bpy.data.node_groups["GameManager"].nodes:
                    if _node.name == self.node_properties.source_node_name:
                        _source_node = bpy.data.node_groups["GameManager"].nodes[self.node_properties.source_node_name]
                        if hasattr(_source_node, "scene"):
                            for _prop in _source_node.scene.entity_properties:
                                if _prop.property_name == self.node_properties.property_selected:
                                    row3 = layout.row()
                                    row3.prop(self.node_properties, "operation_selected", text="Operation")
                                    if self.node_properties.operation_selected != "none":
                                        row4 = layout.row()
                                        row4.prop(self.node_properties, "operation_parameter", text="Parameter")
                                    break

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Change Entity Integer Property"

    def update(self):
        '''Called when node graph is changed'''
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.update_buttons)
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        pass
        '''Mark invalid links, must be called from a timer
        _input_go = self.inputs[0]
        for _link in _input_go.links:
            print(type(_link.from_socket).__name__)
            _valid_link = False
            if ((type(_link.from_socket).__name__ == "B2G_Pipeline_Socket") or (type(_link.from_socket).__name__ == "B2G_3dmenu_Socket")):
                _valid_link = True
            else:
                _valid_link = False
            _link.is_valid = _valid_link'''

    def socket_value_update(self, context): # Doesn't work
        print("Socket value update")
    
    def update_buttons(self):
        if self.inputs[1].is_linked:
            if self.check_source_node_name_changed():
                self.node_properties.property_selected = "none"
                self.node_properties.source_node_name = self.new_source_node_name
        else:
            self.node_properties.source_node_name = ""
            self.node_properties.property_selected = "none"

    def update_sockets(self):
        if self.inputs[1].is_linked:
            if self.inputs[1].links[0].is_valid:
                self.inputs[1].name = self.inputs[1].links[0].from_socket.name
            else:
                self.inputs[1].name = "Not valid"
        else:
            self.inputs[1].name = "Entity Ref"

class B2G_Change_Entity_Float_Property_Node(MyCustomTreeNode, Node):
    bl_idname = 'B2G_Change_Entity_Float_Property_NodeType'
    bl_label = "Change Entity Float Property"
    bl_icon = 'LINENUMBERS_ON'
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=ChangeEntityFloatPropertyNodeProperties) # type: ignore
    #source_node_name : bpy.props.StringProperty(default="") # type: ignore
    new_source_node_name : bpy.props.StringProperty(default="") # type: ignore
    
    def get_entity_props(self, context):
        entity_props = [
                ("none", "None", "NONE"),
        ]
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.node_properties.source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.node_properties.source_node_name]
                if hasattr(_source_node, "scene"):
                    for _prop in _source_node.scene.entity_properties:
                        if _prop.property_type == "float":
                            entity_props.append((_prop.property_name, _prop.property_name, _prop.property_name))
        return entity_props

    def on_update_property_selected_enum(self, context):
        self.node_properties.property_selected = self.property_selected_enum

    #operation_selected : bpy.props.EnumProperty(items=integer_operations) # type: ignore
    property_selected_enum : bpy.props.EnumProperty(items=get_entity_props, update=on_update_property_selected_enum) # type: ignore

    def on_update_property_selected(self, context):
        self.node_properties.operation_selected = "none"
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.node_properties.source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.node_properties.source_node_name]
                if hasattr(_source_node, "scene"):
                    for _prop in _source_node.scene.entity_properties:
                        if _prop.property_name == self.node_properties.property_selected:
                            self.current_property_type = _prop.property_type
                            '''
                            if len(self.inputs) < 3:
                                self.inputs.new(property_node_sockets[self.current_property_type], "Param")
                            else:
                                self.inputs.remove(self.inputs[2])
                                self.inputs.new(property_node_sockets[self.current_property_type], "Param")
                            '''
                            break
                else:
                    pass
                    #print("Has no scene attr", self.source_node.name)

    #property_selected : bpy.props.EnumProperty(items=get_entity_props, update=on_update_property_selected) # type: ignore

    #operation_parameter : bpy.props.FloatProperty(default=0.0) # type: ignore

    ''' for v0.3
    execution_behavior : bpy.props.EnumProperty(items=execution_behaviors, default="once") # type: ignore
    execution_parameter : bpy.props.FloatProperty(default=1.0, min=0.01) # type: ignore
    '''

    def check_source_node_name_changed(self):
        _source_node = None
        self.new_source_node_name = self.inputs[1].links[0].from_node.name
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.new_source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.new_source_node_name]
                break
        if _source_node:
            for _input in _source_node.inputs:
                if (_input.name + "_REF") == self.inputs[1].links[0].from_socket.name:
                    _source_node = _input.links[0].from_node
                    self.new_source_node_name = _source_node.name
                    break
                else:
                    pass
        return (self.node_properties.source_node_name != self.new_source_node_name)

    def init(self, context):
        self.inputs.new("B2G_Pipeline_SocketType", "Do")
        self.inputs.new("B2G_Player_SocketType", "Entity Ref")
        self.update()

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        if self.inputs[1].is_linked:
            row1 = layout.row()
            row1.prop(self, "property_selected_enum", text="Property")
            if self.node_properties.property_selected == "none":
                pass
            else:
                for _node in bpy.data.node_groups["GameManager"].nodes:
                    if _node.name == self.node_properties.source_node_name:
                        _source_node = bpy.data.node_groups["GameManager"].nodes[self.node_properties.source_node_name]
                        if hasattr(_source_node, "scene"):
                            for _prop in _source_node.scene.entity_properties:
                                if _prop.property_name == self.node_properties.property_selected:
                                    row3 = layout.row()
                                    row3.prop(self.node_properties, "operation_selected", text="Operation")
                                    if self.node_properties.operation_selected != "none":
                                        row4 = layout.row()
                                        row4.prop(self.node_properties, "operation_parameter", text="Parameter")
                                    break
            ''' for v0.3
            row2 = layout.row()
            row2.prop(self, "execution_behavior", text="Execution")
            if self.execution_behavior == "always":
                row5 = layout.row()
                row5.prop(self, "execution_parameter", text="Cadence")
            '''

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Change Entity Float Property"

    def update(self):
        '''Called when node graph is changed'''
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.update_buttons)
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        pass
        '''Mark invalid links, must be called from a timer
        _input_go = self.inputs[0]
        for _link in _input_go.links:
            print(type(_link.from_socket).__name__)
            _valid_link = False
            if ((type(_link.from_socket).__name__ == "B2G_Pipeline_Socket") or (type(_link.from_socket).__name__ == "B2G_3dmenu_Socket")):
                _valid_link = True
            else:
                _valid_link = False
            _link.is_valid = _valid_link'''

    def socket_value_update(self, context): # Doesn't work
        print("Socket value update")
    
    def update_buttons(self):
        if self.inputs[1].is_linked:
            if self.check_source_node_name_changed():
                self.node_properties.property_selected = "none"
                self.node_properties.source_node_name = self.new_source_node_name
        else:
            self.node_properties.source_node_name = ""
            self.node_properties.property_selected = "none"

    def update_sockets(self):
        if self.inputs[1].is_linked:
            if self.inputs[1].links[0].is_valid:
                self.inputs[1].name = self.inputs[1].links[0].from_socket.name
            else:
                self.inputs[1].name = "Not valid"
        else:
            self.inputs[1].name = "Entity Ref"

class B2G_Change_Entity_Boolean_Property_Node(MyCustomTreeNode, Node):
    bl_idname = 'B2G_Change_Entity_Boolean_Property_NodeType'
    bl_label = "Change Entity Boolean Property"
    bl_icon = 'LINENUMBERS_ON'
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=ChangeEntityBoolPropertyNodeProperties) # type: ignore

    #source_node_name : bpy.props.StringProperty(default="") # type: ignore
    new_source_node_name : bpy.props.StringProperty(default="") # type: ignore
    
    def get_entity_props(self, context):
        entity_props = [
                ("none", "None", "NONE"),
        ]
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.node_properties.source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.node_properties.source_node_name]
                if hasattr(_source_node, "scene"):
                    for _prop in _source_node.scene.entity_properties:
                        if _prop.property_type == "boolean":
                            entity_props.append((_prop.property_name, _prop.property_name, _prop.property_name))
        return entity_props

    def on_update_property_selected_enum(self, context):
        self.node_properties.property_selected = self.property_selected_enum

    property_selected_enum : bpy.props.EnumProperty(items=get_entity_props, update=on_update_property_selected_enum) # type: ignore
    #operation_selected : bpy.props.EnumProperty(items=integer_operations) # type: ignore

    def on_update_property_selected(self, context):
        self.node_properties.operation_selected = "none"
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.node_properties.source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.node_properties.source_node_name]
                if hasattr(_source_node, "scene"):
                    for _prop in _source_node.scene.entity_properties:
                        if _prop.property_name == self.node_properties.property_selected:
                            self.current_property_type = _prop.property_type
                            break
                else:
                    pass
                    #print("Has no scene attr", self.source_node.name)

    #property_selected : bpy.props.EnumProperty(items=get_entity_props, update=on_update_property_selected) # type: ignore

    #operation_parameter : bpy.props.BoolProperty(default=False) # type: ignore
    
    def check_source_node_name_changed(self):
        _source_node = None
        self.new_source_node_name = self.inputs[1].links[0].from_node.name
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.new_source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.new_source_node_name]
                break
        if _source_node:
            for _input in _source_node.inputs:
                if (_input.name + "_REF") == self.inputs[1].links[0].from_socket.name:
                    _source_node = _input.links[0].from_node
                    self.new_source_node_name = _source_node.name
                    break
                else:
                    pass
        return (self.node_properties.source_node_name != self.new_source_node_name)

    def init(self, context):
        self.inputs.new("B2G_Pipeline_SocketType", "Do")
        self.inputs.new("B2G_Player_SocketType", "Entity Ref")
        self.update()

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        if self.inputs[1].is_linked:
            row1 = layout.row()
            row1.prop(self, "property_selected_enum", text="Property")
            if self.node_properties.property_selected == "none":
                pass
            else:
                for _node in bpy.data.node_groups["GameManager"].nodes:
                    if _node.name == self.node_properties.source_node_name:
                        _source_node = bpy.data.node_groups["GameManager"].nodes[self.node_properties.source_node_name]
                        if hasattr(_source_node, "scene"):
                            for _prop in _source_node.scene.entity_properties:
                                if _prop.property_name == self.node_properties.property_selected:
                                    row3 = layout.row()
                                    row3.prop(self.node_properties, "operation_selected", text="Operation")
                                    if self.node_properties.operation_selected != "none":
                                        row4 = layout.row()
                                        row4.prop(self.node_properties, "operation_parameter", text="Parameter")
                                    break

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Change Entity Boolean Property"

    def update(self):
        '''Called when node graph is changed'''
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.update_buttons)
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        pass
        '''Mark invalid links, must be called from a timer
        _input_go = self.inputs[0]
        for _link in _input_go.links:
            print(type(_link.from_socket).__name__)
            _valid_link = False
            if ((type(_link.from_socket).__name__ == "B2G_Pipeline_Socket") or (type(_link.from_socket).__name__ == "B2G_3dmenu_Socket")):
                _valid_link = True
            else:
                _valid_link = False
            _link.is_valid = _valid_link'''

    def socket_value_update(self, context): # Doesn't work
        print("Socket value update")
    
    def update_buttons(self):
        if self.inputs[1].is_linked:
            if self.check_source_node_name_changed():
                self.node_properties.property_selected = "none"
                self.node_properties.source_node_name = self.new_source_node_name
        else:
            self.node_properties.source_node_name = ""
            self.node_properties.property_selected = "none"

    def update_sockets(self):
        if self.inputs[1].is_linked:
            if self.inputs[1].links[0].is_valid:
                self.inputs[1].name = self.inputs[1].links[0].from_socket.name
            else:
                self.inputs[1].name = "Not valid"
        else:
            self.inputs[1].name = "Entity Ref"

class B2G_Play_Entity_Animation_Node(MyCustomTreeNode, Node):
    bl_idname = 'B2G_Play_Entity_Animation_NodeType'
    bl_label = "Play Entity Animation"
    bl_icon = "ARMATURE_DATA"
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=PlayEntityAnimationNodeProperties) # type: ignore
    new_source_node_name : bpy.props.StringProperty(default="") # type: ignore

    def get_entity_animations(self, context):
        #print("Updating animations")
        entity_animations = [
                ("none", "None", "NONE", 0),
        ]
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.node_properties.source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.node_properties.source_node_name]
                if hasattr(_source_node, "scene"):
                    for _entity in _source_node.scene.objects:
                        if len(self.inputs[1].links) > 0:
                            _socket_name = self.inputs[1].links[0].from_socket.name
                            if (_entity.name + "_REF") == _socket_name:
                                if _entity.object_type == "entity":
                                    _anim_data = _entity.animation_data
                                    _index = 1
                                    #print("Anims of", _entity.name)
                                    for _object_action in _anim_data.nla_tracks:
                                        #print("NLA:", _object_action)
                                        entity_animations.append((_object_action.name, _object_action.name, _object_action.name, _index))
                                        _index += 1
        return entity_animations
    
    def on_update_animation_selected(self, context):
        if self.node_properties.animation_selected != self.animation_selected_enum:
            self.node_properties.animation_selected = self.animation_selected_enum
        self.node_properties.operation_selected = "none"

    animation_selected_enum : bpy.props.EnumProperty(items=get_entity_animations, update=on_update_animation_selected)#, set=on_set_animation_selected)#, get=on_get_animation_selected) # type: ignore
   
    def check_source_node_name_changed(self):
        _source_node = None
        self.new_source_node_name = self.inputs[1].links[0].from_node.name
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.new_source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.new_source_node_name]
                break
        return (self.node_properties.source_node_name != self.new_source_node_name)

    def init(self, context):
        self.inputs.new("B2G_Pipeline_SocketType", "Do")
        self.inputs.new("B2G_Player_SocketType", "Entity Ref")
        self.update()

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        if self.inputs[1].is_linked:
            if len(self.get_entity_animations(context)) > 1:
                row1 = layout.row()
                row1.prop(self, "animation_selected_enum", text="Animation")
                if self.node_properties.animation_selected == "none":
                    pass
                else:
                    row3 = layout.row()
                    row3.prop(self.node_properties, "operation_selected", text="Repro.")
                    if self.node_properties.operation_selected != "none":
                        row4 = layout.row()
                        row4.prop(self.node_properties, "operation_parameter", text="Speed")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Play Entity Animation"

    def update(self):
        '''Called when node graph is changed'''
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.update_buttons)
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        pass
        '''Mark invalid links, must be called from a timer
        _input_go = self.inputs[0]
        for _link in _input_go.links:
            print(type(_link.from_socket).__name__)
            _valid_link = False
            if ((type(_link.from_socket).__name__ == "B2G_Pipeline_Socket") or (type(_link.from_socket).__name__ == "B2G_3dmenu_Socket")):
                _valid_link = True
            else:
                _valid_link = False
            _link.is_valid = _valid_link'''
   
    def update_buttons(self):
        if self.inputs[1].is_linked:
            if self.check_source_node_name_changed():
                self.node_properties.animation_selected = "none"
                self.animation_selected_enum = "none"
                self.node_properties.property_selected = "none"
                self.node_properties.source_node_name = self.new_source_node_name
                for _node in bpy.data.node_groups["GameManager"].nodes:
                    if _node.name == self.node_properties.source_node_name:
                        _source_node = bpy.data.node_groups["GameManager"].nodes[self.node_properties.source_node_name]
                        if hasattr(_source_node, "scene"):
                            for _entity in _source_node.scene.objects:
                                if len(self.inputs[1].links) > 0:
                                    _socket_name = self.inputs[1].links[0].from_socket.name
                                    if (_entity.name + "_REF") == _socket_name:
                                        self.entity_name = _entity.name
        else:
            self.node_properties.source_node_name = ""
            self.node_properties.animation_selected = "none"
            self.node_properties.property_selected = "none"
            self.node_properties.entity_name = ""

    def update_sockets(self):
        if self.inputs[1].is_linked:
            if self.inputs[1].links[0].is_valid:
                self.inputs[1].name = self.inputs[1].links[0].from_socket.name
            else:
                self.inputs[1].name = "Not valid"
        else:
            self.inputs[1].name = "Entity Ref"

class B2G_Trigger_Action_Node(MyCustomTreeNode, Node):
    bl_idname = 'B2G_Trigger_Action_NodeType'
    bl_label = "Get Trigger"
    bl_icon = "ARMATURE_DATA"
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=TriggerActionNodeProperties) # type: ignore
    new_source_node_name : bpy.props.StringProperty(default="") # type: ignore

    def check_source_node_name_changed(self):
        _source_node = None
        self.new_source_node_name = self.inputs[0].links[0].from_node.name
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.new_source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.new_source_node_name]
                break
        if _source_node:
            for _input in _source_node.inputs:
                if (_input.name + "_REF") == self.inputs[0].links[0].from_socket.name:
                    _source_node = _input.links[0].from_node
                    self.new_source_node_name = _source_node.name
                    break
                else:
                    pass
        return (self.node_properties.source_node_name != self.new_source_node_name)

    def get_stage_triggers(self, context):
        _triggers = [
            ("none", "None", "NONE", 0),
        ]
        if len(self.inputs[0].links) > 0:
            _source_node = self.inputs[0].links[0].from_node
            _from_socket_name = self.inputs[0].links[0].from_socket.name
            if _from_socket_name == "Stage_REF":
                pass
            else:
                _source_node = _source_node.inputs[_source_node.inputs.find(_from_socket_name.rstrip("_REF"))].links[0].from_node
            _source_scene = _source_node.scene
            if _source_scene:
                for _index,_scene_object in enumerate(_source_scene.objects):
                    if _scene_object.object_type == "trigger_zone":
                        _triggers.append((_scene_object.name, _scene_object.name, _scene_object.name, _index+1))
        return _triggers

    def on_stage_trigger_update(self, context):
        self.node_properties.trigger_name = self.stage_triggers
        self.outputs.clear()
        if self.stage_triggers == "none":
            pass
        else:
            self.outputs.new("B2G_Pipeline_SocketType", "OnEnter")
            self.outputs.new("B2G_Pipeline_SocketType", "OnStay")
            self.outputs.new("B2G_Pipeline_SocketType", "OnExit")

    stage_triggers : bpy.props.EnumProperty(items=get_stage_triggers, update=on_stage_trigger_update) # type: ignore
    
    def init(self, context):
        self.inputs.new("B2G_Player_SocketType", "Stage_REF")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        if self.inputs[0].is_linked:
            layout.prop(self, "stage_triggers", text="Trigger")
            #layout.prop(self, "trigger_condition", text="")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Get Trigger"

    def update(self):
        '''Called when node graph is changed'''
        bpy.app.timers.register(self.mark_invalid_links)
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.update_buttons)

    def mark_invalid_links(self):
        for _link in self.inputs[0].links:
            #print("updating links")
            _link.is_valid = (type(_link.from_socket).__name__ == "B2G_Player_Socket")
   
    def update_buttons(self):
        if self.inputs[0].is_linked:
            if self.check_source_node_name_changed():
                self.node_properties.source_node_name = self.new_source_node_name
                self.stage_triggers = "none"
        else:
            self.node_properties.source_node_name = ""
            self.outputs.clear()
            self.node_properties.trigger_name = ""
            self.stage_triggers = "none"

    def update_sockets(self):
        if self.inputs[0].is_linked:
            if self.check_source_node_name_changed():
                self.inputs[0].name = self.inputs[0].links[0].from_socket.name
        else:
            self.inputs[0].name = "Stage_REF"
            self.outputs.clear()
            self.stage_triggers = "none"

class B2G_Get_Scene_Entity_Node(MyCustomTreeNode, Node):
    bl_idname = 'B2G_Get_Scene_Entity_NodeType'
    bl_label = "Get Entity"
    bl_icon = "ARMATURE_DATA"
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=GetSceneEntityNodeProperties) # type: ignore
    new_source_node_name : bpy.props.StringProperty(default="") # type: ignore

    def check_source_node_name_changed(self):
        _source_node = None
        self.new_source_node_name = self.inputs[0].links[0].from_node.name
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.new_source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.new_source_node_name]
                break
        if _source_node:
            for _input in _source_node.inputs:
                if (_input.name + "_REF") == self.inputs[0].links[0].from_socket.name:
                    _source_node = _input.links[0].from_node
                    self.new_source_node_name = _source_node.name
                    break
                else:
                    pass
        return (self.node_properties.source_node_name != self.new_source_node_name)

    def get_scene_entities(self, context):
        _entities = [
            ("none", "None", "NONE", 0),
        ]
        if len(self.inputs[0].links) > 0:
            _from_socket = self.inputs[0].links[0].from_socket
            _source_node = None
            _source_scene = None
            if _from_socket.name == "Stage_REF":
                _source_node = self.inputs[0].links[0].from_node
                _source_scene = _source_node.scene
            else:
                _resource_socket_index = _from_socket.node.inputs.find(_from_socket.name.rstrip("_REF"))
                _source_node = _from_socket.node.inputs[_resource_socket_index].links[0].from_node
                _source_scene = _source_node.scene
            if _source_scene:
                for _index,_scene_object in enumerate(_source_scene.objects):
                    if _scene_object.object_type == "entity":
                        _entities.append((_scene_object.name, _scene_object.name, _scene_object.name, _index+1))
        return _entities

    def on_scene_entities_update(self, context):
        self.node_properties.entity_name = self.scene_entities
        self.inputs[0].name = self.inputs[0].links[0].from_socket.name
        self.outputs.clear()
        if self.scene_entities != "none":
            _output_name = self.node_properties.entity_name + "_REF"
            self.outputs.new("B2G_Player_SocketType", _output_name)

    scene_entities : bpy.props.EnumProperty(items=get_scene_entities, update=on_scene_entities_update) # type: ignore
    
    def init(self, context):
        self.inputs.new("B2G_Player_SocketType", "Stage_REF")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        if self.inputs[0].is_linked:
            layout.prop(self, "scene_entities", text="Entity")
            #layout.prop(self, "trigger_condition", text="")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Get Entity"

    def update(self):
        '''Called when node graph is changed'''
        bpy.app.timers.register(self.mark_invalid_links)
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.update_buttons)

    def mark_invalid_links(self):
        for _link in self.inputs[0].links:
            #print("updating links")
            _link.is_valid = (type(_link.from_socket).__name__ == "B2G_Player_Socket")
   
    def update_buttons(self):
        if self.inputs[0].is_linked:
            if self.check_source_node_name_changed():
                #self.node_properties.property_selected = "none"
                self.node_properties.source_node_name = self.new_source_node_name
        else:
            self.node_properties.source_node_name = ""
            self.outputs.clear()
            #self.node_properties.property_selected = "none"

    def update_sockets(self):
        if self.inputs[0].is_linked:
            if self.check_source_node_name_changed():
                self.inputs[0].name = self.inputs[0].links[0].from_socket.name
                self.outputs.clear()
                _output_name = self.node_properties.entity_name + "_REF"
                self.outputs.new("B2G_Player_SocketType", _output_name)
        else:
            self.inputs[0].name = "_REF"
            self.outputs.clear()

class B2G_Get_Entity_Property_Node(MyCustomTreeNode, Node):
    bl_idname = 'B2G_Get_Entity_Property_NodeType'
    bl_label = "Get Property"
    bl_icon = "ARMATURE_DATA"
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=GetEntityPropertiesNodeProperties) # type: ignore
    new_source_node_name : bpy.props.StringProperty(default="") # type: ignore

    def check_source_node_name_changed(self):
        _source_node = None
        self.new_source_node_name = self.inputs[0].links[0].from_node.name
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.new_source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.new_source_node_name]
                break
        if _source_node:
            for _input in _source_node.inputs:
                if (_input.name + "_REF") == self.inputs[0].links[0].from_socket.name:
                    _source_node = _input.links[0].from_node
                    self.new_source_node_name = _source_node.name
                    break
                else:
                    pass
        return (self.node_properties.source_node_name != self.new_source_node_name)

    def get_entity_properties(self, context):
        _properties = [
            ("none", "None", "NONE", 0),
        ]
        if len(self.inputs[0].links) > 0:
            _source_node = self.inputs[0].links[0].from_node
            _from_socket = self.inputs[0].links[0].from_socket
            match type(_source_node).__name__:
                case "B2G_Stage_Scene_Node":
                    if _from_socket.name == "Stage_REF":
                        if len(_source_node.scene.entity_properties) > 0:
                            for _index,_scene_property in enumerate(_source_node.scene.entity_properties):
                                _properties.append((_scene_property.property_name, _scene_property.property_name, _scene_property.property_name, _index+1))
                    else:
                        for _source_socket in _source_node.inputs:
                            if _source_socket.name == _from_socket.name.rstrip("_REF"):
                                _source_source_node = _source_socket.links[0].from_node
                                _source_scene = _source_source_node.scene
                                if len(_source_scene.entity_properties) > 0:
                                    for _index,_scene_property in enumerate(_source_scene.entity_properties):
                                        _properties.append((_scene_property.property_name, _scene_property.property_name, _scene_property.property_name, _index+1))
                                break
                case "B2G_Get_Scene_Entity_Node":
                    _resource_node = _source_node.inputs[0].links[0].from_node
                    _refrom_socket = _source_node.inputs[0].links[0].from_socket
                    if _refrom_socket.name == "Stage_REF":
                        pass
                    else:
                        _resource_node = _resource_node.inputs[_resource_node.inputs.find(_refrom_socket.name.rstrip("_REF"))].links[0].from_node
                    for _scene_object in _resource_node.scene.objects:
                        if _scene_object.name == _source_node.scene_entities:
                            if len(_scene_object.entity_properties) > 0:
                                for _index,_scene_property in enumerate(_scene_object.entity_properties):
                                    _properties.append((_scene_property.property_name, _scene_property.property_name, _scene_property.property_name, _index+1))
        return _properties

    def on_entity_properties_update(self, context):
        self.node_properties.property_name = self.entity_properties
        self.outputs.clear()
        if self.entity_properties == "none":
            pass
        else:
            _output_name = self.node_properties.property_name + "_REF"
            self.outputs.new("B2G_Player_SocketType", _output_name)

    entity_properties : bpy.props.EnumProperty(items=get_entity_properties, update=on_entity_properties_update) # type: ignore
    
    def init(self, context):
        self.inputs.new("B2G_Player_SocketType", "Stage_REF")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        if self.inputs[0].is_linked:
            layout.prop(self, "entity_properties", text="Props")
            #layout.prop(self, "trigger_condition", text="")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Get Property"

    def update(self):
        '''Called when node graph is changed'''
        bpy.app.timers.register(self.mark_invalid_links)
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.update_buttons)

    def mark_invalid_links(self):
        for _link in self.inputs[0].links:
            #print("updating links")
            _link.is_valid = (type(_link.from_socket).__name__ == "B2G_Player_Socket")
   
    def update_buttons(self):
        if self.inputs[0].is_linked:
            if self.check_source_node_name_changed():
                #self.node_properties.property_selected = "none"
                self.node_properties.source_node_name = self.new_source_node_name
        else:
            self.node_properties.source_node_name = ""
            self.outputs.clear()
            #self.node_properties.property_selected = "none"

    def update_sockets(self):
        if self.inputs[0].is_linked:
            if self.check_source_node_name_changed():
                self.inputs[0].name = self.inputs[0].links[0].from_socket.name
                self.outputs.clear()
        else:
            self.entity_properties = "none"
            self.inputs[0].name = "_REF"
            self.outputs.clear()
            self.node_properties.source_node_name = ""

class B2G_Get_HUD_Content_Node(MyCustomTreeNode, Node):
    bl_idname = 'B2G_Get_HUD_Content_NodeType'
    bl_label = "Get Content"
    bl_icon = "ARMATURE_DATA"
    bl_width_default = 200.0
    bl_height_default = 100.0

    node_properties : bpy.props.PointerProperty(type=GetHUDContentNodeProperties) # type: ignore
    new_source_node_name : bpy.props.StringProperty(default="") # type: ignore

    def check_source_node_name_changed(self):
        _source_node = None
        self.new_source_node_name = self.inputs[0].links[0].from_node.name
        for _node in bpy.data.node_groups["GameManager"].nodes:
            if _node.name == self.new_source_node_name:
                _source_node = bpy.data.node_groups["GameManager"].nodes[self.new_source_node_name]
                break
        if _source_node:
            for _input in _source_node.inputs:
                if (_input.name + "_REF") == self.inputs[0].links[0].from_socket.name:
                    _source_node = _input.links[0].from_node
                    self.new_source_node_name = _source_node.name
                    break
                else:
                    pass
        return (self.node_properties.source_node_name != self.new_source_node_name)

    def get_hud_contents(self, context):
        _contents = [
            ("none", "None", "NONE", 0),
        ]
        if len(self.inputs[0].links) > 0:
            _source_node = self.inputs[0].links[0].from_node
            _resource_node = _source_node.inputs[_source_node.inputs.find("HUD")].links[0].from_node
            for _index,_scene_object in enumerate(_resource_node.scene.objects):
                if hasattr(_scene_object, "hud_element_properties"):
                    if _scene_object.hud_element_properties.element_type == "text_content":
                        _contents.append((_scene_object.name, _scene_object.name, _scene_object.name, _index+1))
        return _contents

    def on_hud_contents_update(self, context):
        self.node_properties.content_name = self.hud_contents
        self.outputs.clear()
        if self.hud_contents == "none":
            pass
        else:
            _output_name = self.node_properties.content_name + "_REF"
            self.outputs.new("B2G_Player_SocketType", _output_name)

    hud_contents : bpy.props.EnumProperty(items=get_hud_contents, update=on_hud_contents_update) # type: ignore
    
    def init(self, context):
        self.inputs.new("B2G_Player_SocketType", "Stage_REF")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        if self.inputs[0].is_linked:
            layout.prop(self, "hud_contents", text="HUD Contents")
            #layout.prop(self, "trigger_condition", text="")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Get Content"

    def update(self):
        '''Called when node graph is changed'''
        bpy.app.timers.register(self.mark_invalid_links)
        bpy.app.timers.register(self.update_sockets)
        bpy.app.timers.register(self.update_buttons)

    def mark_invalid_links(self):
        for _link in self.inputs[0].links:
            #print("updating links")
            _link.is_valid = (type(_link.from_socket).__name__ == "B2G_Player_Socket")
   
    def update_buttons(self):
        if self.inputs[0].is_linked:
            if self.check_source_node_name_changed():
                #self.node_properties.property_selected = "none"
                self.node_properties.source_node_name = self.new_source_node_name
        else:
            self.node_properties.source_node_name = ""
            self.outputs.clear()
            #self.node_properties.property_selected = "none"

    def update_sockets(self):
        if self.inputs[0].is_linked:
            if self.check_source_node_name_changed():
                self.inputs[0].name = self.inputs[0].links[0].from_socket.name
                self.outputs.clear()
        else:
            self.entity_properties = "none"
            self.inputs[0].name = "_REF"
            self.outputs.clear()
            self.node_properties.source_node_name = ""


# --- END ACTION NODES ---


### Node Categories ###
# Node categories are a python system for automatically
# extending the Add menu, toolbar panels and search operator.
# For more examples see scripts/startup/nodeitems_builtins.py

import nodeitems_utils
from nodeitems_utils import NodeCategory, NodeItem

# our own base class with an appropriate poll function,
# so the categories only show up in our own tree type


class MyNodeCategory(NodeCategory):
    @classmethod
    def poll(cls, context):
        return context.space_data.tree_type == 'GameManagerTreeType'


# all categories in a list
node_categories = [
    MyNodeCategory('SCENES', "Scene", items=[
        NodeItem("B2G_Stage_Scene_NodeType"),
        NodeItem("B2G_Player_Scene_NodeType"),
        NodeItem("B2G_HUD_Scene_NodeType"),
        NodeItem("B2G_2dMenu_Scene_NodeType"),
        NodeItem("B2G_3dMenu_Scene_NodeType"),
        NodeItem("B2G_OverlayMenu_Scene_NodeType"),
        NodeItem("B2G_NPC_Scene_NodeType"),
    ]),
    MyNodeCategory('MATH', "Math", items=[
        #NodeItem("FunctionNodeBooleanMath"),
    ]),
    MyNodeCategory('SCENE_ACTIONS', "Scene Actions", items=[
        NodeItem("B2G_Change_Scene_String_Property_NodeType"),
        NodeItem("B2G_Get_Scene_Entity_NodeType"),
        NodeItem("B2G_Trigger_Action_NodeType"),
        NodeItem("B2G_Get_HUD_Content_NodeType"),
    ]),
    MyNodeCategory('ENTITY_ACTIONS', "Entity Actions", items=[
        NodeItem("B2G_Change_Entity_String_Property_NodeType"),
        NodeItem("B2G_Change_Entity_Integer_Property_NodeType"),
        NodeItem("B2G_Change_Entity_Float_Property_NodeType"),
        NodeItem("B2G_Change_Entity_Boolean_Property_NodeType"),
        NodeItem("B2G_Play_Entity_Animation_NodeType"),
        NodeItem("B2G_Get_Entity_Property_NodeType"),
    ]),
    MyNodeCategory('VARIABLES', "Variables", items=[
        NodeItem("B2G_String_NodeType"),
        NodeItem("B2G_Float_NodeType"),
        NodeItem("B2G_Integer_NodeType"),
        NodeItem("B2G_Boolean_NodeType"),
    ]),
    MyNodeCategory('PIPELINE', "Pipeline", items=[
        NodeItem("B2G_Start_NodeType"),
        NodeItem("B2G_Finish_NodeType"),
    ]),
    #'''
    MyNodeCategory('OTHERNODES', "Other", items=[
        # the node item can have additional settings,
        # which are applied to new nodes
        # NOTE: settings values are stored as string expressions,
        # for this reason they should be converted to strings using repr()
        NodeItem("CustomNodeType", label="Node A", settings={
            "my_string_prop": repr("Lorem ipsum dolor sit amet"),
            "my_float_prop": repr(1.0),
        }),
        NodeItem("CustomNodeType", label="Node B", settings={
            "my_string_prop": repr("consectetur adipisicing elit"),
            "my_float_prop": repr(2.0),
        }),
    ]),
    #'''
]

classes = (
    ButtonAction,
    OverlayButtonAction,
    ActionProperty,
    #HudSettings,
    #PlayerEntityProperty,
    StageObject,
    ChangeEntityStringPropertyNodeProperties,
    ChangeEntityBoolPropertyNodeProperties,
    ChangeEntityIntegerPropertyNodeProperties,
    ChangeEntityFloatPropertyNodeProperties,
    ValueNodeProperties,
    GetSceneEntityNodeProperties,
    GetEntityPropertiesNodeProperties,
    GetHUDContentNodeProperties,
    PlayEntityAnimationNodeProperties,
    StageSceneNodeProperties,
    TriggerActionNodeProperties,
    PlayerSceneNodeProperties,
    Menu2dSceneNodeProperties,
    Menu3dSceneNodeProperties,
    HUDSceneNodeProperties,
    OverlaySceneNodeProperties,
    GameManagerTree,
    MyCustomSocket,
    MyCustomNode,
    B2G_String_Socket,
    B2G_Float_Socket,
    B2G_Integer_Socket,
    B2G_Boolean_Socket,
    B2G_Trigger_Socket,
    B2G_Pipeline_Socket,
    B2G_Stage_Socket,
    B2G_2dmenu_Socket,
    B2G_3dmenu_Socket,
    B2G_OverlayMenu_Socket,
    B2G_Player_Socket,
    B2G_HUD_Socket,
    B2G_Start_Node,
    B2G_Finish_Node,
    B2G_String_Node,
    B2G_Float_Node,
    B2G_Integer_Node,
    B2G_Boolean_Node,
    B2G_Stage_Scene_Node,
    B2G_Player_Scene_Node,
    B2G_HUD_Scene_Node,
    B2G_2dMenu_Scene_Node,
    B2G_3dMenu_Scene_Node,
    B2G_OverlayMenu_Scene_Node,
    B2G_NPC_Scene_Node,
    B2G_Change_Entity_String_Property_Node,
    B2G_Change_Scene_String_Property_Node,
    B2G_Change_Entity_Integer_Property_Node,
    B2G_Change_Entity_Float_Property_Node,
    B2G_Change_Entity_Boolean_Property_Node,
    B2G_Play_Entity_Animation_Node,
    B2G_Trigger_Action_Node,
    B2G_Get_Scene_Entity_Node,
    B2G_Get_Entity_Property_Node,
    B2G_Get_HUD_Content_Node,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('CUSTOM_NODES', node_categories)

    bpy.types.Node.special_objects = bpy.props.CollectionProperty(type=ButtonAction, name="Special Objects")
    bpy.types.Node.overlay_special_objects = bpy.props.CollectionProperty(type=OverlayButtonAction, name="Special Objects")
    #bpy.types.Node.entity_properties = bpy.props.CollectionProperty(type=PlayerEntityProperty)
    bpy.types.Node.stage_objects = bpy.props.CollectionProperty(type=StageObject)
    bpy.types.Node.with_pause = bpy.props.BoolProperty(name="With Pause", default=True)

def unregister():
    del bpy.types.Node.with_pause
    del bpy.types.Node.stage_objects
    #del bpy.types.Node.entity_properties
    #del bpy.types.Node.actions_settings
    del bpy.types.Node.overlay_special_objects
    del bpy.types.Node.special_objects
    nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
