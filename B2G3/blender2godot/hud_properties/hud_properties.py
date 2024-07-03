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
HUD properties panel
"""

import bpy, math
from blender2godot.addon_config import addon_config # type: ignore


shape_options = [("square", "Square", "Square shape", "", 0),
                ("round", "Round", "Round shape", "", 1),
                ("triangle", "Triangle", "Triangle shape", "", 2)
                ]

element_type_options = [
    ("none", "None", "None", "", 0),
    ("text_container", "Text Container", "Text Container", "", 1),
    ("horizontal_container", "Horizontal Container", "Horizontal Container", "", 2),
    ("vertical_container", "Vertical Container", "Vertical Container", "", 3),
    ("text_content", "Text Content", "Text Content", "", 4),
    ("horizontal_content", "Horizontal Content", "Horizontal Content", "", 5),
    ("vertical_content", "Vertical Content", "Vertical Content", "", 6)
]

def update_hud_element_type(self, context):
    _ao = context.active_object
    if _ao:
        for _child in context.active_object.children:
            bpy.ops.object.select_all(action='DESELECT')
            _child.select_set(True)
            bpy.ops.object.delete()
        match self.element_type:
            case "text_container":
                bpy.ops.object.text_add()
                _text_object = context.active_object
                #context.active_object.is_containing_element = True
                context.active_object.parent = _ao
                context.active_object.name = _ao.name + "_Content"
                _text_object.delta_location = (0.0,0.0,1.0)
                _text_object.data.align_x = "CENTER"
                _text_object.data.align_y = "CENTER"
            case "horizontal_container":
                bpy.ops.object.select_all(action='DESELECT')
                _ao.select_set(True)
                context.view_layer.objects.active = _ao
                bpy.ops.object.duplicate()
                context.active_object.parent = _ao
                context.active_object.name = _ao.name + "_Content"
                #context.active_object.is_containing_element = True
                bpy.ops.object.mode_set(mode="EDIT_GPENCIL")
                bpy.ops.gpencil.select_all(action='SELECT')
                bpy.ops.transform.resize(value=(0.8, 0.8, 1.0))
            case "vertical_container":
                bpy.ops.object.select_all(action='DESELECT')
                _ao.select_set(True)
                context.view_layer.objects.active = _ao
                bpy.ops.object.duplicate()
                context.active_object.parent = _ao
                context.active_object.name = _ao.name + "_Content"
                #context.active_object.is_containing_element = True
                bpy.ops.object.mode_set(mode="EDIT_GPENCIL")
                bpy.ops.gpencil.select_all(action='SELECT')
                bpy.ops.transform.resize(value=(0.8, 0.8, 1.0))
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.ops.object.select_all(action='DESELECT')
        _ao.select_set(True)
        context.view_layer.objects.active = _ao

def poll_source_scenes(self, object):
    return (object.scene_type == "player")


def get_source_info_property_items(self, context):
    source_info_property_items = [("none", "None", "None", 0)]
    if self.source_info_scene:
        if self.source_info_scene.scene_type == "player":
            for _ind,_prop in enumerate(self.source_info_scene.player_entity_properties):
                source_info_property_items.append((_prop.property_name, _prop.property_name, _prop.property_name, _ind+1))
    return source_info_property_items

class HUDElementProperties(bpy.types.PropertyGroup):
    element_name : bpy.props.StringProperty(name="New element name", default="NewElement") # type: ignore
    element_border_color : bpy.props.FloatVectorProperty(name="Element Border Color", size=4, subtype="COLOR", default=(0.0,0.0,0.0,1.0)) # type: ignore
    element_fill_color : bpy.props.FloatVectorProperty(name="Element Fill Color", size=4, subtype="COLOR", default=(1.0,1.0,1.0,1.0)) # type: ignore
    element_shape : bpy.props.EnumProperty(items=shape_options, name="Element shape") # type: ignore
    radius_parameter : bpy.props.FloatProperty(name="Element Radius", min=1.0, max=10.0, default=3.0) # type: ignore
    segments_parameter : bpy.props.IntProperty(name="Element Segments", min=8, max=64, default=12) # type: ignore
    width_parameter : bpy.props.FloatProperty(name="Element Width", min=2.0, max=10.0, default=3.0) # type: ignore
    height_parameter : bpy.props.FloatProperty(name="Element Height", min=2.0, max=10.0, default=3.0) # type: ignore
    element_type : bpy.props.EnumProperty(name="Element Properties Type", items=element_type_options, update=update_hud_element_type) # type: ignore
    source_info_scene : bpy.props.PointerProperty(type=bpy.types.Scene, name="Source Scene", poll=poll_source_scenes) # type: ignore
    source_info_object : bpy.props.PointerProperty(type=bpy.types.Object, name="Source Object") # type: ignore
    source_info_property : bpy.props.EnumProperty(items=get_source_info_property_items, name="Source Property") # type: ignore

class NewHUDElementProperties(bpy.types.PropertyGroup):
    element_name : bpy.props.StringProperty(name="New element name", default="NewElement") # type: ignore
    element_border_color : bpy.props.FloatVectorProperty(name="Element Border Color", size=4, subtype="COLOR", default=(0.0,0.0,0.0,1.0)) # type: ignore
    element_fill_color : bpy.props.FloatVectorProperty(name="Element Fill Color", size=4, subtype="COLOR", default=(1.0,1.0,1.0,1.0)) # type: ignore
    element_shape : bpy.props.EnumProperty(items=shape_options, name="Element shape") # type: ignore
    radius_parameter : bpy.props.FloatProperty(name="Element Radius", min=1.0, max=10.0, default=3.0) # type: ignore
    segments_parameter : bpy.props.IntProperty(name="Element Segments", min=8, max=64, default=12) # type: ignore
    width_parameter : bpy.props.FloatProperty(name="Element Width", min=2.0, max=10.0, default=3.0) # type: ignore
    height_parameter : bpy.props.FloatProperty(name="Element Height", min=2.0, max=10.0, default=3.0) # type: ignore
    element_type : bpy.props.EnumProperty(name="Element Properties Type", items=element_type_options) # type: ignore

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
    hud_export_format : bpy.props.EnumProperty(items=[
                                                ("png", "PNG", "PNG", "", 0),
                                                ("svg", "SVG", "SVG", "", 1)
                                                ], name="Format", description="HUD export format") # type: ignore

class CreateHUDBaseElementOperator(bpy.types.Operator):
    bl_idname = "scene.create_hud_base_element_operator"
    bl_label = "Create HUD Base Element"
    bl_options = {'REGISTER', 'UNDO'}

    new_element_props : bpy.props.PointerProperty(type=NewHUDElementProperties) # type: ignore

    def draw(self, context):
        layout = self.layout
        row0 = layout.row()
        box0 = row0.box()
        row1 = box0.row()
        box1 = row1.box()
        row2 = box1.row()
        row2.prop(self.new_element_props, "element_name", text="Name")
        row3 = box1.row()
        row3.prop(self.new_element_props, "element_border_color")
        row4 = box1.row()
        row4.prop(self.new_element_props, "element_fill_color")
        row5 = box1.row()
        box3 = row5.box()
        row11 = box3.row()
        row11.label(text="Base Shape:", icon_value=addon_config.preview_collections[0]["shapes_icon"].icon_id)
        row10 = box3.row()
        row10.prop_tabs_enum(self.new_element_props, "element_shape")
        box2 = box1.box()
        row6 = box2.row()
        match self.new_element_props.element_shape:
            case "square":
                row6.prop(self.new_element_props, "width_parameter")
                row7 = box2.row()
                row7.prop(self.new_element_props, "height_parameter")
            case "round":
                row6.prop(self.new_element_props, "radius_parameter")
                row7 = box2.row()
                row7.prop(self.new_element_props, "segments_parameter")
            case "triangle":
                row6.prop(self.new_element_props, "width_parameter")
                row7 = box2.row()
                row7.prop(self.new_element_props, "height_parameter")
        row8 = box1.row()
        row8.label(text="Type:")
        row9 = box1.row()
        row9.props_enum(self.new_element_props, "element_type")
        
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def execute(self, context):
        print("Creating HUD base element with shape", self.new_element_props.element_shape)
        bpy.ops.object.gpencil_add(type="EMPTY")
        context.active_object.name = self.new_element_props.element_name
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
        match self.new_element_props.element_shape:
            case "square":
                str.points.add(count = 4)
                points = str.points
                _width = self.new_element_props.width_parameter/2.0
                _height = self.new_element_props.height_parameter/2.0
                points[0].co = (-_width,-_height,0.0)
                points[1].co = (_width,-_height,0.0)
                points[2].co = (_width,_height,0.0)
                points[3].co = (-_width,_height,0.0)
            case "round":
                segments = self.new_element_props.segments_parameter
                r = self.new_element_props.radius_parameter
                str.points.add(count = segments)
                points = str.points
                for ii in range(segments):
                    theta = 2.0 * 3.1415926 * float(ii) / float(segments)
                    x = r * math.cos(theta) 
                    y = r * math.sin(theta)
                    points[ii].co = (x, y, 0.0)
            case "triangle":
                _width = self.new_element_props.width_parameter/2.0
                _height = self.new_element_props.height_parameter/2.0
                str.points.add(count = 3 )
                points = str.points
                points[0].co = (0.0,-_height, 0.0)
                points[1].co = (_width, _height, 0.0)
                points[2].co = (-_width,_height,0.0)
        str.use_cyclic = True
        gpl.line_change = 50
        bpy.context.object.active_material.grease_pencil.color = self.new_element_props.element_border_color
        bpy.context.object.active_material.grease_pencil.show_fill = True
        bpy.context.object.active_material.grease_pencil.fill_color = self.new_element_props.element_fill_color
        context.active_object.hud_element_properties.element_type = self.new_element_props.element_type
        #bpy.context.object.menu2d_object_properties.menu2d_object_type = "button"

        return {'FINISHED'}

class CreateHUDViewOperator(bpy.types.Operator):
    bl_idname = "scene.create_hud_view_operator"
    bl_label = "Create HUD View"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("Creating hud view...")
        bpy.ops.object.camera_add(align="WORLD", location=(0.0, 0.0, 50.0), rotation=(0.0,0.0,0.0))
        context.active_object.name = context.scene.name + "_Camera"
        bpy.ops.view3d.object_as_camera()
        return {'FINISHED'}

class HUDPropertiesPanel(bpy.types.Panel):
    """HUD Properties Panel"""
    bl_label = "HUD Properties"
    bl_idname = "HUDPROPERTIES_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 3

    @classmethod 
    def poll(self, context):
        _ret = False
        if hasattr(context.scene, "scene_type"):
            if (context.scene.scene_type == "hud"):
                _ret = True
        return _ret
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="GREASEPENCIL")
    
    def draw(self, context):
        layout = self.layout
        
        if not bpy.data.is_saved:       
            return
        
        # HUD TOOLS
        row1 = layout.row()
        box0 = row1.box()
        row3 = box0.row()
        row3.label(text="Tools:")
        row4 = box0.row()
        if len(context.scene.objects) < 1:
            row4.operator("scene.create_hud_view_operator")
            return
        else:
            row4.operator("scene.create_hud_base_element_operator")

        # HUD PROPERTIES
        row2 = layout.row()
        box1 = row2.box()
        box1.label(text="HUD settings")
        box1.prop(context.scene.hud_settings, "visibility_type")
        # TODO : Conditional
        if context.scene.hud_settings.visibility_type == "conditional":
            box1.label(text="TODO, not available", icon="CANCEL")
        box1.prop(context.scene.hud_settings, "show_transition_type")
        if context.scene.hud_settings.show_transition_type == "fade_in":
            box1.prop(context.scene.hud_settings, "show_transition_time")
        box1.prop(context.scene.hud_settings, "hide_transition_type")
        if context.scene.hud_settings.hide_transition_type == "fade_in":
            box1.prop(context.scene.hud_settings, "hide_transition_time")
        box1.prop(context.scene.hud_settings, "hud_export_format")
       
        # ACTIVE OBJECT PROPERTIES
        if context.active_object is not None:
            row2 = layout.row()
            box2 = row2.box()
            box2.label(text="Active Object")
            box3 = box2.box()
            row5 = box3.row()
            row5.label(text=context.active_object.name)
            row7 = box3.row()
            row7.prop(context.active_object.hud_element_properties, "element_type", text="Type")
            match context.active_object.type:
                case "GPENCIL":
                    pass
                case "FONT":
                    row7 = box3.row()
                    row7.prop(context.active_object.data, "font", text="Font", slider=True)
                    row8 = box3.row()
                    row8.prop(context.active_object.data, "size", text="Font Size")
                    '''
                    box4 = box3.box()
                    row11 = box4.row()
                    row11.label(text="Property info")
                    row9 = box4.row()
                    row9.prop(context.active_object.hud_element_properties, "source_info_scene")
                    if context.active_object.hud_element_properties.source_info_scene:
                        row10 = box4.row()
                        #row10.prop(context.active_object.hud_element_properties, "source_info_object")
                        row10.prop(context.active_object.hud_element_properties, "source_info_property")
                    '''
            row6 = box3.row()
            row6.prop(context.active_object, "godot_exportable")

def init_properties():
    bpy.types.Object.hud_element_properties = bpy.props.PointerProperty(type=HUDElementProperties)
    #bpy.types.Object.is_containing_element = bpy.props.BoolProperty(name="Is Containing Element", default=False)
    bpy.types.Scene.hud_settings = bpy.props.PointerProperty(type=HudSettings)

def clear_properties():
    del bpy.types.Object.hud_element_properties
    del bpy.types.Scene.hud_settings
    #del bpy.types.Object.is_containing_element

def register():
    bpy.utils.register_class(NewHUDElementProperties)
    bpy.utils.register_class(HUDElementProperties)
    bpy.utils.register_class(HudSettings)
    init_properties()
    bpy.utils.register_class(CreateHUDBaseElementOperator)
    bpy.utils.register_class(CreateHUDViewOperator)
    bpy.utils.register_class(HUDPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(HUDPropertiesPanel)
    bpy.utils.unregister_class(CreateHUDViewOperator)
    bpy.utils.unregister_class(CreateHUDBaseElementOperator)
    clear_properties()
    bpy.utils.unregister_class(HudSettings)
    bpy.utils.unregister_class(HUDElementProperties)
    bpy.utils.unregister_class(NewHUDElementProperties)


