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
For Godot project creation
"""

import os
import shutil

import bpy
from bpy.types import Context

class AreYouSureDeletingOperator(bpy.types.Operator):
    """Really?"""
    bl_idname = "scene.are_you_sure_deleting_operator"
    bl_label = "Are you sure?"
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.scene.delete_project_operator()
        self.report({'INFO'}, "Project deleted!")
        print("Project deleted.")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

class CreateGodotProjectOperator(bpy.types.Operator):
    """Create Godot Project Operator"""
    bl_idname = "scene.create_godot_project_operator"
    bl_label = "Create Project"
    
    project_file = None
    godot_project_template_path = ""
    
    def add_initial_files(self, context):
        if os.path.isdir(context.scene.project_folder):
            print("Folder exists...")
        else:
            print("Creating project tree from template...")
            shutil.copytree(self.godot_project_template_path, context.scene.project_folder)
            print("Godot project tree created.")
    
    def find_project_template_dir_path(self, context):
        possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "project_templates", context.scene.project_template),
        os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "project_templates", context.scene.project_template)]
        for p_path in possible_paths:
            if os.path.isdir(p_path):
                self.godot_project_template_path = p_path
        print("Godot project template directory:", self.godot_project_template_path)
           
    def main(self, context):
        context.scene.game_folder = bpy.path.abspath("//")
        self.find_project_template_dir_path(context)
        context.scene.project_folder = os.path.join(context.scene.game_folder, context.scene.game_name + "_Game")
        self.add_initial_files(context)

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}

class DeleteProjectButtonOperator(bpy.types.Operator): # TODO: PENDING TO FIX PATHS!
    """Delete Project Button Operator"""
    bl_idname = "scene.delete_project_button_operator"
    bl_label = "Delete Project"
    
    def delete_project(self, context):
        if os.path.isdir(context.scene.project_folder):
            print("Deleting project...", context.scene.project_folder)
            bpy.ops.scene.are_you_sure_deleting_operator()
            print("Project deleted")
        else:
            print("Project not found.")
    
    def main(self, context):
        context.scene.game_folder = bpy.path.abspath("//")
        context.scene.project_folder = os.path.join(context.scene.game_folder, context.scene.game_name + "_Game")
        self.delete_project(context)        

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}

class DeleteProjectOperator(bpy.types.Operator):
    """Delete Project Operator"""
    bl_idname = "scene.delete_project_operator"
    bl_label = "Delete Project"
    
    def delete_project(self, context):
        if os.path.isdir(context.scene.project_folder):
            print("Deleting project...", context.scene.project_folder)
            shutil.rmtree(context.scene.project_folder)
            print("Project deleted")
        else:
            print("Project not found.")
        executables_path = os.path.join(context.scene.game_folder, "builds")
        if os.path.isdir(executables_path):
            print("Deleting executables...", executables_path)
            shutil.rmtree(executables_path)
            print("Executables deleted")
        else:
            print("Executables not found.")
    
    def main(self, context):
        self.delete_project(context)        

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}

class GodotProjectPropertiesPanel(bpy.types.Panel):
    """Godot Project Properties Panel"""
    bl_label = "Godot Project Properties"
    bl_idname = "GODOTPROJECTPROPERTIES_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_order = 1
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod 
    def poll(self, context):
        return ((context.scene.name == context.scene.gamemanager_scene_name) and (bpy.data.is_saved))
    
    def draw_header(self, context: Context):
        layout = self.layout
        layout.template_icon(icon_value=67, scale=1.2)        

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if not bpy.data.is_saved:       
            return

        row0 = layout.row()
        # Project properties box
        box1 = row0.box()
        box1.prop(scene, "game_name", icon="TEXT")
        box1.prop(scene, "game_folder", icon="FILE_FOLDER")
        box1.prop(scene, "game_icon", icon="IMAGE")
        if not scene.game_icon.endswith(".png"):
            box1.label(text="Icon must be a png image!")
        box1.prop(scene, "project_template", icon="SHADERFX")
       

def register():
    bpy.utils.register_class(DeleteProjectButtonOperator)
    bpy.utils.register_class(AreYouSureDeletingOperator)
    bpy.utils.register_class(DeleteProjectOperator)
    bpy.utils.register_class(CreateGodotProjectOperator)
    bpy.utils.register_class(GodotProjectPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(DeleteProjectButtonOperator)
    bpy.utils.unregister_class(AreYouSureDeletingOperator)
    bpy.utils.unregister_class(DeleteProjectOperator)
    bpy.utils.unregister_class(CreateGodotProjectOperator)
    bpy.utils.unregister_class(GodotProjectPropertiesPanel)


