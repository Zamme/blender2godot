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
For player behaviour
"""

import bpy


class PlayerObjects(bpy.types.PropertyGroup):
    """ Player Objects """
    player_objects = [
        ("none", "None", "", "NONE", 0),]

def fill_player_objects_menu(self, context):
    player_objects = []
    player_objects.clear()
    player_objects.append(("None", "None", "None"))
    for ob in bpy.context.scene.objects:
        if ob.type == "CAMERA":
            menu_item = (ob.name, ob.name, ob.name)
            player_objects.append(menu_item)
    return player_objects

class PlayerPropertiesPanel(bpy.types.Panel):
    """Player Properties Panel"""
    bl_label = "Player Properties"
    bl_idname = "PLAYERPROPERTIES_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 3
    
    _gamemanager_added = False
    _not_in_gamemanager = False

    @classmethod 
    def poll(self, context):
        _gm_index = bpy.data.scenes.find(context.scene.gamemanager_scene_name)
        self._gamemanager_added = (_gm_index > -1)
        self._not_in_gamemanager = (context.scene.name != context.scene.gamemanager_scene_name)
        return (self._not_in_gamemanager and self._gamemanager_added and (context.scene.scene_type == "character"))
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        blend_data = context.blend_data
        
        if bpy.path.abspath("//") == "":       
            return

        # INITIAL PROPERTIES
        # Player object
        row = layout.row()
        row.prop(scene, "player_object")
        
        # Player properties
        row = layout.row()
        box = row.box()
        box.prop(scene, "player_gravity_on")
        box.prop(scene, "camera_inverted")

def init_properties():
    # Player properties
    bpy.types.Scene.player_gravity_on = bpy.props.BoolProperty(name="Gravity", default=True)
    bpy.types.Scene.camera_inverted = bpy.props.BoolProperty(name="Camera Inverted", default=True)
    bpy.types.Scene.player_object = bpy.props.EnumProperty(items=fill_player_objects_menu, name="Player", description="Player Object")  

def register():
    init_properties()
    bpy.utils.register_class(PlayerPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(PlayerPropertiesPanel)


