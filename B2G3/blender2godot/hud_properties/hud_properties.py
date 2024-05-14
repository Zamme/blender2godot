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

import bpy



class CreateHUDViewOperator(bpy.types.Operator):
    bl_idname = "scene.create_hud_view_operator"
    bl_label = "Create HUD View"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        print("Creating hud view...")
        bpy.ops.object.camera_add(align="WORLD", location=(0.0, 0.0, 50.0), rotation=(0.0,0.0,0.0))
        bpy.ops.view3d.object_as_camera()
        bpy.ops.object.gpencil_add()
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
        
        # HUD PROPERTIES
        row1 = layout.row()
        box1 = row1.box()
        if len(context.scene.objects) < 1:
            box1.operator("scene.create_hud_view_operator")
            return
        
        #box1.label(text="HUD properties")
       
        # ACTIVE OBJECT PROPERTIES
        if context.active_object is not None:
            box1.label(text="Active Object")
            box2 = box1.box()
            box2.label(text=context.active_object.name)
            if context.active_object.godot_exportable:
                box2.prop(context.active_object, "collider")
            box2.prop(context.active_object, "godot_exportable")

def init_properties():
    pass

def clear_properties():
    pass

def register():
    init_properties()
    bpy.utils.register_class(CreateHUDViewOperator)
    bpy.utils.register_class(HUDPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(HUDPropertiesPanel)
    bpy.utils.unregister_class(CreateHUDViewOperator)
    clear_properties()


