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
            if context.active_object.type == "CAMERA":
                box4.prop(context.active_object.data, "angle")
            elif context.active_object.type == "GPENCIL":
                #box3.prop(context.active_object.data.layers[0].active_frame.strokes[0], "bound_box_max")
                #box3.prop(context.active_object.data.layers[0].active_frame.strokes[0], "bound_box_min")
                for _point_index,_point in enumerate(context.active_object.data.layers[0].active_frame.strokes[0].points):
                    if _point.select:
                        _point_text = "Stroke point: " + str(_point_index)
                        box3.label(text=_point_text)
                        box3.prop(_point, "co")
            else:
                box4.prop(context.active_object.special_object_info, "menu_object_type")
                if context.active_object.special_object_info.menu_object_type == "button":
                    box4.prop(context.active_object.special_object_info, "button_action_on_click")
                    if context.active_object.special_object_info.button_action_on_click == "load_stage":
                        box4.prop(context.active_object.special_object_info, "scene_link")
                    elif context.active_object.special_object_info.button_action_on_click == "load_menu":
                        box4.prop(context.active_object.special_object_info, "scene_link")
                
            box3.prop(context.active_object, "godot_exportable")
                 

def init_properties():
    pass
    #bpy.types.Scene.menu_camera_object = bpy.props.PointerProperty(type=bpy.types.Object, name="Menu Camera", poll=scene_camera_object_poll)
    #bpy.types.Object.special_object_info = bpy.props.PointerProperty(type=MenuSpecialObject, name="Object Info")

def clear_properties():
    pass
    #del bpy.types.Scene.menu_camera_object
    #del bpy.types.Object.special_object_info

def register():
    #bpy.utils.register_class(MenuSpecialObject)
    init_properties()
    bpy.utils.register_class(CreateMenu2dViewOperator)
    bpy.utils.register_class(Menu2DPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(Menu2DPropertiesPanel)
    bpy.utils.unregister_class(CreateMenu2dViewOperator)
    #bpy.utils.unregister_class(MenuSpecialObject)
    clear_properties()


