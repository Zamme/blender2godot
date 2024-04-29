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

class ANIMATIONS_UL_armature_animations(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        custom_icon = 'OUTLINER_DATA_ARMATURE'
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon = custom_icon)
            #if item.name != "B2G_GameManager":
                #layout.prop(item, "scene_type", text="")
                #layout.prop(item, "scene_exportable")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = custom_icon)

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
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="ARMATURE_DATA")        
    
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
        if scene.player_object == None:
            box.label(text="No player object assigned", icon="ERROR")
        else:
            if scene.player_object.type != "ARMATURE":
                _mess = "No armature in player object."
                _ic = "ERROR"
                box.label(text=_mess, icon=_ic)
            else:
                _mess = "Player armature : " + scene.player_object.name
                _ic = "OUTLINER_OB_ARMATURE"
                box1 = box.box()
                box1.template_list("ANIMATIONS_UL_armature_animations", "PlayerAnimationsList", scene.player_object.animation_data, "nla_tracks", scene, "player_animation_sel")
                box.label(text=_mess, icon=_ic)

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
    bpy.types.Scene.player_animation_sel = bpy.props.IntProperty(name="Player Selected Animation", default=0)

def register():
    init_properties()
    bpy.utils.register_class(ANIMATIONS_UL_armature_animations)
    bpy.utils.register_class(PlayerPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(PlayerPropertiesPanel)
    bpy.utils.unregister_class(ANIMATIONS_UL_armature_animations)


