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


def scene_camera_object_poll(self, object):
    return object.type == 'CAMERA'

def scene_player_object_poll(self, object):
    return (object.type == 'MESH' or object.type == 'ARMATURE') 

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
        return (self._not_in_gamemanager and self._gamemanager_added and (context.scene.scene_type == "player"))
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if not bpy.data.is_saved:       
            return

        # INITIAL PROPERTIES
        row = layout.row()
        row.prop(scene, "player_object")
        # Player animations
        row = layout.row()
        box = row.box()
        box.label(text="Animations")

        # Player motion
        row = layout.row()
        box = row.box()
        box.label(text="Player Motion")
        box2 = box.box()
        box2.label(text="Controls")
        box.prop(scene, "player_gravity_on")
        box.prop(scene, "camera_control_inverted")

        # Player camera
        row = layout.row()
        box = row.box()
        box.label(text="Camera Properties")
        box.prop(scene, "camera_object")
        box.prop(scene, "camera_fov")

def init_properties():
    # Player properties
    bpy.types.Scene.player_gravity_on = bpy.props.BoolProperty(name="Gravity", default=True)
    bpy.types.Scene.camera_control_inverted = bpy.props.BoolProperty(name="Camera Inverted", default=True)
    bpy.types.Scene.camera_object = bpy.props.PointerProperty(type=bpy.types.Object, name="Camera Object", description="Camera Object", poll=scene_camera_object_poll)
    bpy.types.Scene.player_object = bpy.props.PointerProperty(type=bpy.types.Object, name="Player Object", description="Player Object", poll=scene_player_object_poll)
    bpy.types.Scene.camera_fov = bpy.props.FloatProperty(name="FOV", default=30.0, min=1.0, max=180.0)

def register():
    init_properties()
    bpy.utils.register_class(PlayerPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(PlayerPropertiesPanel)


