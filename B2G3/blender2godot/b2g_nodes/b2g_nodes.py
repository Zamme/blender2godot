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
from bpy.types import NodeTree, Node, NodeSocket
#from blender2godot.player_properties import player_properties # type: ignore


action_type_options = [("none", "None", "", 0), 
                        ("load_stage", "Load Stage", "", 1),
                        ("load_2dmenu", "Load Menu 2D", "", 2),
                        ("load_3dmenu", "Load Menu 3D", "", 3),
                        ("quit_game", "Quit Game", "", 4)
                        ]

property_node_sockets = {
    "boolean" : "B2G_Boolean_SocketType",
    "string" : "B2G_String_SocketType",
    "integer" : "B2G_Integer_SocketType",
    "float" : "B2G_Float_SocketType"
}

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

def update_action_parameter(self, context):
    context.active_object.special_object_info.action_parameter = context.active_object.special_object_info.scene_parameter

def on_button_action_update(self, context):
    print("Update button action click", self.button_node_name)
    bpy.data.node_groups["GameManager"].nodes[self.button_node_name].update()

class ActionsProperties(bpy.types.PropertyGroup):
    action_id : bpy.props.StringProperty(name="Action ID", default="None") # type: ignore
    action_process : bpy.props.EnumProperty(items=get_actions_list_array, name="Action Process") # type: ignore

class ButtonAction(bpy.types.PropertyGroup):
    button_node_name : bpy.props.StringProperty(name="Button Node") # type: ignore
    button_name : bpy.props.StringProperty(name="Button Name") # type: ignore
    button_action_on_click : bpy.props.EnumProperty(items=action_type_options, name="Action On Click", update=on_button_action_update) # type: ignore
    action_parameter : bpy.props.StringProperty(name="Action Parameter", default="") # type: ignore
    scene_parameter : bpy.props.EnumProperty(items=get_action_scenes, name="Scene Parameter", default=0, update=update_action_parameter) # type: ignore

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

