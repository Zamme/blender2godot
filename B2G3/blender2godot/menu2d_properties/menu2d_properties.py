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

import bpy, math
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

def update_action_parameter(self, context):
    context.active_object.menu2d_object_properties.action_parameter = context.active_object.menu2d_object_properties.scene_parameter

class Menu2DObjectProperties(bpy.types.PropertyGroup):
    """ Menu 2D Object Type """
    object_type_options = [
        ("none", "None", "", 0),
        ("button", "Button", "", 1),
        ("checkbutton", "Checkbutton", "", 2)]
    button_actions = [
        ("none", "None", "", 0),
        ("close_menu", "Close Menu", "", 1),
        ("quit_game", "Quit Game", "", 2),
        ("load_stage", "Load Stage", "", 3),
        ("load_2dmenu", "Load Menu 2D", "", 4),
        ("load_3dmenu", "Load Menu 3D", "", 5)
        ]
    check_actions = [
        ("none", "None", "", 0),
        ("option1", "Option1", "", 1),
        ("option2", "Option2", "", 2)]
    menu2d_object_type : bpy.props.EnumProperty(items=object_type_options, name="Object Type", default=0) # type: ignore
    button_action : bpy.props.EnumProperty(items=button_actions, name="Button Action", default=0) # type: ignore
    action_parameter : bpy.props.StringProperty(name="Action Parameter", default="") # type: ignore
    check_action : bpy.props.EnumProperty(items=check_actions, name="Check Action", default=0) # type: ignore
    scene_parameter : bpy.props.EnumProperty(items=get_action_scenes, name="Scene Parameter", default=0, update=update_action_parameter) # type: ignore

class Button2dProperties(bpy.types.PropertyGroup):
    button_name : bpy.props.StringProperty(name="New button name", default="NewButton") # type: ignore
    button_border_color : bpy.props.FloatVectorProperty(name="Button Border Color", size=4, subtype="COLOR", default=(0.0,0.0,0.0,1.0)) # type: ignore
    button_fill_color : bpy.props.FloatVectorProperty(name="Button Fill Color", size=4, subtype="COLOR", default=(1.0,1.0,1.0,1.0)) # type: ignore
    button_shape : bpy.props.EnumProperty(items=shape_options, name="Button shape") # type: ignore
    radius_parameter : bpy.props.FloatProperty(name="Button Radius", min=1.0, max=10.0, default=3.0) # type: ignore
    segments_parameter : bpy.props.IntProperty(name="Button Segments", min=8, max=64, default=12) # type: ignore
    width_parameter : bpy.props.FloatProperty(name="Button Width", min=2.0, max=10.0, default=3.0) # type: ignore
    height_parameter : bpy.props.FloatProperty(name="Button Height", min=2.0, max=10.0, default=3.0) # type: ignore

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
        _text_object.data.align_x = "MIDDLE"
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
        row3 = box1.row()
        row3.prop(self.new_button_props, "button_border_color")
        row4 = box1.row()
        row4.prop(self.new_button_props, "button_fill_color")
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
        if hasattr(context.scene, "scene_type"):
            if (context.scene.scene_type == "2dmenu"):
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
        row9 = layout.row()
        row1 = layout.row()
        box2 = row9.box()
        row10 = box2.row()
        row10.label(text="Tools:")
        row8 = box2.row()
        if len(context.scene.objects) < 1:
            row8.operator("scene.create_menu2d_view_operator")
            return
        else:
            row8.operator("scene.create_menu2d_base_button_operator")
        
        # ACTIVE OBJECT PROPERTIES
        if context.active_object is not None:
            box1 = row1.box()
            row2 = box1.row()
            box3 = row2.box()
            _nl = "Active Object: " + context.active_object.name
            box3.label(text=_nl)
            if context.active_object.type == "GPENCIL":
                gpl = bpy.data.grease_pencils[context.active_object.name].layers[0]
                box5 = box3.box()
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
                box4 = box3.box()
                box4.prop(context.active_object.menu2d_object_properties, "menu2d_object_type")
                match context.active_object.menu2d_object_properties.menu2d_object_type:
                    case "button":
                        box4.prop(context.active_object.menu2d_object_properties, "button_action")
                        _act = context.active_object.menu2d_object_properties.button_action
                        if ((_act != "none") and (_act != "close_menu") and (_act != "quit_game")):
                            _param_name = get_scene_parameter_name(self, context)
                            box4.prop(context.active_object.menu2d_object_properties, "scene_parameter", text=_param_name)
                    case "check":
                        box4.prop(context.active_object.menu2d_object_properties, "check_action")
            ''' DEBUG
            if context.active_object.type == "GPENCIL":
                for _point_index,_point in enumerate(context.active_object.data.layers[0].active_frame.strokes[0].points):
                    if _point.select:
                        _point_text = "Stroke point: " + str(_point_index)
                        box3.label(text=_point_text)
                        box3.prop(_point, "co")
            '''                
            box3.prop(context.active_object, "godot_exportable")
                 

def init_properties():
    bpy.types.Object.menu2d_object_properties = bpy.props.PointerProperty(type=Menu2DObjectProperties)

def clear_properties():
    del bpy.types.Object.menu2d_object_properties

def register():
    bpy.utils.register_class(Button2dProperties)
    bpy.utils.register_class(CreateMenu2dButtonTextOperator)
    bpy.utils.register_class(Menu2DObjectProperties)
    init_properties()
    bpy.utils.register_class(CreateMenu2dViewOperator)
    bpy.utils.register_class(CreateMenu2dBaseButtonOperator)
    bpy.utils.register_class(Menu2DPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(Menu2DPropertiesPanel)
    bpy.utils.unregister_class(CreateMenu2dBaseButtonOperator)
    bpy.utils.unregister_class(CreateMenu2dViewOperator)
    clear_properties()
    bpy.utils.unregister_class(Menu2DObjectProperties)
    bpy.utils.unregister_class(CreateMenu2dButtonTextOperator)
    bpy.utils.unregister_class(Button2dProperties)



