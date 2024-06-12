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
Testing game 
"""

import subprocess
import os

import contextlib
import socket
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler, test  # type: ignore
from pathlib import Path
from threading import Thread

import bpy
from blender2godot.addon_config import addon_config # type: ignore


### BROWSER SERVER ###
# See cpython GH-17851 and GH-17864.
class DualStackServer(HTTPServer):
    def server_bind(self):
        # Suppress exception when protocol is IPv4.
        with contextlib.suppress(Exception):
            self.socket.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_V6ONLY, 0)
        return super().server_bind()


class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Cross-Origin-Opener-Policy", "same-origin")
        self.send_header("Cross-Origin-Embedder-Policy", "require-corp")
        self.send_header("Access-Control-Allow-Origin", "*")
        super().end_headers()
### END BROWSER SERVER ###


class TestProjectGameOperator(bpy.types.Operator): # It blocks blender execution until game exits
    """Test Project Game Operator"""
    bl_idname = "scene.test_project_game_operator"
    bl_label = "Test Last Exported Project"
    
    def start_project_game(self, context):
        print("Starting project game", context.scene.project_folder)
        self.cmd = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "--path", context.scene.project_folder], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    
    def main(self, context):
        self.start_project_game(context)        

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}

class TestBrowserGameOperator(bpy.types.Operator): # It blocks blender execution until game exits
    """Test Browser Game Operator"""
    bl_idname = "scene.test_browser_game_operator"
    bl_label = "Test Browser Build"

    _output = None
    _testing = False
    _port = 8060
    
    def shell_open(self, context, url):
        if sys.platform == "win32":
            os.startfile(url)
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            self._output = subprocess.run([opener, url])
            print("Output:", self._output)

    def execute(self, context):
        return {'FINISHED'}

    def modal(self, context, event):
        if not self._testing:
            self._testing = True
            self._handler = CORSRequestHandler
            self._dual_stack_server = DualStackServer
            t = Thread(target=test, args=(self._handler, self._dual_stack_server, self._port,))
            t.start()
            test(self._handler, self._dual_stack_server, port=self._port)
            return {'PASS_THROUGH'}
        else:
            print(self._handler)
            return {'FINISHED'}

    def invoke(self, context, event):
        print("Starting browser game", context.scene.project_folder)
        self._path = context.scene.web_exe_filepath.rpartition(os.sep)[0]
        print(self._path)
        os.chdir(self._path)
        self._testing = False
        self.shell_open(context, f"http://127.0.0.1:{self._port}")
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

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
            box.operator("scene.test_project_game_operator", icon="PLAY")
            if os.path.isfile(context.scene.web_exe_filepath + ".html"):
                box.operator_context = 'INVOKE_DEFAULT'
                box.operator("scene.test_browser_game_operator", icon_value=addon_config.preview_collections[0]["godot_icon"].icon_id)
        else:
            box.label(text="Export to godot before testing", icon="ERROR")

def register():
    bpy.utils.register_class(TestProjectGameOperator)
    bpy.utils.register_class(TestBrowserGameOperator)
    bpy.utils.register_class(TestGamePanel)

def unregister():
    bpy.utils.unregister_class(TestGamePanel)
    bpy.utils.unregister_class(TestBrowserGameOperator)
    bpy.utils.unregister_class(TestProjectGameOperator)
