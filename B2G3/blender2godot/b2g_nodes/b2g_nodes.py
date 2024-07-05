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

class B2G_Scene_Node(MyCustomTreeNode, Node):
    '''A custom node'''
    # Optional identifier string. If not explicitly defined, the python class name is used.
    bl_idname = 'B2G_Scene_NodeType'
    # Label for nice name display
    bl_label = "B2G Scene Node"
    # Icon identifier
    bl_icon = 'SEQ_PREVIEW'
    bl_width_default = 200.0
    bl_height_default = 100.0

    scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Scene") # type: ignore

    def init(self, context):
        pass

    def copy(self, node):
        print("Copying from node ", node)

    def free(self):
        print("Removing node ", self, ", Goodbye!")

    def draw_buttons(self, context, layout):
        #layout.prop(self.scene, "scene_type", text="Scene type:")
        box1 = layout.box()
        #row1 = box1.row()
        #row1.label(text=("Scene type: " + self.scene.scene_type.capitalize()))
        match self.scene.scene_type:
            case "stage":
                row2 = box1.row()
                row2.prop(self.scene, "player_spawn_empty", text="Spawn Empty")
            case "player":
                pass
            case "hud":
                row2 = box1.row()
                row2.prop(self.scene.hud_settings, "visibility_type", text="Spawn Empty")
        layout.prop(self.scene, "scene_exportable", text="Export")

    def draw_buttons_ext(self, context, layout):
        pass

    def draw_label(self):
        if self.scene:
            return (self.scene.name + "(" + self.scene.scene_type.capitalize() + ")")
        else:
            return "B2G Scene"
    
    def update_inputs(self):
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
        match self.scene.scene_type:
            case "player":
                for _property in self.scene.player_entity_properties:
                    if not self.outputs.get(_property.property_name):
                        self.outputs.new(property_node_sockets[_property.property_type], _property.property_name)

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
    # identifier, label, items list
    MyNodeCategory('SCENES', "Scene", items=[
        # our basic node
        NodeItem("CustomNodeType"),
    ]),
    MyNodeCategory('MATH', "Math", items=[
        # our basic node
        #NodeItem("FunctionNodeBooleanMath"),
    ]),
    MyNodeCategory('CONSTANTS', "Constants", items=[
        # our basic node
        NodeItem("B2G_String_NodeType"),
        NodeItem("B2G_Float_NodeType"),
    ]),
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
]

classes = (
    MyCustomTree,
    MyCustomSocket,
    MyCustomNode,
    B2G_Scene_Node,
    B2G_String_Node,
    B2G_Float_Node,
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
