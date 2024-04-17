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
Editor main panel
"""

import bpy


class Blender2GodotPanel(bpy.types.Panel):
    """Blender2Godot Panel"""
    bl_label = "B2G Configuration"
    bl_idname = "BLENDER2GODOT_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_order = 0
    
    def draw(self, context):
        layout = self.layout

        scene = context.scene
        blend_data = context.blend_data
        row = layout.row()
        row.label(text="Addon properties:")
        row = layout.row()
        box0 = row.box()
        
        # Addon settings
        #box0.prop(scene, "custom_godot")
        #if scene.custom_godot:
        box0.prop(scene, "godot_executable")

        if bpy.path.abspath("//") == "":       
            row = layout.row()
            row.label(text="Save blend file to continue")
			

def register():
    bpy.utils.register_class(Blender2GodotPanel)

def unregister():
    bpy.utils.unregister_class(Blender2GodotPanel)
