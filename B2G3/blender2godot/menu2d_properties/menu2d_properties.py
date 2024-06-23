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


def get_action_scenes(self, context):
    _scenes = [("none", "None", "", "NONE", 0)]
    _index = 1
    for _sc in bpy.data.scenes:
        if _sc.scene_type == context.active_object.menu2d_object_properties.button_action.removeprefix("load_"):
            if _sc.scene_exportable:
                _scenes.append((_sc.name, _sc.name, "", "", _index))
                _index += 1
    return _scenes

def get_scene_parameter_name(self, context):
    _parameter_name = context.active_object.menu2d_object_properties.button_action.removeprefix("load_").capitalize()
    return _parameter_name

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

class CreateMenu2dBaseButtonOperator(bpy.types.Operator):
    bl_idname = "scene.create_menu2d_base_button_operator"
    bl_label = "Create Menu 2D Base Button"
    bl_options = {'REGISTER', 'UNDO'}

    new_button_name : bpy.props.StringProperty(name="New button name", default="NewButton") # type: ignore

    def draw(self, context):
        layout = self.layout
        row0 = layout.row()
        box0 = row0.box()
        row1 = box0.row()
        row1.prop(self, "new_button_name")
        
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
        str.points.add(count = 4 )
        points = str.points
        points[0].co = (-5.0,-2.0,0.0)
        points[1].co = (5.0,-2.0,0.0)
        points[2].co = (5.0,2.0,0.0)
        points[3].co = (-5.0,2.0,0.0)
        str.use_cyclic = True
        gpl.line_change = 50
        bpy.context.object.active_material.grease_pencil.color = (1.0, 1.0, 1.0, 1.0)
        bpy.context.object.active_material.grease_pencil.show_fill = True
        bpy.context.object.active_material.grease_pencil.fill_color = (1.0, 0.0, 0.0, 1.0)
        bpy.ops.object.mode_set(mode = 'OBJECT')

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
        row1 = layout.row()
        box1 = row1.box()
        if len(context.scene.objects) < 1:
            box1.operator("scene.create_menu2d_view_operator")
            return
        else:
            box1.operator("scene.create_menu2d_base_button_operator")
        
        # ACTIVE OBJECT PROPERTIES
        if context.active_object is not None:
            row2 = box1.row()
            box3 = row2.box()
            _nl = "Active Object: " + context.active_object.name
            box3.label(text=_nl)
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
            '''
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


