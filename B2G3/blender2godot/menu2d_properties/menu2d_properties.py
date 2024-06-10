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

import bpy


def get_stages_scenes(self, context):
    _scenes = [("none", "None", "", "NONE", 0)]
    _index = 1
    for _sc in bpy.data.scenes:
        if _sc.scene_type == context.active_object.menu2d_object_properties.button_action:
            _scenes.append((_sc.name, _sc.name, "", "", _index))
            _index += 1
    return _scenes

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
        ("load_menu2d", "Load Menu 2D", "", 4),
        ("load_menu3d", "Load Menu 3D", "", 5)
        ]
    check_actions = [
        ("none", "None", "", 0),
        ("option1", "Option1", "", 1),
        ("option2", "Option2", "", 2)]
    menu2d_object_type : bpy.props.EnumProperty(items=object_type_options, name="Object Type", default=0) # type: ignore
    button_action : bpy.props.EnumProperty(items=button_actions, name="Button Action", default=0) # type: ignore
    action_parameter : bpy.props.StringProperty(name="Action Parameter", default="") # type: ignore
    check_action : bpy.props.EnumProperty(items=check_actions, name="Check Action", default=0) # type: ignore

class CreateMenu2dViewOperator(bpy.types.Operator):
    bl_idname = "scene.create_menu2d_view_operator"
    bl_label = "Create Menu 2D View"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("Creating menu 2d view...")
        bpy.ops.object.camera_add(align="WORLD", location=(0.0, 0.0, 50.0), rotation=(0.0,0.0,0.0))
        bpy.ops.view3d.object_as_camera()
        bpy.ops.object.gpencil_add()
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
                        box4.prop(context.active_object.menu2d_object_properties, "action_parameter")
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
    #bpy.types.Scene.menu_camera_object = bpy.props.PointerProperty(type=bpy.types.Object, name="Menu Camera", poll=scene_camera_object_poll)
    pass

def clear_properties():
    del bpy.types.Object.menu2d_object_properties
    #del bpy.types.Object.special_object_info
    pass

def register():
    #bpy.utils.register_class(MenuSpecialObject)
    bpy.utils.register_class(Menu2DObjectProperties)
    init_properties()
    bpy.utils.register_class(CreateMenu2dViewOperator)
    bpy.utils.register_class(Menu2DPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(Menu2DPropertiesPanel)
    bpy.utils.unregister_class(CreateMenu2dViewOperator)
    clear_properties()
    bpy.utils.unregister_class(Menu2DObjectProperties)


