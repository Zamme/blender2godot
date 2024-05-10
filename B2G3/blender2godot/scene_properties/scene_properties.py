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
Scene properties panel
"""

import bpy


def on_depsgraph_update(scene):
    #print("DEPSGRAPH!!!")
    bpy.ops.scene.update_scene_resolution_operator()

def show_error_popup(message = [], title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        for _error in message:
           self.layout.label(text=_error, icon="ERROR")
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def scene_emptyobject_poll(self, object):
    return object.type == 'EMPTY'

def update_scene_exportable(self, context):
    if bpy.data.scenes[self.name].scene_type == "player":
        if bpy.data.scenes[self.name].player_object != None:
            print("Updating player scene exportable")
            if bpy.data.scenes[self.name].camera_object == None:
                if bpy.data.scenes[self.name].scene_exportable:
                    bpy.data.scenes[self.name].scene_exportable = False
                    show_error_popup(["Set camera object in player"], "Error detected", "CANCEL")


class UpdateSceneResolutionOperator(bpy.types.Operator):
    bl_idname = "scene.update_scene_resolution_operator"
    bl_label = "Update Scene Resolution"

    def execute(self, context):
        # WATCH FOR CAMERAS RESOLUTION
        if context.active_object:
            if context.active_object.type == 'CAMERA':
                if context.scene.render.resolution_x != bpy.data.scenes["B2G_GameManager"].display_width:
                    context.scene.render.resolution_x = bpy.data.scenes["B2G_GameManager"].display_width
                if context.scene.render.resolution_y != bpy.data.scenes["B2G_GameManager"].display_height:
                    context.scene.render.resolution_y = bpy.data.scenes["B2G_GameManager"].display_height
                #context.active_object.data.sensor_fit = 'VERTICAL'
                #context.active_object.data.sensor_height = 35.0
        return {'FINISHED'}

class ScenePropertiesPanel(bpy.types.Panel):
    """Scene Properties Panel"""
    bl_label = "Scene Properties"
    bl_idname = "SCENEPROPERTIES_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 2

    _gamemanager_added = False
    _not_in_gamemanager = False

    @classmethod 
    def poll(self, context):
        _gm_index = bpy.data.scenes.find(context.scene.gamemanager_scene_name)
        self._gamemanager_added = (_gm_index > -1)
        self._not_in_gamemanager = (context.scene.name != context.scene.gamemanager_scene_name)
        return (self._not_in_gamemanager and self._gamemanager_added)
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="SEQ_PREVIEW")
    
    def draw(self, context):
        layout = self.layout
        
        if not bpy.data.is_saved:       
            return
        
        # SCENE PROPERTIES
        row = layout.row()
        if hasattr(context.scene, "scene_type"):
            row.prop(context.scene, "scene_type")

def init_properties():
    # Scene props
    bpy.types.Scene.scene_exportable = bpy.props.BoolProperty(name="Exportable", default=False, update=update_scene_exportable) # SCENE EXPORTABLE

def clear_properties():
    del bpy.types.Scene.scene_exportable

def register():
    bpy.app.handlers.depsgraph_update_post.append(on_depsgraph_update)
    init_properties()
    bpy.utils.register_class(UpdateSceneResolutionOperator)
    bpy.utils.register_class(ScenePropertiesPanel)

def unregister():
    bpy.utils.unregister_class(ScenePropertiesPanel)
    bpy.utils.unregister_class(UpdateSceneResolutionOperator)
    clear_properties()


