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

import os
import subprocess

import bpy
from bpy.types import Context


class OpenGodotProjectFolderOperator(bpy.types.Operator):
    """Open Godot Project Folder Operator"""
    bl_idname = "scene.open_godot_project_folder_operator"
    bl_label = "Open Godot Project Folder"

    def main(self, context):
        print("Open folder")
        bpy.ops.wm.path_open(filepath=context.scene.project_folder)     

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}

class OpenGodotBuildsFolderOperator(bpy.types.Operator):
    """Open Godot Builds Folder Operator"""
    bl_idname = "scene.open_godot_builds_folder_operator"
    bl_label = "Open Godot Builds Folder"

    @classmethod 
    def poll(self, context):
        return os.path.isdir(context.scene.game_exports_path)
        
    def main(self, context):
        print("Open folder")
        bpy.ops.wm.path_open(filepath=context.scene.game_exports_path)     

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}

class BuildGameOperator(bpy.types.Operator):
    """Build Game Operator"""
    bl_idname = "scene.build_game_operator"
    bl_label = "Build Game"
    
    export_presets_dir_path = ""
    total_file_content = []
    android_preset_content = []
    linux_preset_content = []
    windows_preset_content = []
    mac_preset_content = []
    web_preset_content = []
    exes_dirname = "builds"
    android_exe_dirname = "android_build"
    linux_exe_dirname = "linux_build"
    windows_exe_dirname = "windows_build"
    mac_exe_dirname = "mac_build"
    web_exe_dirname = "web_build"

    _exporting = False


    @classmethod 
    def poll(self, context):
        return (context.scene.android_export or context.scene.linux_export
                 or context.scene.mac_export or context.scene.windows_export
                 or context.scene.web_export)
    
    def add_android_preset(self, context):
        self.android_preset_content.clear()
        self.android_preset_filepath = os.path.join(self.export_presets_dir_path, "android_preset.cfg")
        preset_file = open(self.android_preset_filepath, "r")
        self.android_preset_content = preset_file.readlines()
        preset_file.close()
    
    def add_linux_preset(self, context):
        self.linux_preset_content.clear()
        self.linux_preset_filepath = os.path.join(self.export_presets_dir_path, "linux_preset.cfg")
        preset_file = open(self.linux_preset_filepath, "r")
        self.linux_preset_content = preset_file.readlines()
        preset_file.close()

    def add_mac_preset(self, context):
        self.mac_preset_content.clear()
        self.mac_preset_filepath = os.path.join(self.export_presets_dir_path, "mac_preset.cfg")
        preset_file = open(self.mac_preset_filepath, "r")
        self.mac_preset_content = preset_file.readlines()
        preset_file.close()
    
    def add_preset_content(self, context, preset_content, preset_number):
        for n_line in range(0, len(preset_content)):
            phrase = preset_content[n_line]
            if phrase.startswith("[preset.") and not phrase.endswith("options]\n"):
                new_phrase = "[preset." + str(preset_number) + "]"
                phrase = new_phrase
            if phrase.startswith("[preset.") and phrase.endswith("options]\n"):
                new_phrase = "[preset." + str(preset_number) + ".options]"
                phrase = new_phrase
            self.total_file_content.append(phrase)
        self.total_file_content.append("\n")
    
    def add_selected_export_presets(self, context):
        self.total_file_content.clear()
        self.android_preset_content.clear()
        self.linux_preset_content.clear()
        self.windows_preset_content.clear()
        self.mac_preset_content.clear()
        self.web_preset_content.clear()
        n_versions = 0
        if context.scene.android_export:
            print("Android version...OK")
            self.add_android_preset(context)
            n_versions += 1
        if context.scene.linux_export:
            print("Linux version...OK")
            self.add_linux_preset(context)
            n_versions += 1
        if context.scene.windows_export:
            print("Windows version...OK")
            self.add_windows_preset(context)
            n_versions += 1
        if context.scene.mac_export:
            print("Mac version...OK")
            self.add_mac_preset(context)
            n_versions += 1
        if context.scene.web_export:
            print("Web version...OK")
            self.add_web_preset(context)
            n_versions += 1
        print(n_versions, "versions to export")
        self.config_presets(context)
        #print(self.total_file_content)
        self.fill_total_content(context)
        self.write_export_presets(context)        
    
    def add_web_preset(self, context):
        self.web_preset_content.clear()
        self.web_preset_filepath = os.path.join(self.export_presets_dir_path, "web_preset.cfg")
        preset_file = open(self.web_preset_filepath, "r")
        self.web_preset_content = preset_file.readlines()
        preset_file.close()

    def add_windows_preset(self, context):
        self.windows_preset_content.clear()
        self.windows_preset_filepath = os.path.join(self.export_presets_dir_path, "windows_preset.cfg")
        preset_file = open(self.windows_preset_filepath, "r")
        self.windows_preset_content = preset_file.readlines()
        preset_file.close()
    
    def build_game(self, context):
        print("Building game...")
        print("Creating presets...")
        self.find_preset_dir_path(context)
        self.export_presets_filepath = os.path.join(context.scene.project_folder, "export_presets.cfg")
        self.add_selected_export_presets(context)
        print("Compiling...")
        bpy.ops.scene.compile_selected_versions_operator('INVOKE_DEFAULT')
        
    def config_presets(self, context):
        # Config all presets paths and properties on self.<content> files
        context.scene.game_exports_path = os.path.join(context.scene.game_folder, self.exes_dirname)
        # Android
        context.scene.android_exports_path = os.path.join(context.scene.game_exports_path, self.android_exe_dirname)
        for n_line in range(0, len(self.android_preset_content)):
            if self.android_preset_content[n_line].find("export_path") > -1:
                self.android_preset_content[n_line] = 'export_path="' + context.scene.android_exports_path + '"\n'
        # Linux
        context.scene.linux_exports_path = os.path.join(context.scene.game_exports_path, self.linux_exe_dirname)
        for n_line in range(0, len(self.linux_preset_content)):
            if self.linux_preset_content[n_line].find("export_path") > -1:
                self.linux_preset_content[n_line] = 'export_path="' + context.scene.linux_exports_path + '"\n'          
        # Windows
        context.scene.windows_exports_path = os.path.join(context.scene.game_exports_path, self.windows_exe_dirname)
        for n_line in range(0, len(self.windows_preset_content)):
            if self.windows_preset_content[n_line].find("export_path") > -1:
                self.windows_preset_content[n_line] = 'export_path="' + context.scene.windows_exports_path + '"\n'
        # Mac
        context.scene.mac_exports_path = os.path.join(context.scene.game_exports_path, self.mac_exe_dirname)
        for n_line in range(0, len(self.mac_preset_content)):
            if self.mac_preset_content[n_line].find("export_path") > -1:
                self.mac_preset_content[n_line] = 'export_path="' + context.scene.mac_exports_path + '"\n'
        # Web
        context.scene.web_exports_path = os.path.join(context.scene.game_exports_path, self.web_exe_dirname)
        for n_line in range(0, len(self.web_preset_content)):
            if self.web_preset_content[n_line].find("export_path") > -1:
                self.web_preset_content[n_line] = 'export_path="' + context.scene.web_exports_path + '"\n'
    
    def fill_total_content(self, context):
        n_preset = 0
        if len(self.android_preset_content) > 0:
            self.add_preset_content(context, self.android_preset_content, n_preset)
            n_preset += 1
        if len(self.linux_preset_content) > 0:
            self.add_preset_content(context, self.linux_preset_content, n_preset)
            n_preset += 1
        if len(self.windows_preset_content) > 0:
            self.add_preset_content(context, self.windows_preset_content, n_preset)
            n_preset += 1
        if len(self.mac_preset_content) > 0:
            self.add_preset_content(context, self.mac_preset_content, n_preset)
            n_preset += 1
        if len(self.web_preset_content) > 0:
            self.add_preset_content(context, self.web_preset_content, n_preset)
            n_preset += 1
        
    def find_preset_dir_path(self, context):
        possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "exporting_presets"),
        os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "exporting_presets")]
        for p_path in possible_paths:
            print("Possible path: ", p_path)
            if os.path.isdir(p_path):
                self.export_presets_dir_path = p_path
        print("Export presets directory:", self.export_presets_dir_path)
    
    def write_export_presets(self, context):
        os.remove(self.export_presets_filepath)
        self.presets_file = open(self.export_presets_filepath, "w")
        self.presets_file.writelines(self.total_file_content)
        
    #def main(self, context):
        #bpy.ops.b2g_message.export_confirm_dialogbox('INVOKE_DEFAULT')

    def modal(self, context, event):
        if context.scene.export_action_confirmed:
            self.build_game(context)
            return {'FINISHED'}
        else:
            return {'PASS_THROUGH'}
     
    def invoke(self, context, event):
        context.scene.export_action_confirmed = False
        bpy.ops.b2g_message.export_confirm_dialogbox('INVOKE_DEFAULT')
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class GameExportPanel(bpy.types.Panel):
    """Game Export Panel"""
    bl_label = "Game Export"
    bl_idname = "GAMEEXPORT_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 6

    @classmethod 
    def poll(self, context):
        return ((context.scene.name == context.scene.gamemanager_scene_name) and (bpy.data.is_saved))
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="EXPORT")        

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if not bpy.data.is_saved:       
            return

        if context.scene.godot_exporting:       
            layout.enabled = False
        else:
            layout.enabled = True

        # Export platforms box
        row = layout.row()
        box1 = row.box()
        box1.alignment = "CENTER"
        box2 = box1.box()
        box2.alignment = "LEFT"
        if (os.path.isdir(context.scene.project_folder) and (context.scene.godot_export_ok)):
            box2.label(text="Export platforms:")
            box2.label(text="Be sure that godot export templates are installed!", icon="QUESTION")
            row1 = box2.row()
            row1.alignment = "LEFT"
            grid1 = row1.grid_flow()
            box3 = grid1.box()
            box3.alignment = "LEFT"
            box3.prop(scene, "linux_export")
            box4 = grid1.box()
            box4.alignment = "LEFT"
            box4.prop(scene, "windows_export")
            box5 = grid1.box()
            box5.alignment = "LEFT"
            box5.prop(scene, "mac_export")
            box6 = grid1.box()
            box6.alignment = "LEFT"
            box6.prop(scene, "web_export")
            box7 = grid1.box()
            box7.alignment = "LEFT"
            box7.prop(scene, "android_export")
            if scene.android_export:
                box3 = box2.box()
                box3.prop(scene, "android_sdk_dirpath")
                box3.operator("wm.url_open", text="Help with Android SDK").url = "https://www.zammedev.com/home/wip_projects/blender2godot"
                box3.prop(scene, "android_jdk_dirpath")
                box3.operator("wm.url_open", text="Help with JDK").url = "https://www.zammedev.com/home/wip_projects/blender2godot"
                box3.prop(scene, "android_debug_keystore_filepath")
                box3.operator("wm.url_open", text="Help with Debug Keystore").url = "https://www.zammedev.com/home/wip_projects/blender2godot"
            box7.enabled = False # TODO: Android export disabled

            # Build game button
            row = box1.row()
            row.scale_y = 2.0
            row.operator_context = "INVOKE_DEFAULT"
            row.operator("scene.build_game_operator", icon="MOD_BUILD")

            # Godot Templates Link
            row2 = box1.row()
            row2.alignment="CENTER"
            row2.operator("wm.url_open", text="Godot export templates link", icon="URL").url = "https://www.zammedev.com/home/wip_projects/blender2godot#h.z8i36npe1lzc"

            # Open folders buttons
            row2.operator("scene.open_godot_builds_folder_operator", icon="FOLDER_REDIRECT")
        else:
            box2.label(text="Export to Godot project before build game", icon="ERROR")
        if context.scene.is_game_exporting:
            box1.enabled = False
            box2.label(text="Exporting game ...")
        else:
            box1.enabled = True

