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
from blender2godot.addon_config import addon_config # type: ignore


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
        self.check_naming_conventions(context)
        if context.scene.game_name == "":
            self.add_error(context, 8, "Project has no name")
        ''' TODO: CHANGE THIS FOR GAMEMANAGER NODES START
        if (context.scene.startup_scene == None):
            self.add_warning(context, 2, "Startup scene not set")
            if hasattr(context.scene.startup_scene, "scene_type"):
                if (context.scene.startup_scene.scene_type == "player"):
                    self.add_warning(context, 3, "Startup scene can't be a player")
        '''
        if (context.scene.godot_engine_ok == False):
            self.add_error(context, 4, "Godot Engine not set")
        for _scene in bpy.data.scenes:
            if _scene.scene_exportable:
                self.check_scene_requirements(context, _scene)

    def check_naming_conventions(self, context):
        _invalid_characters = [".", ":", "@", '"', "/", "%"]
        _objects_with_bad_name = []
        for _scene in bpy.data.scenes:
            for _object in _scene.objects:
                for _inv_char in _invalid_characters:
                    if (_object.name.find(_inv_char) > -1):
                        _objects_with_bad_name.append([_object.name, _scene.name])
                        break
        if len(_objects_with_bad_name) > 0:
            self.add_error(context, 20, 'Bad naming objects: (".", ":", "@", "/", "%")')
            for _bno in _objects_with_bad_name:
                self.add_error(context, 21, _bno[0] + " from scene " + _bno[1])

    def check_scene_requirements(self, context, _scene):
        match _scene.scene_type:
            case "player":
                if not _scene.player_object:
                    self.add_error(context, 5, "Player object lacks on " + _scene.name)
                if not _scene.camera_object:
                    self.add_warning(context, 6, _scene.name + " scene has no camera")
                if len(_scene.controls_settings) < 0:
                    self.add_error(context, 7, _scene.name + " player has no controls")
            case "2dmenu":
                if len(_scene.objects) == 0:
                    self.add_error(context, 9, _scene.name + " scene is empty")
                else:
                    _cameras = 0
                    for _child in _scene.objects:
                        match _child.type:
                            case "CAMERA":
                                _cameras += 1
                            case "GPENCIL":
                                match _child.menu2d_object_properties.menu2d_object_type:
                                    case "button":
                                        match _child.menu2d_object_properties.button_action:
                                            case "load_stage":
                                                if _child.menu2d_object_properties.scene_parameter == "none":
                                                    self.add_warning(context, 11, "Load Stage button no linked on " + _scene.name)
                                            case "load_2dmenu":
                                                if _child.menu2d_object_properties.scene_parameter == "none":
                                                    self.add_warning(context, 17, "Load 2D Menu button no linked on " + _scene.name)
                                            case "load_3dmenu":
                                                if _child.menu2d_object_properties.scene_parameter == "none":
                                                    self.add_warning(context, 18, "Load 3D Menu button no linked on " + _scene.name)
                    if _cameras != 1:
                        self.add_error(context, 10, _scene.name + " must have 1 camera")
            case "3dmenu":
                if not _scene.menu_camera_object:
                    self.add_error(context, 12, _scene.name + " menu has no camera assigned")
                _has_meshes = False
                for _object in _scene.objects:
                    if _object.type == "MESH":
                        _has_meshes = True
                        break
                if not _has_meshes:
                    self.add_error(context, 13, _scene.name + " menu has no meshes")
                else:
                    for _object in _scene.objects:
                        if _object.type == "MESH":
                            if hasattr(_object, "special_object_info"):
                                if _object.special_object_info.menu_object_type == "button":
                                    match _object.special_object_info.button_action_on_click:
                                        case "load_stage":
                                            if _object.special_object_info.scene_parameter == "none":
                                                self.add_warning(context, 14, _scene.name + " has load stage with no linked scene")
                                        case "load_2dmenu":
                                            if _object.special_object_info.scene_parameter == "none":
                                                self.add_warning(context, 15, _scene.name + " has load 2d menu with no linked scene")
                                        case "load_3dmenu":
                                            if _object.special_object_info.scene_parameter == "none":
                                                self.add_warning(context, 16, _scene.name + " has load 3d menu with no linked scene")
            case "loading":
                # TODO : Pending to add
                self.add_error(context, 99, "Loading scene type is not available")
            case "npc":
                # TODO : Pending to add
                self.add_error(context, 99, "NPC scene type is not available")

    def cancel(self, context):
        context.scene.godot_export_ok = self._last_export_state
        context.scene.godot_exporting = False
        #return {'CANCELLED'}
    
    def draw(self, context):
        layout = self.layout
        row0 = layout.row()
        box0 = row0.box()
        row1 = box0.row()
        if (len(context.scene.current_export_errors) == 0):
            row1.label(text="No errors", icon_value=addon_config.preview_collections[0]["ok_green"].icon_id)
        else:
            for _issue in context.scene.current_export_errors:
                _new_row = box0.row()
                _new_row.label(text=_issue.description, icon="CANCEL")
        # WARNINGS
        if (len(context.scene.current_export_warnings) > 0):
            for _issue in context.scene.current_export_warnings:
                _new_row = box0.row()
                _new_row.label(text=_issue.description, icon="ERROR")
        # TOTAL REPORT
        row7 = box0.row()
        if (len(context.scene.current_export_warnings) == 0) and (len(context.scene.current_export_errors) == 0):
            row7.label(text="All OK", icon_value=addon_config.preview_collections[0]["ok_green"].icon_id)
        else:
            row7.label(text="There are some issues but you can export", icon="INFO")

        row2 = layout.row()
        row2.label(text="Godot project will be overwritten", icon="ERROR")
    
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
        context.window.cursor_set(cursor="WAIT")
        context.window.cursor_modal_set(cursor="WAIT")
        print("Deleting last export...")
        bpy.ops.scene.delete_project_operator()
        print("Last export deleted!")
        print("Exporting to godot project...")
        bpy.ops.scene.create_godot_project_operator()
        bpy.ops.scene.export_game_operator()
        bpy.ops.scene.open_godot_project_operator(no_window = True)
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

