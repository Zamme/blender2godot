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
    
    @classmethod 
    def poll(self, context):
        return (context.scene.name == context.scene.gamemanager_scene_name)
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        blend_data = context.blend_data
        
        if bpy.path.abspath("//") == "":       
            return

        row = layout.row()
        row.label(text="Display properties:")
        row = layout.row()
        box1 = row.box()
        # Display properties box
        box1.prop(scene, "display_width")
        box1.prop(scene, "display_height")
        row2 = layout.row()
        box2 = row2.box()
        box2.prop(scene, "display_resizable")
        box2.prop(scene, "display_borderless")
        box2.prop(scene, "display_fullscreen")
        box2.prop(scene, "display_alwaysontop")
        #box1.prop(scene, "game_folder")       

def register():
    bpy.utils.register_class(DisplayPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(DisplayPropertiesPanel)



