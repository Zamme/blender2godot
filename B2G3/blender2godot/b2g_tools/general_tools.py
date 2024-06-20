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


def show_error_popup(message = [], title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        for _error in message:
           self.layout.label(text=_error, icon="ERROR")
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

class ExportIssue(bpy.types.PropertyGroup):
    id : bpy.props.IntProperty(name="Export issue id", default=-1)  # type: ignore
    description : bpy.props.StringProperty(name="Export issue description", default="")  # type: ignore

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
        return (cond1 and cond2)
    
    def add_error(self, context, _issue_index, _issue_desc):
            _new_issue = context.scene.current_export_errors.add()
            _new_issue.id = _issue_index
            _new_issue.description = _issue_desc

    def add_warning(self, context, _issue_index, _issue_desc):
            _new_issue = context.scene.current_export_warnings.add()
            _new_issue.id = _issue_index
            _new_issue.description = _issue_desc

    def check_export_requirements(self, context):
        context.scene.current_export_warnings.clear()
        context.scene.current_export_errors.clear()
        if (context.scene.startup_scene == None):
            self.add_warning(context, 2, "Startup scene not set")
            if hasattr(context.scene.startup_scene, "scene_type"):
                if (context.scene.startup_scene.scene_type == "player"):
                    self.add_warning(context, 3, "Startup scene can't be a player")
        if (context.scene.godot_engine_ok == False):
            self.add_error(context, 4, "Godot Engine not set")
        for _scene in bpy.data.scenes:
            self.check_scene_requirements(context, _scene)
        return (len(context.scene.current_export_warnings) == 0)

    def check_scene_requirements(self, context, _scene):
        match _scene.scene_type:
            case "player":
                if not _scene.player_object:
                    self.add_warning(context, 5, "Player object lacks on " + _scene.name)
                else:
                    if not _scene.camera_object:
                        self.add_warning(context, 6, _scene.name + " scene has no camera")
        
    def check_conditions(self, context):
        self._errors = []
        # Check game name
        if context.scene.game_name == "":
            self._errors.append("Game name not set")
        return self._errors

    def cancel(self, context):
        context.scene.godot_export_ok = self._last_export_state
        context.scene.godot_exporting = False
        #return {'CANCELLED'}
    
    def draw(self, context):
        layout = self.layout
        row = layout.row()
        row.label(text="Godot project will be overwritten", icon="ERROR")
    
    def invoke(self, context, event):
        self._last_export_state = context.scene.godot_export_ok
        context.scene.godot_exporting = True
        self.check_export_requirements(context)
        #print("Export Issues:", context.scene.current_export_issues)
        #print(len(context.scene.current_export_issues))
        if (len(context.scene.current_export_errors) == 0):
            return context.window_manager.invoke_props_dialog(self)
        else:
            context.scene.godot_export_ok = self._last_export_state
            context.scene.godot_exporting = False
            return {'CANCELLED'}
    
    def execute(self, context):
        context.scene.godot_export_ok = False
        checked_errors = self.check_conditions(context)
        if len(checked_errors) == 0:
            context.window.cursor_set(cursor="WAIT")
            context.window.cursor_modal_set(cursor="WAIT")
            print("Deleting last export...")
            bpy.ops.scene.delete_project_operator()
            print("Last export deleted!")
            print("Exporting to godot project...")
            bpy.ops.scene.create_godot_project_operator()
            bpy.ops.scene.export_game_operator()
            bpy.ops.scene.open_godot_project_operator(no_window = True)
        else:
            show_error_popup(self._errors, "Errors detected", "CANCEL")
        context.window.cursor_set(cursor="DEFAULT")
        context.window.cursor_modal_restore()
        return {'FINISHED'}


def register():
    bpy.utils.register_class(ExportIssue)
    bpy.types.Scene.current_export_errors = bpy.props.CollectionProperty(type=ExportIssue, name="Export Errors")
    bpy.types.Scene.current_export_warnings = bpy.props.CollectionProperty(type=ExportIssue, name="Export Warnings")
    bpy.utils.register_class(ExportProjectToGodotOperator)

def unregister():
    bpy.utils.unregister_class(ExportProjectToGodotOperator)
    del bpy.types.Scene.current_export_warnings
    del bpy.types.Scene.current_export_errors
    bpy.utils.unregister_class(ExportIssue)

