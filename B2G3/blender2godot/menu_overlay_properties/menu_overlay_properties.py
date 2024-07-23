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
For menus overlay
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
        if hasattr(context.active_object, "menu_overlay_object_properties"):
            if _sc.scene_type == context.active_object.menu_overlay_object_properties.button_action.removeprefix("load_"):
                if _sc.scene_exportable:
                    _scenes.append((_sc.name, _sc.name, "", "", _index))
                    _index += 1
    return _scenes

def get_scene_parameter_name(self, context):
    _parameter_name = ""
    if hasattr(context.active_object, "menu_overlay_object_properties"):
        _parameter_name = context.active_object.menu_overlay_object_properties.button_action.removeprefix("load_").capitalize()
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
    context.active_object.menu_overlay_object_properties.action_parameter = context.active_object.menu_overlay_object_properties.scene_parameter

class MenuOverlaySpecialObject(bpy.types.PropertyGroup):
    """ Menu Overlay Object Type """
    object_type_options = [
                            ("none", "None", "", 0), 
                            ("button", "Button", "", 1),
                            ("button_content", "Button Content", "", 2),
                            #("checkbox", "Checkbox", "", 2)
                            ]
    menu_overlay_object_type : bpy.props.EnumProperty(items=object_type_options, name="Type") # type: ignore
    object_depth : bpy.props.IntProperty(name="Object Depth", default=0, update=on_depth_update) # type: ignore

class ButtonOverlayProperties(bpy.types.PropertyGroup):
    button_name : bpy.props.StringProperty(name="New button name", default="NewButton") # type: ignore
    button_border_color : bpy.props.FloatVectorProperty(name="Button Border Color", size=4, subtype="COLOR", default=(0.0,0.0,0.0,1.0)) # type: ignore
    button_fill_color : bpy.props.FloatVectorProperty(name="Button Fill Color", size=4, subtype="COLOR", default=(1.0,1.0,1.0,1.0)) # type: ignore
    button_shape : bpy.props.EnumProperty(items=shape_options, name="Button shape") # type: ignore
    radius_parameter : bpy.props.FloatProperty(name="Button Radius", min=1.0, max=10.0, default=3.0) # type: ignore
    segments_parameter : bpy.props.IntProperty(name="Button Segments", min=8, max=64, default=12) # type: ignore
    width_parameter : bpy.props.FloatProperty(name="Button Width", min=2.0, max=10.0, default=3.0) # type: ignore
    height_parameter : bpy.props.FloatProperty(name="Button Height", min=2.0, max=10.0, default=3.0) # type: ignore

class CreateMenuOverlayButtonTextOperator(bpy.types.Operator):
    bl_idname = "scene.create_menu_overlay_button_text_operator"
    bl_label = "Create Menu Overlay Button Text"
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

class CreateMenuOverlayBaseButtonOperator(bpy.types.Operator):
    bl_idname = "scene.create_menu_overlay_base_button_operator"
    bl_label = "Create Menu Overlay Base Button"
    bl_options = {'REGISTER', 'UNDO'}

    new_button_props : bpy.props.PointerProperty(type=ButtonOverlayProperties) # type: ignore

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
        print("Creating menu overlay base button...")
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
        bpy.context.object.menu_overlay_object_properties.menu_overlay_object_type = "button"

        return {'FINISHED'}
    
class CreateMenuOverlayViewOperator(bpy.types.Operator):
    bl_idname = "scene.create_menu_overlay_view_operator"
    bl_label = "Create Menu Overlay View"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("Creating menu overlay view...")
        bpy.ops.object.camera_add(align="WORLD", location=(0.0, 0.0, 50.0), rotation=(0.0,0.0,0.0))
        bpy.ops.view3d.object_as_camera()
        #bpy.ops.object.mode_set(mode = 'OBJECT')
        return {'FINISHED'}

class MenuOverlayPropertiesPanel(bpy.types.Panel):
    """Menu Overlay Properties Panel"""
    bl_label = "Menu Overlay Properties"
    bl_idname = "MENUOVERLAYPROPERTIES_PT_layout"
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
            if (context.scene.scene_type == "overlay_menu"):
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
            row8.operator("scene.create_menu_overlay_view_operator")
            return
        else:
            row8.operator("scene.create_menu_overlay_base_button_operator")
        
        # ACTIVE OBJECT PROPERTIES
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
                    row11.prop(context.active_object.menu_overlay_object_properties, "object_depth")
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
                        row7.operator("scene.create_menu_overlay_button_text_operator", text="Add text")
                    box4 = box3.box()
                    box4.prop(context.active_object.menu_overlay_object_properties, "menu_overlay_object_type")
                case "FONT":
                    row7 = box3.row()
                    row7.prop(context.active_object.data, "font", text="Font", slider=True)
                    row8 = box3.row()
                    row8.prop(context.active_object.data, "size", text="Font Size")
                    box4 = box3.box()
                    box4.prop(context.active_object.menu_overlay_object_properties, "menu_overlay_object_type")

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
    bpy.types.Object.menu_overlay_object_properties = bpy.props.PointerProperty(type=MenuOverlaySpecialObject)

def clear_properties():
    del bpy.types.Object.menu_overlay_object_properties

def register():
    bpy.utils.register_class(ButtonOverlayProperties)
    bpy.utils.register_class(CreateMenuOverlayButtonTextOperator)
    bpy.utils.register_class(MenuOverlaySpecialObject)
    init_properties()
    bpy.utils.register_class(CreateMenuOverlayViewOperator)
    bpy.utils.register_class(CreateMenuOverlayBaseButtonOperator)
    bpy.utils.register_class(MenuOverlayPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(MenuOverlayPropertiesPanel)
    bpy.utils.unregister_class(CreateMenuOverlayBaseButtonOperator)
    bpy.utils.unregister_class(CreateMenuOverlayViewOperator)
    clear_properties()
    bpy.utils.unregister_class(MenuOverlaySpecialObject)
    bpy.utils.unregister_class(CreateMenuOverlayButtonTextOperator)
    bpy.utils.unregister_class(ButtonOverlayProperties)



