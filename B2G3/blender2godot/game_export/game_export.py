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
import time

import bpy


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
        
    def main(self, context):
        self.find_preset_dir_path(context)
        self.export_presets_filepath = os.path.join(context.scene.project_folder, "export_presets.cfg")
        self.build_game(context)        

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}


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
        layout.template_icon(icon_value=292, scale=1.2)        

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        blend_data = context.blend_data
        
        if not bpy.data.is_saved:       
            return

        # Export platforms box
        row = layout.row()
        box1 = row.box()
        box2 = box1.box()
        box2.label(text="Export platforms:")
        box2.label(text="Be sure that godot export templates are installed!", icon="QUESTION")
        box2.prop(scene, "linux_export")
        box2.prop(scene, "windows_export")
        box2.prop(scene, "mac_export")
        box2.prop(scene, "web_export")
        box2.prop(scene, "android_export")
        if scene.android_export:
            box3 = box2.box()
            box3.prop(scene, "android_sdk_dirpath")
            box3.operator("wm.url_open", text="Help with Android SDK").url = "https://www.zammedev.com/home/wip_projects/blender2godot"
            box3.prop(scene, "android_jdk_dirpath")
            box3.operator("wm.url_open", text="Help with JDK").url = "https://www.zammedev.com/home/wip_projects/blender2godot"
            box3.prop(scene, "android_debug_keystore_filepath")
            box3.operator("wm.url_open", text="Help with Debug Keystore").url = "https://www.zammedev.com/home/wip_projects/blender2godot"
        row = box2.row()
        row.alignment="CENTER"
        row.operator("wm.url_open", text="Godot export templates link", icon="URL").url = "https://www.zammedev.com/home/wip_projects/blender2godot#h.z8i36npe1lzc"
            
        # Build game button
        row = box1.row()
        row.scale_y = 2.0
        row.operator("scene.build_game_operator", icon="MOD_BUILD")

        # Open folders buttons
        row = box1.row()
        row.alignment="CENTER"
        row.operator("scene.open_godot_builds_folder_operator", icon="FOLDER_REDIRECT")


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

    def execute(self, context):
        return {'FINISHED'}
    
    def compile_exe(self, context):
        bpy.ops.message.messagebox()
        if context.scene.current_version_compiling == "Android":
            if not os.path.isdir(context.scene.android_exports_path):
                os.mkdir(context.scene.android_exports_path)
            print("Android version...OK")
            context.scene.android_exe_filepath = os.path.join(context.scene.android_exports_path, context.scene.game_name)
            context.scene.android_exe_filepath = context.scene.android_exe_filepath + ".apk"
            self.process = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "--path", context.scene.project_folder, "--export-debug", "Android", context.scene.android_exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Android version exported at :", context.scene.android_exports_path)
        elif context.scene.current_version_compiling == "Linux":
            if not os.path.isdir(context.scene.linux_exports_path):
                os.mkdir(context.scene.linux_exports_path)
            print("Linux version...OK")
            context.scene.linux_exe_filepath = os.path.join(context.scene.linux_exports_path, context.scene.game_name)
            self.process = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "--path", context.scene.project_folder, "--export", "Linux/X11", context.scene.linux_exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Linux version exported at :", context.scene.linux_exports_path)
        elif context.scene.current_version_compiling == "Windows":
            if not os.path.isdir(context.scene.windows_exports_path):
                os.mkdir(context.scene.windows_exports_path)
            print("Windows version...OK")
            context.scene.windows_exe_filepath = os.path.join(context.scene.windows_exports_path, context.scene.game_name)
            context.scene.windows_exe_filepath = context.scene.windows_exe_filepath + ".exe"
            self.process = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "--path", context.scene.project_folder, "--export", "Windows Desktop", context.scene.windows_exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Windows version exported at :", context.scene.windows_exports_path)
        elif context.scene.current_version_compiling == "Mac":
            if not os.path.isdir(context.scene.mac_exports_path):
                os.mkdir(context.scene.mac_exports_path)
            print("Mac version...OK")
            context.scene.mac_exe_filepath = os.path.join(context.scene.mac_exports_path, context.scene.game_name)
            context.scene.mac_exe_filepath = context.scene.mac_exe_filepath + ".zip"
            self.process = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "--path", context.scene.project_folder, "--export", "Mac OSX", context.scene.mac_exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("MacOS version exported at :", context.scene.mac_exports_path)
        elif context.scene.current_version_compiling == "Web":
            if not os.path.isdir(context.scene.web_exports_path):
                os.mkdir(context.scene.web_exports_path)
            print("Web version...OK")
            context.scene.web_exe_filepath = os.path.join(context.scene.web_exports_path, context.scene.game_name)
            self.process = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "--path", context.scene.project_folder, "--export", "HTML5", context.scene.web_exe_filepath], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print("Web version exported at :", context.scene.web_exports_path)
        return {'FINISHED'}

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
            return {'FINISHED'}
        
        if event.type == "ESC":
            return {'FINISHED'}
        
        if len(self.pending_platforms) > 0:
            if self.process is None:
                context.scene.current_version_compiling = self.pending_platforms.pop()
                self.compile_exe(context)
            else:
                if self.process.poll() == 0:
                    context.scene.current_version_compiling = self.pending_platforms.pop()
                    self.compile_exe(context)
        else:
            self.all_compiled = True
            return {'FINISHED'}
        
        return {'RUNNING_MODAL'}

    def invoke(self, context, event):
        self.all_compiled = False
        self.process = None
        #bpy.ops.message.dialogbox('INVOKE_DEFAULT', message = "Compiling...")
        self.create_builds_folder(context)
        self.set_pending_platforms(context)
        self.execute(context)

        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}
            

class DailogBoxOperator(bpy.types.Operator):
    bl_idname = "message.dialogbox"
    bl_label = ""
 
    message = bpy.props.StringProperty(
        name = "message",
        description = "message",
        default = ''
    )
 
    def execute(self, context):
        self.report({'INFO'}, self.message)
        print(self.message)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self, width = 400)
 
    def draw(self, context):
        self.layout.label(text=self.message)
        self.layout.label(text="")


class MessageBoxOperator(bpy.types.Operator):
    bl_idname = "message.messagebox"
    bl_label = ""
 
    def execute(self, context):
        def draw(self, context):
            self.layout.label(text="Compiling...")
        context.window_manager.popup_menu(draw, title="Compiling...", icon='INFO')
        return {'FINISHED'}

def register():
    bpy.utils.register_class(MessageBoxOperator)
    bpy.utils.register_class(DailogBoxOperator)
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
    bpy.utils.unregister_class(DailogBoxOperator)
    bpy.utils.unregister_class(MessageBoxOperator)
