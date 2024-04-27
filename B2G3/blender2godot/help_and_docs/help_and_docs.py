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
Help and Documentation
"""

import subprocess

import bpy


class B2GDocumentationOperator(bpy.types.Operator):
    """B2G Documentation Operator"""
    bl_idname = "scene.b2g_documentation_operator"
    bl_label = "Documentation"
    
    def go_documentation(self, context):
        bpy.ops.wm.url_open(url = "https://www.zammedev.com/home/wip_projects/blender2godot")
    
    def main(self, context):
        self.go_documentation(context)        

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}

class B2GTutorialsOperator(bpy.types.Operator):
    """B2G Tutorials Operator"""
    bl_idname = "scene.b2g_tutorials_operator"
    bl_label = "Tutorials"
    
    def go_tutorials(self, context):
        bpy.ops.wm.url_open(url = "https://www.zammedev.com/home/wip_projects/blender2godot")
    
    def main(self, context):
        self.go_tutorials(context)        

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}

class B2GRepositoryOperator(bpy.types.Operator):
    """B2G Repository Operator"""
    bl_idname = "scene.b2g_repository_operator"
    bl_label = "Repository"
    
    def go_repository(self, context):
        bpy.ops.wm.url_open(url = "https://github.com/Zamme/blender2godot")
    
    def main(self, context):
        self.go_repository(context)        

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}

class HelpAndDocsPanel(bpy.types.Panel):
    """Help and Docs Panel"""
    bl_label = "Help and Docs"
    bl_idname = "HELPANDDOCS_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 6
    
    def draw_header(self, context):
        layout = self.layout
        layout.template_icon(icon_value=1, scale=1.2)        

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        # Go to documentation button
        row = layout.row()
        row.scale_x = 1.0
        row.scale_y = 1.5
        row.alignment="CENTER"
        box = row.box()
        box.operator("scene.b2g_documentation_operator", icon="DOCUMENTS")
        box.operator("scene.b2g_tutorials_operator", icon="INFO")
        box.operator("scene.b2g_repository_operator", icon="DISC")


def register():
    bpy.utils.register_class(B2GRepositoryOperator)
    bpy.utils.register_class(B2GTutorialsOperator)
    bpy.utils.register_class(B2GDocumentationOperator)
    bpy.utils.register_class(HelpAndDocsPanel)

def unregister():
    bpy.utils.unregister_class(HelpAndDocsPanel)
    bpy.utils.unregister_class(B2GDocumentationOperator)
    bpy.utils.unregister_class(B2GTutorialsOperator)
    bpy.utils.unregister_class(B2GRepositoryOperator)
