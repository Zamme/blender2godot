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
NPC properties panel
"""

import bpy
from blender2godot.addon_config import addon_config # type: ignore


class NpcPropertiesPanel(bpy.types.Panel):
    """NPC Properties Panel"""
    bl_label = "NPC Properties"
    bl_idname = "NPCPROPERTIES_PT_layout"
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
            if ((context.scene.scene_type == "npc") and (context.scene.name != context.scene.gamemanager_scene_name)):
                _ret = True
        return _ret
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon_value=addon_config.preview_collections[0]["npc_icon"].icon_id)        
    
    def draw(self, context):
        layout = self.layout
        
        if not bpy.data.is_saved:       
            return
        
        # NPC PROPERTIES
        row = layout.row()
        box0 = row.box()
        row1 = box0.row()
        row1.label(text="NPC Properties")
        row3 = box0.row()
        row3.label(text="TODO")
        return
       
        # ACTIVE OBJECT PROPERTIES
        if context.active_object is not None:
            row = layout.row()
            box = row.box()
            box.label(text="Active Object")
            box3 = box.box()
            box3.label(text=context.active_object.name)
            if context.active_object.godot_exportable:
                box3.prop(context.active_object, "collider")
            box.prop(context.active_object, "godot_exportable")

def init_properties():
    pass

def clear_properties():
    pass

def register():
    init_properties()
    bpy.utils.register_class(NpcPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(NpcPropertiesPanel)
    clear_properties()


