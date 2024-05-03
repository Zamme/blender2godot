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

import os

import bpy
from bpy.app.handlers import persistent


def scene_emptyobject_poll(self, object):
    return object.type == 'EMPTY'

def update_scene_exportable(self, context):
    if bpy.data.scenes[self.name].scene_type == "player":
        print("Updating player scene exportable")
        if bpy.data.scenes[self.name].camera_object == None:
            if bpy.data.scenes[self.name].scene_exportable:
                bpy.data.scenes[self.name].scene_exportable = False
        

class ColliderProperties(bpy.types.PropertyGroup):
    """ Collider properties """
    collider_options = [
        ("none", "None", "", "NONE", 0),
        ("convex", "Convex", "", "CONVEX", 1),
        ("mesh", "Mesh", "", "MESH", 2),
        ("smart", "Smart", "", "SMART", 3)]

class CreateMenuManagerOperator(bpy.types.Operator):
    """Create Menu Manager Operator"""
    bl_idname = "scene.create_menumanager_operator"
    bl_label = "Create Menu Manager"


    def execute(self, context):
        print("Creating Menu Manager")
        #_new_scene = bpy.data.scenes.new(context.scene.gamemanager_scene_name)
        #context.window.scene = _new_scene
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
            row = layout.row()
            row.label(text="Save blend file before!")
            return
        
        # SCENE PROPERTIES
        row = layout.row()
        if hasattr(context.scene, "scene_type"):
            row.prop(context.scene, "scene_type")

            match context.scene.scene_type:
                case "stage":
                    # Player spawner
                    row = layout.row()
                    row.prop(context.scene, "player_spawn_empty")
                    if context.scene.player_spawn_empty == None:
                        row = layout.row()
                        row.label(text="Select a spawn position!", icon="ERROR")

                    # Environment Lighting
                    # Sky
                    row = layout.row()
                    box = row.box()
                    box.label(text="Environment Properties")
                    #row = layout.row()
                    box = box.box()
                    box.prop(context.scene, "sky_on")
                    row1 = box.row()
                    if context.scene.sky_on:
                        box1 = row1.box()
                        box1.prop(context.scene, "sky_energy")
                
                    # ACTIVE OBJECT PROPERTIES
                    if context.active_object is not None:
                        row = layout.row()
                        box = row.box()
                        box.label(text="Active Object")
                        box3 = box.box()
                        box3.label(text=context.active_object.name)
                        box3.prop(context.active_object, "godot_exportable")
                        if context.active_object.godot_exportable:
                            box3.prop(context.active_object, "collider")
                case "player":
                    pass
                case "menu":
                    row = layout.row()
                    box = row.box()
                    box.operator("scene.create_menumanager_operator")


class SetGodotProjectEnvironmentOperator(bpy.types.Operator):
    """Set Godot Project Environment Operator"""
    bl_idname = "scene.set_godot_project_environment_operator"
    bl_label = "Set Godot Project Environment"
    
    background_mode_line = "background_mode = "
    background_energy_line = "background_energy = "
    done = False
    
    def replace_or_fill(self, context, where, this, that, pre_sentence):
        self.done = False
        for n_line in range(0, len(where)):
            if where[n_line].find(this) > -1:
                where[n_line] = that
                self.done = True
                print("First: ", that)
        if not self.done:
            for n_line in range(0, len(where)):
                if where[n_line].find(pre_sentence) > -1:
                    where.insert(n_line+1, that)
                    print("Second: ", that)
        return where
    
    def set_sky(self, context):
        print("Setting sky...")
        default_environment_filepath = os.path.join(context.scene.project_folder, "default_env.tres")
        default_environment_file = open(default_environment_filepath, "r")
        default_environment_file_content = default_environment_file.readlines()
        default_environment_file.close()
        
        if context.scene.sky_on:
            new_background_mode_line = self.background_mode_line + "2" + "\n"
            new_background_energy_line = self.background_energy_line + str(context.scene.sky_energy) + "\n"
            default_environment_file_content = self.replace_or_fill(context, default_environment_file_content, self.background_mode_line, new_background_mode_line, "[resource]")
        
            default_environment_file_content = self.replace_or_fill(context, default_environment_file_content, self.background_energy_line, new_background_energy_line, "background_sky =")
        else:
            new_background_mode_line = self.background_mode_line + "0" + "\n"
            new_background_energy_line = self.background_energy_line + "0.25" + "\n"
            default_environment_file_content = self.replace_or_fill(context, default_environment_file_content, self.background_mode_line, new_background_mode_line, "[resource]")        
            default_environment_file_content = self.replace_or_fill(context, default_environment_file_content, self.background_energy_line, new_background_energy_line, "background_sky =")
        
        # Save File
        os.remove(default_environment_filepath)
        f = open(default_environment_filepath, "w")
        f.writelines(default_environment_file_content)
        f.close()
        
        print("Sky done. ", new_background_mode_line)
    
    def execute(self, context):
        print("Setting Godot project environment...")
        self.set_sky(context)
        return {'FINISHED'}

def init_properties():
    # Scene props
    bpy.types.Scene.scene_exportable = bpy.props.BoolProperty(name="Exportable", default=False, update=update_scene_exportable) # SCENE EXPORTABLE
    bpy.types.Scene.player_spawn_empty = bpy.props.PointerProperty(type=bpy.types.Object, name="Player Spawn", poll=scene_emptyobject_poll)

    # Scene object properties
    bpy.types.Object.collider = bpy.props.EnumProperty(
        items = ColliderProperties.collider_options,
        name = "Collider Type",
        description = "Collider type",
        default = "convex")
    bpy.types.Object.godot_exportable = bpy.props.BoolProperty(name="Exportable", default=True) # OBJECT EXPORTABLE

    # Scene Environment properties
    bpy.types.Scene.sky_on = bpy.props.BoolProperty(name="Sky", default=True)
    bpy.types.Scene.sky_energy = bpy.props.FloatProperty(name="Sky Energy", default=1.0, min=0.0, max=16.0, soft_min=0.0, soft_max=16.0)

def clear_properties():
    del bpy.types.Scene.scene_exportable
    del bpy.types.Scene.player_spawn_empty
    del bpy.types.Object.godot_exportable
    del bpy.types.Scene.sky_on
    del bpy.types.Scene.sky_energy

def register():
    init_properties()
    bpy.utils.register_class(CreateMenuManagerOperator)
    bpy.utils.register_class(ScenePropertiesPanel)
    bpy.utils.register_class(SetGodotProjectEnvironmentOperator)

def unregister():
    bpy.utils.unregister_class(SetGodotProjectEnvironmentOperator)
    bpy.utils.unregister_class(ScenePropertiesPanel)
    bpy.utils.unregister_class(CreateMenuManagerOperator)
    clear_properties()


