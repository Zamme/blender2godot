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


class HudSettings(bpy.types.PropertyGroup):
    visibility_type : bpy.props.EnumProperty(items=[
                                    ("always", "Always", "ALWAYS", "", 0),
                                    ("conditional", "Conditional", "CONDITIONAL", "", 1)
                                        ], name="Visibility", description="HUD visibility behavior")
    show_transition_type : bpy.props.EnumProperty(items=[
                                    ("none", "None", "NONE", "", 0),
                                    ("fade_in", "Fade In", "FADE IN", "", 1)
                                        ], name="Showing HUD effect")
    show_transition_time : bpy.props.FloatProperty(name="Show Transition Time")
    hide_transition_type : bpy.props.EnumProperty(items=[
                                    ("none", "None", "NONE", "", 0),
                                    ("fade_in", "Fade In", "FADE IN", "", 1)
                                        ], name="Hiding HUD effect")
    hide_transition_time : bpy.props.FloatProperty(name="Hide Transition Time")

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
       
        # ACTIVE OBJECT PROPERTIES
        if context.active_object is not None:
            row2 = layout.row()
            box2 = row2.box()
            box2.label(text="Active Object")
            box3 = box2.box()
            box3.label(text=context.active_object.name)
            box3.prop(context.active_object, "hud_object_type")
            box3.prop(context.active_object, "godot_exportable")

def init_properties():
    bpy.types.Object.hud_object_type = bpy.props.EnumProperty(items=[
                                                ("none", "None", "NONE", "", 0),
                                                ("frame", "Frame", "FRAME", "", 1),
                                                ("container", "Container", "CONTAINER", "", 2)
                                                ], name="Type", description="HUD object type")

    bpy.types.Scene.hud_settings = bpy.props.PointerProperty(type=HudSettings)

def clear_properties():
    pass

def register():
    bpy.utils.register_class(HudSettings)
    init_properties()
    bpy.utils.register_class(CreateHUDViewOperator)
    bpy.utils.register_class(HUDPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(HUDPropertiesPanel)
    bpy.utils.unregister_class(CreateHUDViewOperator)
    clear_properties()
    bpy.utils.unregister_class(HudSettings)