class CompileSelectedVersionsOperator(bpy.types.Operator):
    bl_idname = "scene.compile_selected_versions_operator"
    bl_label = "Selected Versions Compile Operator"

    available_platforms = ["Android", "Linux", "Windows", "Mac", "Web"]
    pending_platforms = []
    all_compiled = False
    is_compiling = False
    
    def __init__(self):
        print("Start exporting...")

    def __del__(self):
        print("Exporting finished.")

    def compile_exe(self, context):
        if context.scene.current_version_compiling == "Android":
            #bpy.ops.b2g_message.messagebox(message="Compiling Android Version ...")
            if not os.path.isdir(context.scene.android_exports_path):
                os.mkdir(context.scene.android_exports_path)
            print("Android version...OK")
            context.scene.android_exe_filepath = os.path.join(context.scene.android_exports_path, context.scene.game_name)
            context.scene.android_exe_filepath = context.scene.android_exe_filepath + ".apk"
            self.process = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "--no-window", "--path", context.scene.project_folder, "--export-debug", "Android", context.scene.android_exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Android version exported at :", context.scene.android_exports_path)
        elif context.scene.current_version_compiling == "Linux":
            #bpy.ops.b2g_message.messagebox(message="Compiling Linux Version ...")
            if not os.path.isdir(context.scene.linux_exports_path):
                os.mkdir(context.scene.linux_exports_path)
            print("Linux version...OK")
            context.scene.linux_exe_filepath = os.path.join(context.scene.linux_exports_path, context.scene.game_name)
            self.process = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "-v", "--no-window", "--path", context.scene.project_folder, "--export", "Linux/X11", context.scene.linux_exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            #print("STDOUT:", self.process.stdout)
            print("Linux version exported at :", context.scene.linux_exports_path)
        elif context.scene.current_version_compiling == "Windows":
            #bpy.ops.b2g_message.messagebox(message="Compiling Windows Version ...")
            if not os.path.isdir(context.scene.windows_exports_path):
                os.mkdir(context.scene.windows_exports_path)
            print("Windows version...OK")
            context.scene.windows_exe_filepath = os.path.join(context.scene.windows_exports_path, context.scene.game_name)
            context.scene.windows_exe_filepath = context.scene.windows_exe_filepath + ".exe"
            self.process = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "-v", "--no-window", "--path", context.scene.project_folder, "--export", "Windows Desktop", context.scene.windows_exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Windows version exported at :", context.scene.windows_exports_path)
        elif context.scene.current_version_compiling == "Mac":
            #bpy.ops.b2g_message.messagebox(message="Compiling Mac Version ...")
            if not os.path.isdir(context.scene.mac_exports_path):
                os.mkdir(context.scene.mac_exports_path)
            print("Mac version...OK")
            context.scene.mac_exe_filepath = os.path.join(context.scene.mac_exports_path, context.scene.game_name)
            context.scene.mac_exe_filepath = context.scene.mac_exe_filepath + ".zip"
            self.process = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "--no-window", "--path", context.scene.project_folder, "--export", "Mac OSX", context.scene.mac_exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("MacOS version exported at :", context.scene.mac_exports_path)
        elif context.scene.current_version_compiling == "Web":
            #bpy.ops.b2g_message.messagebox(message="Compiling Web Version ...")
            if not os.path.isdir(context.scene.web_exports_path):
                os.mkdir(context.scene.web_exports_path)
            print("Web version...OK")
            context.scene.web_exe_filepath = os.path.join(context.scene.web_exports_path, context.scene.game_name)
            context.scene.web_exe_filepath += ".html"
            self.process = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "--no-window", "--path", context.scene.project_folder, "--export", "HTML5", context.scene.web_exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Web version exported at :", context.scene.web_exports_path)
        #return {'FINISHED'}

    def create_builds_folder(self, context):
        if not os.path.isdir(context.scene.game_exports_path):
            os.mkdir(context.scene.game_exports_path)

    def set_pending_platforms(self, context):
        self.pending_platforms.clear()
        if context.scene.android_export:
            self.pending_platforms.append(self.available_platforms[0])
        if context.scene.linux_export:
            self.pending_platforms.append(self.available_platforms[1])
        if context.scene.windows_export:
            self.pending_platforms.append(self.available_platforms[2])
        if context.scene.mac_export:
            self.pending_platforms.append(self.available_platforms[3])
        if context.scene.web_export:
            self.pending_platforms.append(self.available_platforms[4])
        print("Pending versions: ", self.pending_platforms)

    def modal(self, context, event):
        if self.all_compiled == True:
            print("Processes completed")
            context.window.cursor_set(cursor="DEFAULT")
            context.window.cursor_modal_restore()
            context.scene.is_game_exporting = False
            return {'FINISHED'}
        
        if event.type == "ESC":
            print("Processes cancelled")
            return {'CANCEL'}
        
        if len(self.pending_platforms) > 0:
            if self.process is None:
                print("Process None")
                context.scene.current_version_compiling = self.pending_platforms.pop()
                self.compile_exe(context)
            else:
                if self.process.poll() == 0:
                    print("Process Next")
                    context.scene.current_version_compiling = self.pending_platforms.pop()
                    self.compile_exe(context)
            return {'PASS_THROUGH'}
        else:
            self.all_compiled = True
            print("Processes completed")
            context.window.cursor_set(cursor="DEFAULT")
            context.window.cursor_modal_restore()
            context.scene.is_game_exporting = False
            return {'FINISHED'}

    def invoke(self, context, event):
        context.window.cursor_set(cursor="WAIT")
        context.window.cursor_modal_set(cursor="WAIT")
        context.scene.is_game_exporting = True
        self.all_compiled = False
        self.process = None
        self.create_builds_folder(context)
        self.set_pending_platforms(context)
        #self.execute(context)
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

