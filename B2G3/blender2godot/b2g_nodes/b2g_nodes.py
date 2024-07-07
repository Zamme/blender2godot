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

import bpy
from bpy.types import NodeTree, Node, NodeSocket

property_node_sockets = {
    "boolean" : "NodeSocketBool",
    "string" : "NodeSocketString",
    "integer" : "NodeSocketInteger",
    "float" : "NodeSocketFloat"
}

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
            layout.label(text="")

    # Socket color
    def draw_color(self, context, node):
        return (0.0, 1.0, 0.0, 1.0)

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
        _new_socket.display_shape="SQUARE"
        _new_socket.description = "Pipeline socket"
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
        _valid_scene_types = ["stage", "2dmenu", "3dmenu"]
        for _output in self.outputs:
            for _link in _output.links:
                if hasattr(_link.to_node, "scene"):
                    _scene = _link.to_node.scene
                    _link.is_valid = _scene.scene_type in _valid_scene_types
                    print("Link valid", _link.is_valid)

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
        #row2 = box1.row()
        #row2.prop(self.scene, "player_spawn_empty", text="Spawn Empty")
        if self.scene:
            layout.prop(self.scene, "scene_exportable", text="Export")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(Stage)")
        else:
            return "Stage"
    
class B2G_Player_Scene_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Player_Scene_NodeType'
    # Label for nice name display
    bl_label = "Player Scene"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    def poll_scenes(self, object):
        return object.scene_type == "player"
    
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
            layout.prop(self.scene, "scene_exportable", text="Export")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(Player)")
        else:
            return "Player"
    
class B2G_HUD_Scene_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_HUD_Scene_NodeType'
    # Label for nice name display
    bl_label = "HUD Scene"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    def poll_scenes(self, object):
        return object.scene_type == "hud"
    
    scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Scene", poll=poll_scenes) # type: ignore
    settings : bpy.props.PointerProperty(type=HudSettings, name="HudSettings") # type: ignore
    
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

    def poll_scenes(self, object):
        return object.scene_type == "2dmenu"
    
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
            return (self.scene.name + "(Menu 2D)")
        else:
            return "Menu 2D"

class B2G_3dMenu_Scene_Node(MyCustomTreeNode, Node):
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_3dMenu_Scene_NodeType'
    # Label for nice name display
    bl_label = "Menu 3D Scene"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    def poll_scenes(self, object):
        return object.scene_type == "3dmenu"
    
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
            return (self.scene.name + "(Menu 3D)")
        else:
            return "Menu 3D"

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
    HudSettings,
    MyCustomTree,
    MyCustomSocket,
    MyCustomNode,
    B2G_Pipeline_Socket,
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


def unregister():
    nodeitems_utils.unregister_node_categories('CUSTOM_NODES')

    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
