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
from bpy.types import Context


def show_error_popup(message = [], title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        for _error in message:
           self.layout.label(text=_error, icon="ERROR")
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

class ExportProjectToGodotOperator(bpy.types.Operator):
    """Export Project To Godot Operator"""
    bl_idname = "scene.export_project_to_godot_operator"
    bl_label = "Export To Godot"
    
    _errors = []
    _last_export_state = False

    @classmethod 
    def poll(self, context):
        cond1 = (context.scene.name == context.scene.gamemanager_scene_name)
        cond2 = (bpy.data.is_saved)
        cond3 = (bpy.data.scenes[context.scene.gamemanager_scene_name].startup_scene != None)
        return (cond1 and cond2 and cond3)
    
    def check_conditions(self, context):
        self._errors = []

        _tr = context.scene.current_template_requirements.template_requirements

        # Check game name
        if context.scene.game_name == "":
            self._errors.append("Game name not set")
        # Check minimum scenes
        _min_scenes = []
        for _reqs in _tr:
            print("Searching in:", _reqs.name)
            if _reqs.name == "project_export":
                for _index,_value in enumerate(_reqs.requirements):
                    _min_scenes.append(_value.value.lower())
                break
        for _scene in bpy.data.scenes:
            if _scene.scene_exportable:
                if _scene.scene_type in _min_scenes:
                    _min_scenes.remove(_scene.scene_type)
        if len(_min_scenes) > 0:
            for _min_scene in _min_scenes:
                _lack = _min_scene.capitalize() + " type scene needed"
                self._errors.append(_lack)
        # Check one exportable player only
        players_amount = 0
        for _reqs in _tr:
            print("Searching in:", _reqs.name)
            if _reqs.name == "players_amount":
                players_amount = int(_reqs.requirements[0].value)
                print("Players amount:", players_amount)
        for _scene in bpy.data.scenes:
            if _scene.name == self.name:
                        pass
            else:
                if _scene.scene_type == "player":
                    if _scene.scene_exportable:
                        players_amount -= 1
        if players_amount > 0:
            self._errors.append("Need more exportable players")
        elif players_amount < 0:
            self._errors.append("Too many exportable players")
        return self._errors
        
        '''
    def modal(self, context, event):
        return {'PASS_THROUGH'}
    
    def invoke(self, context, event):
            return {'CANCELLED'}
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "No active object, could not finish")
            return {'CANCELLED'}
        '''

    def cancel(self, context):
        context.scene.godot_export_ok = self._last_export_state
        context.scene.godot_exporting = False
        return {'CANCELLED'}
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Godot project will be overwritten", icon="ERROR")
    
    def invoke(self, context, event):
        self._last_export_state = context.scene.godot_export_ok
        context.scene.godot_export_ok = False
        context.scene.godot_exporting = True
        return context.window_manager.invoke_props_dialog(self)
    
    def execute(self, context):
        checked_errors = self.check_conditions(context)
        if len(checked_errors) == 0:
            print("Deleting last export...")
            bpy.ops.scene.delete_project_operator()
            print("Last export deleted!")
            print("Exporting to godot project...")
            bpy.ops.scene.create_godot_project_operator()
            bpy.ops.scene.export_game_operator()
            bpy.ops.scene.open_godot_project_operator(no_window = True)
        else:
            show_error_popup(self._errors, "Errors detected", "CANCEL")
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ExportProjectToGodotOperator)

def unregister():
    bpy.utils.unregister_class(ExportProjectToGodotOperator)

