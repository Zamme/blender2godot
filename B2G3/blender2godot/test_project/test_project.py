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
        return (context.scene.name == context.scene.gamemanager_scene_name)
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene

        if bpy.path.abspath("//") == "":       
            return

        # Test game button
        row = layout.row()
        row.scale_y = 3.0
        row.operator("scene.test_game_operator")


def register():
    bpy.utils.register_class(TestGameOperator)
    bpy.utils.register_class(TestGamePanel)

def unregister():
    bpy.utils.unregister_class(TestGamePanel)
    bpy.utils.unregister_class(TestGameOperator)
