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
For display properties
"""

import os
import shutil

import bpy

class DisplayPropertiesPanel(bpy.types.Panel):
    """Display Properties Panel"""
    bl_label = "Display Properties"
    bl_idname = "DISPLAYPROPERTIES_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_order = 1
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod 
    def poll(self, context):
        return ((context.scene.name == context.scene.gamemanager_scene_name) and (bpy.data.is_saved))
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="RESTRICT_VIEW_ON")        

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        blend_data = context.blend_data
        
        if not bpy.data.is_saved:       
            return

        row0 = layout.row()
        box0 = row0.box()
        box0.label(text="Resolution:")
        box1 = box0.box()
        box1.prop(scene, "display_width")
        box1.prop(scene, "display_height")
        box2 = box0.box()
        box2.label(text="Options:")
        box2.prop(scene, "display_resizable")
        box2.prop(scene, "display_borderless")
        box2.prop(scene, "display_fullscreen")
        box2.prop(scene, "display_alwaysontop")

def init_properties():
    # Display vars
    bpy.types.Scene.display_width = bpy.props.IntProperty(name="Width", default=1024)
    bpy.types.Scene.display_height = bpy.props.IntProperty(name="Height", default=768)
    bpy.types.Scene.display_resizable = bpy.props.BoolProperty(name="Resizable", default=True)
    bpy.types.Scene.display_borderless = bpy.props.BoolProperty(name="Borderless", default=False)
    bpy.types.Scene.display_fullscreen = bpy.props.BoolProperty(name="Fullscreen", default=False)
    bpy.types.Scene.display_alwaysontop = bpy.props.BoolProperty(name="Always on top", default=False)

def clear_properties():
    del bpy.types.Scene.display_width
    del bpy.types.Scene.display_height
    del bpy.types.Scene.display_resizable
    del bpy.types.Scene.display_borderless
    del bpy.types.Scene.display_fullscreen
    del bpy.types.Scene.display_alwaysontop

def register():
    init_properties()
    bpy.utils.register_class(DisplayPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(DisplayPropertiesPanel)
    clear_properties()


