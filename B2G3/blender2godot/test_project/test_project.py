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
import sys
import contextlib
import socket
from http.server import HTTPServer, SimpleHTTPRequestHandler, test  # type: ignore
from threading import Thread

import bpy
from blender2godot.addon_config import addon_config # type: ignore


t1 = None
t2 = None
testing = None
handler = None
server = None
output = None
server_address = ('127.0.0.1', 8060)

def shell_open(_url):
    if sys.platform == "win32":
        os.startfile(_url)
    else:
        opener = "open" if sys.platform == "darwin" else "xdg-open"
        global output
        output = subprocess.run([opener, _url])
        print("Output:", output)

def close_test():
    global testing, server
    server.shutdown()
    server.server_close()
    testing = False

def exec_test():
    global server, handler, server_address
    handler = CORSRequestHandler
    server = DualStackServer(server_address, handler)
    server.serve_forever()


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


class StopTestBrowserGameOperator(bpy.types.Operator): # It blocks blender execution until game exits
    """Stop Test Browser Game Operator"""
    bl_idname = "scene.stop_test_browser_game_operator"
    bl_label = "Stop Test Browser"

    def execute(self, context):
        global t2, t1
        print("Stopping test browser...")
        t2 = Thread(target=close_test)
        t2.start()
        t2.join()
        t1.join()
        print("Test browser stopped.")
        return {'FINISHED'}

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

    def execute(self, context):
        global t1, testing, server_address
        if not testing:
            print("Starting browser game", context.scene.project_folder)
            self._path = context.scene.web_exe_filepath.rpartition(os.sep)[0]
            print(self._path)
            os.chdir(self._path)
            testing = True
            t1 = Thread(target=exec_test)
            t1.start()
            shell_open(f"http://127.0.0.1:8060")
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
                global testing
                if testing:
                    box.operator("scene.stop_test_browser_game_operator", icon_value=addon_config.preview_collections[0]["godot_icon"].icon_id)
                else:
                    box.operator("scene.test_browser_game_operator", icon_value=addon_config.preview_collections[0]["godot_icon"].icon_id)
        else:
            box.label(text="Export to godot before testing", icon="ERROR")

def register():
    bpy.utils.register_class(StopTestBrowserGameOperator)
    bpy.utils.register_class(TestProjectGameOperator)
    bpy.utils.register_class(TestBrowserGameOperator)
    bpy.utils.register_class(TestGamePanel)

def unregister():
    bpy.utils.unregister_class(TestGamePanel)
    bpy.utils.unregister_class(TestBrowserGameOperator)
    bpy.utils.unregister_class(TestProjectGameOperator)
    bpy.utils.unregister_class(StopTestBrowserGameOperator)