class ExportConfirmDailogBoxOperator(bpy.types.Operator):
    bl_idname = "b2g_message.export_confirm_dialogbox"
    bl_label = "Build Game"
 
    message : bpy.props.StringProperty(
        name = "b2g_message",
        description = "message",
        default = ''
    ) # type: ignore
 
    _platforms_array = []
    _platforms_string = ""

    def execute(self, context):
        context.scene.export_action_confirmed = True
        #bpy.ops.b2g_message.export_state_dialogbox('INVOKE_DEFAULT')
        return {'FINISHED'}
 
    def invoke(self, context, event):
        self._platforms_array.clear()
        if context.scene.android_export:
            self._platforms_array.append("Android")
        if context.scene.linux_export:
            self._platforms_array.append("Linux")
        if context.scene.windows_export:
            self._platforms_array.append("Windows")
        if context.scene.mac_export:
            self._platforms_array.append("MacOS")
        if context.scene.web_export:
            self._platforms_array.append("Web")
        for _ind,_pl in enumerate(self._platforms_array):
            if _ind > 0:
                self._platforms_string += ", "
            self._platforms_string += _pl
            if _ind == len(self._platforms_array)-1:
                self._platforms_string += "."
        return context.window_manager.invoke_props_dialog(self, width = 500)
 
    def draw_header(self, context):
        self.layout.label(text="Build Game", icon="INFO")

    def draw(self, context):
        layout = self.layout
        row0 = layout.row()
        box0 = row0.box()
        box0.label(text="Platforms", icon="INFO")
        box1 = box0.box()
        box1.label(text=self._platforms_string)
        box0.label(text="Are you sure? Past builds will be overwritten.", icon="ERROR")