# Derived from the NodeTree base type, similar to Menu, Operator, Panel, etc.
class MyCustomTree(NodeTree):
    # Description string
    '''A custom node tree type that will show up in the editor type list'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'CustomTreeType'
    # Label for nice name display
    bl_label = "GameManager Node Tree"
    # Icon identifier
    bl_icon = 'NODETREE'


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
        return ntree.bl_idname == 'CustomTreeType'


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
class B2G_Float_Socket(NodeSocket):
    # Description string
    """float socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Float_SocketType'
    # Label for nice name display
    bl_label = "Float Socket"
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.5, 0.5, 0.0, 1.0)

class B2G_String_Socket(NodeSocket):
    # Description string
    """string socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_String_SocketType'
    # Label for nice name display
    bl_label = "String Socket"
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.0, 0.5, 0.5, 1.0)

class B2G_Boolean_Socket(NodeSocket):
    # Description string
    """boolean socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Boolean_SocketType'
    # Label for nice name display
    bl_label = "Boolean Socket"
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.0, 0.25, 0.0, 1.0)

class B2G_Integer_Socket(NodeSocket):
    # Description string
    """integer socket type"""
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Integer_SocketType'
    # Label for nice name display
    bl_label = "Integer Socket"
    
    # Optional function for drawing the socket input value
    def draw(self, context, layout, node, text):
        if self.is_output or self.is_linked:
            layout.label(text=text)
        else:
            layout.label(text=text)

    # Socket color
    def draw_color(self, context, node):
        return (0.5, 0.5, 0.5, 1.0)

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
        return (0.0, 0.0, 1.0, 1.0)

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
        return (0.0, 0.0, 0.5, 1.0)

# --- END SOCKETS ---

# --- PIPELINE NODES ---
class B2G_Start_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Start_NodeType'
    # Label for nice name display
    bl_label = "Start"
    # Icon identifier
    bl_icon = 'SOUND'

    def init(self, context):
        _new_socket = self.outputs.new("B2G_Pipeline_SocketType", "Go")
        #_new_socket.display_shape="SQUARE"
        #_new_socket.description = "Pipeline socket"
        _new_socket.link_limit = 1

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
    bl_icon = 'SOUND'

    def init(self, context):
        self.inputs.new("B2G_Pipeline_SocketType", "Go")

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
class B2G_Float_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Float_NodeType'
    # Label for nice name display
    bl_label = "B2G Float Node"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    my_float : bpy.props.FloatProperty(name="MyFloat") # type: ignore

    def init(self, context):
        #self.inputs.new("NodeSocketString", "Value")
        self.outputs.new("NodeSocketString", "Value")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "my_float", text="")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "Float"
    
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

    my_string : bpy.props.StringProperty(name="MyString") # type: ignore

    def init(self, context):
        #self.inputs.new("NodeSocketString", "Value")
        self.outputs.new("NodeSocketString", "Value")

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "my_string", text="")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        return "String"
    
    def update_inputs(self):
        pass

    def update_outputs(self):
        pass
# --- END MATH NODES ---

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

    def poll_scenes(self, object):
        return object.scene_type == "stage"
    
    scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Scene", poll=poll_scenes) # type: ignore

    def init(self, context):
        self.inputs.new("B2G_Player_SocketType", "Player")
        self.inputs.new("B2G_Pipeline_SocketType", "Go")
        _new_output = self.outputs.new("B2G_Pipeline_SocketType", "Go")
        _new_output.link_limit = 1

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        box1 = layout.box()
        row1 = box1.row()
        row1.prop(self, "scene", text="Scene")
        # Check scene properties
        if self.scene:
            if not self.scene.player_spawn_empty:
                row2 = box1.row()
                row2.label(text="Player spawn not set", icon="INFO")
        else:
            row2 = box1.row()
            row2.label(text="Stage scene not set", icon="INFO")
        # Check scene links
        if self.scene:
            if not self.inputs[0].is_linked:
                row2 = box1.row()
                row2.label(text="Player not set", icon="INFO")
            if not self.inputs[1].is_linked:
                row2 = box1.row()
                row2.label(text="Stage not in pipeline", icon="INFO")

        # EXPORT PROPERTY
        if self.scene:
            layout.prop(self.scene, "scene_exportable", text="Export")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(Stage)")
        else:
            return "Stage"
    
    def update(self):
        '''Called when node graph is changed'''
        #print("Update", self.name, "links")
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        '''Mark invalid links, must be called from a timer'''
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

class B2G_Player_Scene_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Player_Scene_NodeType'
    # Label for nice name display
    bl_label = "Player Scene"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    #player_actions = []

    def poll_scenes(self, object):
        return object.scene_type == "player"
    
    def on_update_scene(self, context):
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
        self.player_entity_properties.clear()
        if self.scene:
            for _player_property in self.scene.player_entity_properties:
                _new_property = self.player_entity_properties.add()
                _new_property.property_name = _player_property.property_name
                _new_property.property_type = _player_property.property_type
                match _player_property.property_type:
                    case "boolean":
                        _new_property.property_boolean = _player_property.property_boolean
                    case "string":
                        _new_property.property_string = _player_property.property_string
                    case "integer":
                        _new_property.property_integer = _player_property.property_integer
                    case "float":
                        _new_property.property_float = _player_property.property_float
        # Clean new outputs on change scene
        print("Update player")
        self.outputs.clear()
        self.outputs.new("B2G_Player_SocketType", "Player")
        # Load entity properties as new outputs
        if self.scene:
            for _entity_property in self.scene.player_entity_properties:
                self.outputs.new(property_node_sockets[_entity_property.property_type], _entity_property.property_name)

    scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Scene", poll=poll_scenes, update=on_update_scene) # type: ignore

    def init(self, context):
        # INPUTS
        self.inputs.new("B2G_HUD_SocketType", "HUD")
        self.inputs.new("B2G_2dmenu_SocketType", "Pause Menu") # TODO: Change by pausemenu_socket
        # OUTPUTS
        self.outputs.new("B2G_Player_SocketType", "Player")

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
            box3 = box1.box()
            row4 = box3.row()
            row4.label(text="Player Properties")
            for _player_property in self.player_entity_properties:
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
            box1.prop(self.scene, "scene_exportable", text="Export")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(Player)")
        else:
            return "Player"
    
    def update(self):
        '''Called when node graph is changed'''
        print("Update", self.name)
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        '''Mark invalid links, must be called from a timer'''
        print("Update", self.name, "links")
        _input_player = self.inputs[0]
        for _link in _input_player.links:
            _valid_link = False
            if type(_link.from_socket).__name__ == "B2G_HUD_Socket":
                _valid_link = True
            else:
                _valid_link = False
            _link.is_valid = _valid_link

class B2G_HUD_Scene_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_HUD_Scene_NodeType'
    # Label for nice name display
    bl_label = "HUD Scene"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    new_inputs = []
    valid_sockets = ["B2G_Float_Socket", "B2G_Integer_Socket", "B2G_Boolean_Socket", "B2G_String_Socket"]

    def poll_scenes(self, object):
        return object.scene_type == "hud"
    
    def on_update_scene(self, context):
        # Clean inputs on change scene
        self.inputs.clear()
        self.new_inputs.clear()
        # Load entity properties as new outputs
        if self.scene:
            for _object in self.scene.objects:
                #print(_entity_property.property_name)
                if hasattr(_object, "hud_element_properties"):
                    match _object.hud_element_properties.element_type:
                        case "text_content":
                            self.new_inputs.append(self.inputs.new("B2G_String_SocketType", _object.name))
                        case "horizontal_content":
                            self.new_inputs.append(self.inputs.new("B2G_Float_SocketType", _object.name))
                        case "vertical_content":
                            self.new_inputs.append(self.inputs.new("B2G_Float_SocketType", _object.name))
        else:
            for _new_input in self.new_inputs:
                self.inputs.remove(_new_input)
            self.new_inputs.clear()

    scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Scene", poll=poll_scenes, update=on_update_scene) # type: ignore
    settings : bpy.props.PointerProperty(type=HudSettings, name="HudSettings") # type: ignore
    
    def init(self, context):
        self.outputs.new("B2G_HUD_SocketType", "HUD")

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
            row2.prop(self.settings, "visibility_type", text="Visibility")
            row2 = box1.row()
            row2.prop(self.settings, "show_transition_type", text="Show Transition Type")
            row2 = box1.row()
            row2.prop(self.settings, "show_transition_time", text="Show Transition Time")
            row2 = box1.row()
            row2.prop(self.settings, "hide_transition_type", text="Hide Transition Type")
            row2 = box1.row()
            row2.prop(self.settings, "hide_transition_time", text="Hide Transition Time")
            layout.prop(self.scene, "scene_exportable", text="Export")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(HUD)")
        else:
            return "HUD"

    def update(self):
        '''Called when node graph is changed'''
        print("Update", self.name, "links")
        bpy.app.timers.register(self.mark_invalid_links)

    def mark_invalid_links(self):
        for _input in self.inputs:
            for _link in _input.links:
                _valid_link = False
                #print(type(_link.from_socket).__name__)
                if type(_link.from_socket).__name__ in self.valid_sockets:
                    _valid_link = True
                else:
                    _valid_link = False
                _link.is_valid = _valid_link

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

    #new_outputs = []

    def poll_scenes(self, object):
        return object.scene_type == "2dmenu"

    def on_update_scene(self, context):
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
        print("Update", self.name)
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
        print("Update", self.name, "links")
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

    def poll_scenes(self, object):
        return object.scene_type == "3dmenu"

    def on_update_scene(self, context):
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
        print("Update", self.name, "links")
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

''' SCENE NODE MASTER CLASS 
class B2G_Scene_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Scene_NodeType'
    # Label for nice name display
    bl_label = "B2G Scene Node"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    def update_all(self, context):
        self.update_inputs()
        self.update_outputs()

    scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Scene", update=update_all) # type: ignore

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
        #row1.label(text=("Scene type: " + self.scene.scene_type.capitalize()))
        if self.scene:
            match self.scene.scene_type:
                case "stage":
                    row2 = box1.row()
                    row2.prop(self.scene, "player_spawn_empty", text="Spawn Empty")
                case "player":
                    pass
                case "hud":
                    row2 = box1.row()
                    #row2.prop(self.scene.hud_settings, "visibility_type", text="Spawn Empty")
            layout.prop(self.scene, "scene_exportable", text="Export")
            #self.update_inputs()
            #self.update_outputs()

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(" + self.scene.scene_type.capitalize() + ")")
        else:
            return "B2G Scene"
    
    def update_inputs(self):
        self.inputs.clear()
        match self.scene.scene_type:
            case "player":
                for _property in self.scene.player_entity_properties:
                    if not self.inputs.get(_property.property_name):
                        self.inputs.new(property_node_sockets[_property.property_type], _property.property_name)
            case "hud":
                for _object in self.scene.objects:
                    if hasattr(_object, "hud_element_properties"):
                        #_object.hud_element_properties.element_type
                        match _object.hud_element_properties.element_type:
                            case "text_content":
                                _socket_name = _object.name
                                if not self.inputs.get(_object.name):
                                    self.inputs.new("NodeSocketString", _object.name)
    
    def update_outputs(self):
        self.outputs.clear()
        match self.scene.scene_type:
            case "player":
                for _property in self.scene.player_entity_properties:
                    if not self.outputs.get(_property.property_name):
                        self.outputs.new(property_node_sockets[_property.property_type], _property.property_name)
