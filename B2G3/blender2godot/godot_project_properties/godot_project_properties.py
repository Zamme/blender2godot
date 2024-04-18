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
    
    def add_lines(self, context, where, new_lines):
        where.append("\n")
        for nl in new_lines:
            where.append(nl)
            where.append("\n")
        where.append("\n")
        return where
    
    def add_lines_at_section(self, context, where, _section, new_lines):
        print("New lines to add:")
        print(new_lines)
        section_index = where.index(_section)
        for _new_line in new_lines:
            where.insert(section_index + 2, _new_line)
        return where
    
    def find_project_template_dir_path(self, context):
        possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "project_template"),
        os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "project_template")]
        for p_path in possible_paths:
            if os.path.isdir(p_path):
                self.godot_project_template_path = p_path
        print("Godot project template directory:", self.godot_project_template_path)
        
    def modify_godot_project_file(self, context):
        context.scene.godot_project_filepath = os.path.join(context.scene.project_folder, "project.godot")
        godot_project_file = open(context.scene.godot_project_filepath, "r")
        godot_project_file_content = godot_project_file.readlines()
        godot_project_file.close()
        #print("Content:", godot_project_file_content)
        #print("Lines:", len(godot_project_file_content))

        # Title
        godot_project_file_content = self.replace(context, godot_project_file_content, "Godot_Project-name", context.scene.game_name)

        # Display settings
        print("Adding display lines ...")
        display_lines_to_add = ["[display]"]
        display_lines_to_add.append("window/size/width=" + str(context.scene.display_width))
        display_lines_to_add.append("window/size/height=" + str(context.scene.display_height))
        display_lines_to_add.append("window/size/resizable=" + str(context.scene.display_resizable).lower())
        display_lines_to_add.append("window/size/borderless=" + str(context.scene.display_borderless).lower())
        display_lines_to_add.append("window/size/fullscreen=" + str(context.scene.display_fullscreen).lower())
        display_lines_to_add.append("window/size/always_on_top=" + str(context.scene.display_alwaysontop).lower())
        print("Display lines added.")
        godot_project_file_content = self.add_lines(context, godot_project_file_content, display_lines_to_add)

        # Boot splash settings
        splash_lines_to_add = ["boot_splash/show_image=" + str(context.scene.splash_showimage).lower() + "\n"]
        splash_lines_to_add.append("boot_splash/image=" + '"' + context.scene.splash_imagefilepath + '"' + "\n")
        splash_lines_to_add.append("boot_splash/fullsize=" + str(context.scene.splash_fullsize).lower() + "\n")
        splash_lines_to_add.append("boot_splash/use_filter=" + str(context.scene.splash_usefilter).lower() + "\n")
        #splash_lines_to_add = ["boot_splash/bg_color=" + str(context.scene.splash_bgcolor).lower() + "\n"]
        #print(godot_project_file_content)
        godot_project_file_content = self.add_lines_at_section(context, godot_project_file_content, "[application]\n", splash_lines_to_add)

        print(godot_project_file_content)
        
        # Save File
        os.remove(context.scene.godot_project_filepath)
        f = open(context.scene.godot_project_filepath, "w")
        f.writelines(godot_project_file_content)
        f.close()
    
    def modify_project_information(self, context):
        self.modify_godot_project_file(context)
    
    def replace(self, context, where, this, that):
        for n_line in range(0, len(where)):
            if where[n_line].find(this) > -1:
                #print("Located")
                where[n_line] = where[n_line].replace(this, that)
                #print("Replaced by", that)
        return where
                
    def main(self, context):
        context.scene.game_folder = bpy.path.abspath("//")
        self.find_project_template_dir_path(context)
        context.scene.project_folder = os.path.join(context.scene.game_folder, context.scene.game_name + "_Game")
        self.add_initial_files(context)
        self.modify_project_information(context)

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
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        blend_data = context.blend_data
        
        if bpy.path.abspath("//") == "":       
            return

        row = layout.row()
        row.label(text="Project properties:")
        row = layout.row()
        box1 = row.box()
        # Project properties box
        box1.prop(scene, "game_name")
        #box1.prop(scene, "game_folder")
        row2 = layout.row()
        box2 = row2.box()
        box2.label(text="Icon must be a png image!")
        box2.prop(scene, "game_icon")
        

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


