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
For splash properties
"""

import os
import shutil

import bpy

class SplashPropertiesPanel(bpy.types.Panel):
    """Splash Properties Panel"""
    bl_label = "Splash Properties"
    bl_idname = "SPLASHPROPERTIES_PT_layout"
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
        layout.label(icon="RESTRICT_VIEW_OFF")        

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        blend_data = context.blend_data
        
        if not bpy.data.is_saved:       
            return

        if context.scene.is_game_exporting:
            layout.enabled = False
        else:
            layout.enabled = True

        row = layout.row()
        box1 = row.box()
        # Splash properties box
        box1.prop(scene, "splash_showimage", text="Image")
        if scene.splash_showimage:
            box1.prop(scene, "splash_imagefilepath")
        row2 = layout.row()
        box2 = row2.box()
        box2.prop(scene, "splash_fullsize")
        box2.prop(scene, "splash_usefilter")
        box2.prop(scene, "splash_bgcolor")

def init_properties():
    # Splash vars
    bpy.types.Scene.splash_showimage = bpy.props.BoolProperty(name="Show splash image", default=True)
    bpy.types.Scene.splash_imagefilepath = bpy.props.StringProperty(name="Splash Image Filepath", subtype="FILE_PATH", default="res://icon.png")
    bpy.types.Scene.splash_fullsize = bpy.props.BoolProperty(name="Full size", default=False)
    bpy.types.Scene.splash_usefilter = bpy.props.BoolProperty(name="Use filter", default=False)
    bpy.types.Scene.splash_bgcolor = bpy.props.FloatVectorProperty(name="BG Color", subtype = "COLOR", default = (0.0,0.0,0.0,1.0), min = 0.0, max = 1.0, size = 4)

def clear_properties():
    del bpy.types.Scene.splash_showimage
    del bpy.types.Scene.splash_imagefilepath
    del bpy.types.Scene.splash_fullsize
    del bpy.types.Scene.splash_usefilter
    del bpy.types.Scene.splash_bgcolor

def register():
    init_properties()
    bpy.utils.register_class(SplashPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(SplashPropertiesPanel)
    clear_properties()