'''

# --- END SCENE NODES ---

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
        return context.space_data.tree_type == 'CustomTreeType'


# all categories in a list
node_categories = [
    MyNodeCategory('SCENES', "Scene", items=[
        NodeItem("B2G_Stage_Scene_NodeType"),
        NodeItem("B2G_Player_Scene_NodeType"),
        NodeItem("B2G_HUD_Scene_NodeType"),
        NodeItem("B2G_2dMenu_Scene_NodeType"),
        NodeItem("B2G_3dMenu_Scene_NodeType"),
        NodeItem("B2G_NPC_Scene_NodeType"),
    ]),
    MyNodeCategory('MATH', "Math", items=[
        #NodeItem("FunctionNodeBooleanMath"),
    ]),
    MyNodeCategory('CONSTANTS', "Constants", items=[
        NodeItem("B2G_String_NodeType"),
        NodeItem("B2G_Float_NodeType"),
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
    ActionsProperties,
    HudSettings,
    PlayerEntityProperty,
    MyCustomTree,
    MyCustomSocket,
    MyCustomNode,
    B2G_String_Socket,
    B2G_Float_Socket,
    B2G_Integer_Socket,
    B2G_Boolean_Socket,
    B2G_Pipeline_Socket,
    B2G_Stage_Socket,
    B2G_2dmenu_Socket,
    B2G_3dmenu_Socket,
    B2G_Player_Socket,
    B2G_HUD_Socket,
    B2G_Start_Node,
    B2G_Finish_Node,
    B2G_String_Node,
    B2G_Float_Node,
    B2G_Stage_Scene_Node,
    B2G_Player_Scene_Node,
    B2G_HUD_Scene_Node,
    B2G_2dMenu_Scene_Node,
    B2G_3dMenu_Scene_Node,
    B2G_NPC_Scene_Node,
)


def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    nodeitems_utils.register_node_categories('CUSTOM_NODES', node_categories)

    bpy.types.Node.special_objects = bpy.props.CollectionProperty(type=ButtonAction, name="Special Objects")
    bpy.types.Node.actions_settings = bpy.props.CollectionProperty(type=ActionsProperties)
    bpy.types.Node.player_entity_properties = bpy.props.CollectionProperty(type=PlayerEntityProperty)

def unregister():
    del bpy.types.Node.player_entity_properties
    del bpy.types.Node.actions_settings
    del bpy.types.Node.special_objects
    nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
