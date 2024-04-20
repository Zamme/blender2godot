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



class CreateGameManagerOperator(bpy.types.Operator):
    """Create Game Manager Operator"""
    bl_idname = "scene.create_gamemanager_operator"
    bl_label = "Create Game Manager"

    def execute(self, context):
        print("Creating Game Manager")
        _new_scene = bpy.data.scenes.new(context.scene.gamemanager_scene_name)
        #context.scene = _new_scene
        return {'FINISHED'}

class Blender2GodotPanel(bpy.types.Panel):
    """Blender2Godot Panel"""
    bl_label = "B2G Configuration"
    bl_idname = "BLENDER2GODOT_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_order = 0

    _gamemanager_added = False
    _in_gamemanager = False

    @classmethod 
    def poll(self, context):
        _gm_index = bpy.data.scenes.find(context.scene.gamemanager_scene_name)
        self._gamemanager_added = (_gm_index > -1)
        self._in_gamemanager = (context.scene.name == context.scene.gamemanager_scene_name)
        return (self._in_gamemanager or not self._gamemanager_added)

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        blend_data = context.blend_data
        if not self._gamemanager_added:
            row = layout.row()
            row.operator("scene.create_gamemanager_operator")
        else:
            # Addon settings
            row = layout.row()
            row.label(text="Addon properties:")
            row = layout.row()
            box0 = row.box()        
            box0.prop(scene, "godot_executable")
            if bpy.path.abspath("//") == "":       
                row = layout.row()
                row.label(text="Save blend file to continue")
			

def register():
    bpy.utils.register_class(Blender2GodotPanel)

def unregister():
    bpy.utils.unregister_class(Blender2GodotPanel)