class ExportStateDailogBoxOperator(bpy.types.Operator):
    bl_idname = "b2g_message.export_state_dialogbox"
    bl_label = "Building Game State"
 
    @classmethod
    def poll(cls, context):
        return True
    
    def execute(self, context):
        # Cancel compilation
        #context.scene.export_action_confirmed = True
        return {'FINISHED'}
 
    def invoke(self, context, event):
        #return context.window_manager.invoke_confirm(self, event)
        return context.window_manager.invoke_props_dialog(self, width = 500)
 
    def draw_header(self, context):
        self.layout.label(text="Building Game State", icon="INFO")

    def draw(self, context):
        layout = self.layout
        row0 = layout.row()
        box0 = row0.box()
        box0.label(text="Compilation", icon="INFO")
        #box1 = box0.box()
        #box1.label(text=self._platforms_string)
        #box0.label(text="Are you sure? All past builds will be deleted.", icon="ERROR")


'''
class CompilingStateMessageBoxOperator(bpy.types.Operator):
    bl_idname = "b2g_message.messagebox"
    bl_label = ""

    message : bpy.props.StringProperty(name="MessageBox Message")

    def execute(self, context):
        def draw(self, context):
            self.layout.label(text=self.self.message)
        context.window_manager.popup_menu(draw, title="Compiling...", icon='INFO')
        return {'FINISHED'}
'''
def init_properties():
    bpy.types.Scene.export_action_confirmed = bpy.props.BoolProperty("ExportActionConfirmed", default=False)
    bpy.types.Scene.is_game_exporting = bpy.props.BoolProperty("Is Game Exporting", default=False)
    # Export vars
    # Checkboxes
    bpy.types.Scene.android_export = bpy.props.BoolProperty(name="Android", default=False)
    bpy.types.Scene.linux_export = bpy.props.BoolProperty(name="Linux", default=False)
    bpy.types.Scene.windows_export = bpy.props.BoolProperty(name="Windows", default=False)
    bpy.types.Scene.mac_export = bpy.props.BoolProperty(name="Mac", default=False)
    bpy.types.Scene.web_export = bpy.props.BoolProperty(name="Web", default=False)
    # Paths
    bpy.types.Scene.android_exe_filepath = bpy.props.StringProperty(name="AndroidExeFilepath", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.linux_exe_filepath = bpy.props.StringProperty(name="LinuxExeFilepath", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.windows_exe_filepath = bpy.props.StringProperty(name="WindowsExeFilepath", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.mac_exe_filepath = bpy.props.StringProperty(name="MacExeFilepath", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.web_exe_filepath = bpy.props.StringProperty(name="WebExeFilepath", subtype="FILE_PATH", default=" ")
    bpy.types.Scene.current_version_compiling = bpy.props.StringProperty(name="CurrentVersionCompiling", default=" ")
    bpy.types.Scene.game_exports_path = bpy.props.StringProperty(name="GameExportsPath", default=" ")
    bpy.types.Scene.android_exports_path = bpy.props.StringProperty(name="AndroidExportPath", default=" ")
    bpy.types.Scene.linux_exports_path = bpy.props.StringProperty(name="LinuxExportPath", default=" ")
    bpy.types.Scene.windows_exports_path = bpy.props.StringProperty(name="WindowsExportPath", default=" ")
    bpy.types.Scene.mac_exports_path = bpy.props.StringProperty(name="MacExportPath", default=" ")
    bpy.types.Scene.web_exports_path = bpy.props.StringProperty(name="WebExportPath", default=" ")
    # Android environment vars
    bpy.types.Scene.android_sdk_dirpath = bpy.props.StringProperty(name="Android SDK Folder", subtype="DIR_PATH", default=" ")
    bpy.types.Scene.android_jdk_dirpath = bpy.props.StringProperty(name="JDK Folder", subtype="DIR_PATH", default=" ")
    bpy.types.Scene.android_debug_keystore_filepath = bpy.props.StringProperty(name="Debug Keystore", subtype="FILE_PATH", default=" ")

def clear_properties():
    del bpy.types.Scene.android_export
    del bpy.types.Scene.linux_export
    del bpy.types.Scene.windows_export
    del bpy.types.Scene.mac_export
    del bpy.types.Scene.web_export
    del bpy.types.Scene.android_exe_filepath
    del bpy.types.Scene.linux_exe_filepath
    del bpy.types.Scene.windows_exe_filepath
    del bpy.types.Scene.mac_exe_filepath
    del bpy.types.Scene.web_exe_filepath
    del bpy.types.Scene.current_version_compiling
    del bpy.types.Scene.game_exports_path
    del bpy.types.Scene.android_exports_path
    del bpy.types.Scene.linux_exports_path
    del bpy.types.Scene.windows_exports_path
    del bpy.types.Scene.mac_exports_path
    del bpy.types.Scene.web_exports_path
    del bpy.types.Scene.android_sdk_dirpath
    del bpy.types.Scene.android_jdk_dirpath
    del bpy.types.Scene.android_debug_keystore_filepath

def register():
    init_properties()
    #bpy.utils.register_class(CompilingStateMessageBoxOperator)
    bpy.utils.register_class(ExportStateDailogBoxOperator)
    bpy.utils.register_class(ExportConfirmDailogBoxOperator)
    bpy.utils.register_class(CompileSelectedVersionsOperator)
    bpy.utils.register_class(OpenGodotProjectFolderOperator)
    bpy.utils.register_class(OpenGodotBuildsFolderOperator)
    bpy.utils.register_class(BuildGameOperator)
    bpy.utils.register_class(GameExportPanel)

def unregister():
    bpy.utils.unregister_class(GameExportPanel)
    bpy.utils.unregister_class(BuildGameOperator)
    bpy.utils.unregister_class(OpenGodotProjectFolderOperator)
    bpy.utils.unregister_class(OpenGodotBuildsFolderOperator)
    bpy.utils.unregister_class(CompileSelectedVersionsOperator)
    bpy.utils.unregister_class(ExportConfirmDailogBoxOperator)
    bpy.utils.unregister_class(ExportStateDailogBoxOperator)
    #bpy.utils.unregister_class(CompilingStateMessageBoxOperator)
    clear_properties()