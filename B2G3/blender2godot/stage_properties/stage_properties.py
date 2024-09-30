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
Stage properties panel
"""

import bpy


def show_error_popup(message = [], title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        for _error in message:
           self.layout.label(text=_error, icon="ERROR")
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

def update_scene_exportable(self, context):
    if bpy.data.scenes[self.name].scene_type == "player":
        if bpy.data.scenes[self.name].player_object != None:
            print("Updating player scene exportable")
            if bpy.data.scenes[self.name].camera_object == None:
                if bpy.data.scenes[self.name].scene_exportable:
                    bpy.data.scenes[self.name].scene_exportable = False
                    show_error_popup(["Set camera object in player"], "Error detected", "CANCEL")

class ColliderProperties(bpy.types.PropertyGroup):
    """ Collider properties """
    collider_options = [
        ("none", "None", "", "NONE", 0),
        ("convex", "Convex", "", "CONVEX", 1),
        ("mesh", "Mesh", "", "MESH", 2),
        ("smart", "Smart", "", "SMART", 3)]

class StagePropertiesPanel(bpy.types.Panel):
    """Stage Properties Panel"""
    bl_label = "Stage Properties"
    bl_idname = "STAGEPROPERTIES_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    #bl_options = {"DEFAULT_CLOSED"}
    bl_order = 3

    _gamemanager_added = False
    _not_in_gamemanager = False

    @classmethod 
    def poll(self, context):
        _ret = False
        _gm_index = bpy.data.scenes.find(context.scene.gamemanager_scene_name)
        self._gamemanager_added = (_gm_index > -1)
        if self._gamemanager_added:
            if hasattr(context.scene, "scene_type"):
                if ((context.scene.scene_type == "stage") and (context.scene.name != context.scene.gamemanager_scene_name)):
                    _ret = True
        return _ret
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="SEQ_PREVIEW")
    
    def draw(self, context):
        layout = self.layout
        
        if not bpy.data.is_saved:       
            return
        
        # STAGE PROPERTIES
        row = layout.row()
        # Player spawner
        #row = layout.row()
        #row.prop(context.scene, "player_spawn_empty")
        #if context.scene.player_spawn_empty == None:
            #row = layout.row()
            #row.label(text="Select an EMPTY object as spawn position.", icon="ERROR")
       
        # ACTIVE OBJECT PROPERTIES
        if context.active_object is not None:
            row = layout.row()
            box = row.box()
            box.label(text="Active Object")
            box3 = box.box()
            box3.label(text=context.active_object.name)
            #if context.active_object.godot_exportable:
            box3.prop(context.active_object, "object_type", text="Object Type")
            box3.prop(context.active_object, "is_visible")
            match context.active_object.object_type:
                case "trigger_zone":
                    row0 = box3.row()
                    row0.label(text="Aware Physics Groups:")
                    row1 = box3.row()
                    row1.prop(context.active_object, "physics_group")#, text=context.active_object.physics_group)
                case "entity":
                    row0 = box3.row()
                    row0.label(text="Entity Properties:")
                    for _property in context.active_object.entity_properties:
                        box2 = box3.box()
                        row5 = box2.row()
                        column0 = row5.column()
                        column0.prop(_property, "property_name", text="Name")
                        column1 = row5.column()
                        column1.prop(_property, "property_type")
                        #column2 = row5.column()
                        #column2.prop(_property, "property_value")
                        column3 = row5.column()
                        column3.operator(operator="object.remove_object_entity_property_operator", text="X").prop_to_remove_name = _property.property_name
                    row6 = box3.row()
                    row6.operator("object.add_object_entity_property_operator")
                case _:
                    box3.prop(context.active_object, "collider")
                    if context.active_object.collider != "none":
                        row0 = box3.row()
                        row0.label(text="Physics Groups:")
                        row1 = box3.row()
                        if len(bpy.data.scenes["B2G_GameManager"].physics_groups) > 0:
                            row1.prop(context.active_object, "physics_group")#, text=context.active_object.physics_group)
                        else:
                            row1.label(text="Game Manager physics groups empty!")
            box.prop(context.active_object, "godot_exportable")

def init_properties():
    bpy.types.Object.collider = bpy.props.EnumProperty(
        items = ColliderProperties.collider_options,
        name = "Collider Type",
        description = "Collider type",
        default = "convex")

def clear_properties():
    del bpy.types.Object.collider

def register():
    init_properties()
    bpy.utils.register_class(StagePropertiesPanel)

def unregister():
    bpy.utils.unregister_class(StagePropertiesPanel)
    clear_properties()


