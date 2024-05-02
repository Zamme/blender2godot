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
Building utils for exporting to different platforms
"""

import bpy


class ExportProjectToGodotOperator(bpy.types.Operator):
    """Export Project To Godot Operator"""
    bl_idname = "scene.export_project_to_godot_operator"
    bl_label = "Export To Godot"
    
    @classmethod 
    def poll(self, context):
        cond1 = (context.scene.name == context.scene.gamemanager_scene_name)
        cond2 = (bpy.data.is_saved)
        cond3 = (bpy.data.scenes[context.scene.gamemanager_scene_name].startup_scene != None)
        """
        _min_scenes = []
        _tr = context.scene.current_template_requirements.template_requirements
        for _reqs in _tr:
            if _reqs.name == "project_export":
                for _index,_value in enumerate(_reqs.requirements):
                    _min_scenes.append(_value.value.lower())
            break
        print("Minimum scenes:", _min_scenes)
        """
        return (cond1 and cond2 and cond3)
    
    def execute(self, context):
        print("Deleting last export...")
        bpy.ops.scene.delete_project_operator()
        print("Last export deleted!")
        print("Exporting to godot project...")
        bpy.ops.scene.create_godot_project_operator()
        bpy.ops.scene.export_game_operator()
        bpy.ops.scene.open_godot_project_operator()
        print("Project exported!")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ExportProjectToGodotOperator)

def unregister():
    bpy.utils.unregister_class(ExportProjectToGodotOperator)

