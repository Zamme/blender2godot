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
Editor panel
"""

import os
import json
import subprocess
import shutil
import imghdr

import bpy
import mathutils


class my_dictionary(dict): 
  
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 

class SCENES_UL_scenes_added(bpy.types.UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        #layout.prop(item, "name", text=item.name, emboss=False, icon_value=icon)
 
        custom_icon = 'SCENE'
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon = custom_icon)
            layout.prop(item, "value")
        elif self.layout_type in {'GRID'}:
            layout.alignment = 'CENTER'
            layout.label(text="", icon = custom_icon)

class RemoveSceneFromListOperator(bpy.types.Operator):
    """Remove scene from list"""
    bl_idname = "scene.remove_scene_from_list_operator"
    bl_label = "X"

    def execute(self, context):
        print("removing scene...")
        print("scene removed.")
        return {'FINISHED'}

class B2G_ToolsPanel(bpy.types.Panel):
    """B2G Tools Panel"""
    bl_label = "B2G Tools"
    bl_idname = "B2GTOOLS_PT_layout"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_options = {"DEFAULT_CLOSED"}
    bl_order = 4
    
    advanced_tools = False
    
    @classmethod 
    def poll(self, context):
        return ((context.scene.name == context.scene.gamemanager_scene_name) and (bpy.data.is_saved))
    
    def draw(self, context):
        layout = self.layout
        scene = context.scene
        blend_data = context.blend_data
        
        if bpy.path.abspath("//") == "":       
            return

        # Game structure
        row = layout.row()
        row.label(text="Check scenes to export:")
        row = layout.row()
        box = row.box()
        if len(bpy.data.scenes["B2G_GameManager"].scenes_added) > 0:
            box.template_list("SCENES_UL_scenes_added", "The_List", scene, "scenes_added", scene, "scenes_added_index")
        else:
            box.label(text="No scenes to add")

        # Export project to godot button
        row = layout.row()
        row.scale_y = 3.0
        row.operator("scene.export_project_to_godot_operator")        
        
        row = layout.row()
        row.prop(context.scene, 'advanced_tools')
        
        if context.scene.advanced_tools:
            # Delete project button
            row = layout.row()
            row.scale_y = 3.0
            row.operator_context = 'INVOKE_DEFAULT' # TODO: not working!!!
            #row.operator("scene.delete_project_button_operator")
            row.operator("scene.delete_project_operator")
            
            # Create project button
            row = layout.row()
            row.scale_y = 3.0
            row.operator("scene.create_godot_project_operator")
            
            # Export project button
            #row = layout.row()
            #row.scale_y = 3.0
            #row.operator("scene.export_game_operator")
            
            # Open godot project button
            row = layout.row()
            row.scale_y = 3.0
            row.operator("scene.open_godot_project_operator")


class ExportGameOperator(bpy.types.Operator):
    """Export Game Operator"""
    bl_idname = "scene.export_game_operator"
    bl_label = "Export Game"
    
    assets_folder_name = "assets"
    models_folder_name = "models"
    colliders_filepath = ""
    player_info_filepath = ""
    lights_info_filepath = ""
    
    dict_colliders = my_dictionary()
    dict_player_info = my_dictionary()
    dict_lights_info = my_dictionary()
    
    def check_custom_icon(self, context):
        return (imghdr.what(context.scene.game_icon) == "png")
    
    def export_colliders(self, context, _scene):
        print("Exporting colliders...")
        self.find_colliders_file_path(context)
        scene_objects = _scene.objects
        for ob in scene_objects:
            if ob.godot_exportable:
                new_name = ob.name.replace(".", "")
                print("Exporting", new_name)
                self.dict_colliders.add(new_name, ob.collider)
                #self.dict_colliders.add(ob.name, ob.collider)
        print("Colliders exporting finished.")
        self.data_colliders = json.dumps(self.dict_colliders, indent=1, ensure_ascii=True)
        with open(self.colliders_filepath, 'w') as outfile:
            outfile.write(self.data_colliders + '\n')
        #with open(self.colliders_filepath, 'r') as fp:
            #data_file = json.load(fp)
        #print(data_file)
    
    def export_game_project(self, context):
        print("Exporting game", context.scene.project_folder)
        #self.fix_objects_names(context)
        self.models_folder_path = os.path.join(self.assets_folder_path, self.models_folder_name)
        if not os.path.isdir(self.models_folder_path):
            os.mkdir(self.models_folder_path)
        for _sc_added in context.scene.scenes_added:
            if _sc_added.value:
                _sc = bpy.data.scenes[_sc_added.name]
                self.export_scene(context, _sc)
                context.window.scene = bpy.data.scenes["B2G_GameManager"]
                self.export_colliders(context, _sc)
                context.window.scene = bpy.data.scenes["B2G_GameManager"]
                self.export_player_info(context)
                context.window.scene = bpy.data.scenes["B2G_GameManager"]
                self.export_lights(context)
                context.window.scene = bpy.data.scenes["B2G_GameManager"]
                self.export_icon(context)
                context.window.scene = bpy.data.scenes["B2G_GameManager"]
        bpy.ops.scene.set_godot_project_environment_operator()
        context.window.scene = bpy.data.scenes["B2G_GameManager"]
    
    def export_icon(self, context):
        scene = context.scene
        dest_image_path = os.path.join(scene.project_folder, "icon.png")
        if ((scene.game_icon == "") or (scene.game_icon == dest_image_path)): # TODO : what to do?
            return
        if self.check_custom_icon(context):
            shutil.copyfile(scene.game_icon, dest_image_path)
        else:
            print("Custom icon is not a png image. Loading default icon.")
    
    def export_lights(self, context):
        print("Exporting lights...")
        self.find_lights_file_path(context)
        scene_objects = context.scene.objects
        for ob in scene_objects:
            #print(ob.type)
            if ob.type == "LIGHT":
                print("Exporting", ob.name)
                self.dict_lights_info.add(ob.name, ob.data.type)
                self.dict_lights_info.add(ob.name + "PositionX", ob.location.x)
                self.dict_lights_info.add(ob.name + "PositionY", ob.location.y)
                self.dict_lights_info.add(ob.name + "PositionZ", ob.location.z)
                self.dict_lights_info.add(ob.name + "ColorR", ob.data.color[0])
                self.dict_lights_info.add(ob.name + "ColorG", ob.data.color[1])
                self.dict_lights_info.add(ob.name + "ColorB", ob.data.color[2])
                if hasattr(ob.data, "distance"):
                    self.dict_lights_info.add(ob.name + "Range", ob.data.distance)
                else:
                    self.dict_lights_info.add(ob.name + "Range", 5.0)
                self.dict_lights_info.add(ob.name + "RotationX", ob.rotation_euler.x)
                self.dict_lights_info.add(ob.name + "RotationY", ob.rotation_euler.y)
                self.dict_lights_info.add(ob.name + "RotationZ", ob.rotation_euler.z)
                if ob.data.type == "POINT":
                    self.dict_lights_info.add(ob.name + "Energy", ob.data.energy)
                    self.dict_lights_info.add(ob.name + "UseShadow", ob.data.use_shadow)
                elif ob.data.type == "SUN":
                    self.dict_lights_info.add(ob.name + "Energy", ob.data.energy)
                    self.dict_lights_info.add(ob.name + "UseShadow", ob.data.use_shadow)
                elif ob.data.type == "SPOT":
                    self.dict_lights_info.add(ob.name + "Energy", ob.data.energy)
                    self.dict_lights_info.add(ob.name + "UseShadow", ob.data.use_shadow)
                    self.dict_lights_info.add(ob.name + "UseSquare", ob.data.use_square)
                elif ob.data.type == "AREA":
                    self.dict_lights_info.add(ob.name + "Energy", ob.data.energy)
                    self.dict_lights_info.add(ob.name + "UseShadow", ob.data.use_shadow)
        print("Lights exporting finished.")
        self.data_lights = json.dumps(self.dict_lights_info, indent=1, ensure_ascii=True)
        with open(self.lights_info_filepath, 'w') as outfile:
            outfile.write(self.data_lights + '\n')
    
    def export_player_info(self, context):
        print("Exporting player...")
        self.find_player_info_file_path(context)
        self.dict_player_info.add("GravityOn", context.scene.player_gravity_on)
        if context.scene.player_object != "None":
            camera_object = context.scene.objects[context.scene.player_object]
            player_position = camera_object.location
            player_rotation = camera_object.rotation_euler
        else:
            player_position = mathutils.Vector((0.0, 0.0, 0.0))
            player_rotation = mathutils.Vector((0.0, 0.0, 0.0))
        self.dict_player_info.add("PlayerObjectName", context.scene.player_object)
        self.dict_player_info.add("InitialPositionX", player_position[0])
        self.dict_player_info.add("InitialPositionY", player_position[1])
        self.dict_player_info.add("InitialPositionZ", player_position[2])
        self.dict_player_info.add("InitialRotationX", player_rotation[0])
        self.dict_player_info.add("InitialRotationY", player_rotation[1])
        self.dict_player_info.add("InitialRotationZ", player_rotation[2])
        self.dict_player_info.add("CameraInverted", context.scene.camera_inverted)
        self.data_player_info = json.dumps(self.dict_player_info, indent=1, ensure_ascii=True)
        with open(self.player_info_filepath, 'w') as outfile:
            outfile.write(self.data_player_info + '\n')
        with open(self.player_info_filepath, 'r') as fp:
            data_file = json.load(fp)
        print(data_file)        
    
    def export_scene(self, context, _scene):
        print("Exporting scene", _scene.name)
        context.window.scene = _scene
        model_path = os.path.join(self.models_folder_path, _scene.name)
        for ob in _scene.objects:
            ob.select_set(ob.godot_exportable)
        if len(_scene.objects) > 0:
            bpy.ops.export_scene.gltf(filepath=model_path, use_selection=True, export_apply=True, export_lights=True)
        print("Scene", _scene.name, "exported.")
    
    def find_colliders_file_path(self, context):
        self.colliders_filepath = os.path.join(context.scene.project_folder, "colliders_info", "colliders.json")
        print("Colliders json filepath:", self.colliders_filepath)
    
    def find_lights_file_path(self, context):
        self.lights_info_filepath = os.path.join(context.scene.project_folder, "lights_info", "lights_info.json")
        print("Lights json filepath:", self.lights_info_filepath)
        
    def find_player_info_file_path(self, context):
        self.player_info_filepath = os.path.join(context.scene.project_folder, "player_info", "player_info.json")
        print("Player info json filepath:", self.player_info_filepath)

    def fix_objects_names(self, context):
        print("Fixing objects names...(Godot can't use dots and other signs!)")
        scene_objects = context.scene.objects
        for sc_ob in scene_objects:
            sc_ob.name = sc_ob.name.replace(".", "_")
            sc_ob.name = sc_ob.name.replace(":", "_")
            sc_ob.name = sc_ob.name.replace("@", "_")
            sc_ob.name = sc_ob.name.replace("/", "_")
            sc_ob.name = sc_ob.name.replace('"', "_")
        print("Objects names fixed.")
    
    def main(self, context):
        self.assets_folder_path = os.path.join(context.scene.project_folder, self.assets_folder_name)
        if not os.path.isdir(self.assets_folder_path):
            os.mkdir(self.assets_folder_path)
        self.export_game_project(context)        

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}


class OpenGodotProjectOperator(bpy.types.Operator): # It DOESN'T block blender execution until game exits
    """Open Godot Project Operator"""
    bl_idname = "scene.open_godot_project_operator"
    bl_label = "Open Godot Project"
    
    def execute(self, context):
        print("Opening godot project...")
        self.cmd = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "--editor", "--path", context.scene.project_folder], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(SCENES_UL_scenes_added)
    bpy.utils.register_class(RemoveSceneFromListOperator)
    bpy.utils.register_class(ExportGameOperator)
    bpy.utils.register_class(B2G_ToolsPanel)
    bpy.utils.register_class(OpenGodotProjectOperator)

def unregister():
    bpy.utils.unregister_class(OpenGodotProjectOperator)
    bpy.utils.unregister_class(B2G_ToolsPanel)
    bpy.utils.unregister_class(ExportGameOperator)
    bpy.utils.unregister_class(RemoveSceneFromListOperator)
    bpy.utils.unregister_class(SCENES_UL_scenes_added)

