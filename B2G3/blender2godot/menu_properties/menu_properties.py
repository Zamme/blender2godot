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
For menus 
"""

import bpy


class MenuPropertiesPanel(bpy.types.Panel):
    """Menu Properties Panel"""
    bl_label = "Menu Properties"
    bl_idname = "MENUPROPERTIES_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 3
    
    _gamemanager_added = False
    _not_in_gamemanager = False

    @classmethod 
    def poll(self, context):
        _ret = False
        if hasattr(context.scene, "scene_type"):
            if (context.scene.scene_type == "menu"):
                _ret = True
        return _ret
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="OUTLINER")        
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if not bpy.data.is_saved:       
            return

        # INITIAL PROPERTIES


def init_properties():
    pass

def register():
    init_properties()
    bpy.utils.register_class(MenuPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(MenuPropertiesPanel)


