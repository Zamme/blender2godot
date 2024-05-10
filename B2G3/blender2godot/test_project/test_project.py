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
Testing game actions
"""

import subprocess
import os

import bpy


class TestGameOperator(bpy.types.Operator): # It blocks blender execution until game exits
    """Test Game Operator"""
    bl_idname = "scene.test_game_operator"
    bl_label = "Test Game"
    
    def start_game(self, context):
        print("Starting game", context.scene.project_folder)
        self.cmd = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "--path", context.scene.project_folder], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def main(self, context):
        self.start_game(context)        

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}


class TestGamePanel(bpy.types.Panel):
    """Test Game Panel"""
    bl_label = "Test Game"
    bl_idname = "TESTGAME_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 5
    
    @classmethod 
    def poll(self, context):
        return ((context.scene.name == context.scene.gamemanager_scene_name) and (bpy.data.is_saved) )
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="PLAY")        

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if not bpy.data.is_saved:       
            return

        if context.scene.godot_exporting or context.scene.is_game_exporting:       
            layout.enabled = False
        else:
            layout.enabled = True

        # Test game button
        row = layout.row()
        row.scale_y = 3.0
        box = row.box()
        if (os.path.isdir(context.scene.project_folder) and (context.scene.godot_export_ok)):
            row.alignment="CENTER"
            box.operator("scene.test_game_operator", icon="PLAY")
        else:
            box.label(text="Export to godot before testing", icon="ERROR")


def register():
    bpy.utils.register_class(TestGameOperator)
    bpy.utils.register_class(TestGamePanel)

def unregister():
    bpy.utils.unregister_class(TestGamePanel)
    bpy.utils.unregister_class(TestGameOperator)
