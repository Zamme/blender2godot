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
    def filter_items(self, context, data, propname):
        _scenes = getattr(data, propname)

        filter_flags = [0] * len(_scenes)
        visible = 1 << 30

        for i, me in enumerate(_scenes):
            if me.name != "B2G_GameManager":
                filter_flags[i] = visible

        return filter_flags, ()

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        custom_icon = 'SCENE'
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon = custom_icon)
            #if item.name != "B2G_GameManager":
            if hasattr(context.scene, "scene_type"):
                layout.prop(item, "scene_type", text="")
                if item.scene_type != "none":
                    layout.prop(item, "scene_exportable")
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
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon="TOOL_SETTINGS")        

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        blend_data = context.blend_data
        
        if not bpy.data.is_saved:       
            return

        # Game structure
        row = layout.row()
        box0 = row.box()
        box1 = box0.box()
        box1.label(text="Check scenes to export")
        if len(bpy.data.scenes) > 0:
            box1.template_list("SCENES_UL_scenes_added", "ScenesAddedList", bpy.data, "scenes", scene, "scenes_added_index")
            box1.prop(scene, "startup_scene")
        else:
            box1.label(text="No scenes to add")

        # Export project to godot button
        if (bpy.data.scenes[context.scene.gamemanager_scene_name].startup_scene == None):
            box1.label(text="Select startup scene", icon="ERROR")
            return
        elif (bpy.data.scenes[context.scene.gamemanager_scene_name].startup_scene.name == "B2G_GameManager"):
            box1.label(text="Startup scene can't be Game Manager", icon="ERROR")
            return
        elif hasattr(bpy.data.scenes[context.scene.gamemanager_scene_name].startup_scene, "scene_type"):
            if (bpy.data.scenes[context.scene.gamemanager_scene_name].startup_scene.scene_type == "player"):
                box1.label(text="Startup scene can't be a player", icon="ERROR")
                return

        row = box0.row()
        row.scale_y = 2.0
        row.operator("scene.export_project_to_godot_operator", icon="EXPORT")        
        
        row = layout.row()
        row.alignment="CENTER"
        row.prop(context.scene, 'advanced_tools', icon="PLUS")
        
        if context.scene.advanced_tools:
            row2 = layout.row()
            box2 = row2.box()
            # Create project button
            box2.operator("scene.create_godot_project_operator", icon="PRESET_NEW")
            if os.path.isdir(context.scene.project_folder):
                # Delete project button
                box2.operator("scene.delete_project_operator", icon="TRASH")
                # Open godot project button
                box2.operator("scene.open_godot_project_operator", icon="GHOST_ENABLED")
                box2.operator("scene.open_godot_project_folder_operator", icon="FOLDER_REDIRECT")


class ExportGameOperator(bpy.types.Operator):
    """Export Game Operator"""
    bl_idname = "scene.export_game_operator"
    bl_label = "Export Game"
    
    assets_folder_name = "assets"
    models_folder_name = "models"
    colliders_filepath = ""
    player_info_filepath = ""
    lights_info_filepath = ""
    godot_project_settings_filepath = ""
    stages_info_filepath = ""
    
    dict_colliders = my_dictionary()
    dict_player_info = my_dictionary()
    dict_lights_info = my_dictionary()
    dict_godot_project_settings = my_dictionary()
    dict_stages_info = my_dictionary()
    
    def check_custom_icon(self, context):
        _checked = False
        if os.path.exists(context.scene.game_icon):
            if (imghdr.what(context.scene.game_icon) == "png"):
                _checked = True
        return _checked
    
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
        _sc_index = 0
        for _sc_added in bpy.data.scenes:
            if _sc_added.scene_exportable:
                _sc = bpy.data.scenes[_sc_added.name]
                self.export_scene(context, _sc)
                context.window.scene = bpy.data.scenes["B2G_GameManager"]
                match _sc_added.scene_type:
                    case "stage":
                        self.export_colliders(context, _sc)
                        context.window.scene = bpy.data.scenes["B2G_GameManager"]
                        self.export_lights(context)
                        context.window.scene = bpy.data.scenes["B2G_GameManager"]
                        _temp_dict = my_dictionary()
                        _temp_dict.add("SceneName", _sc_added.name)
                        if not _sc_added.player_spawn_empty:
                            _temp_dict.add("PlayerSpawnObjectName", "")
                        else:
                            _temp_dict.add("PlayerSpawnObjectName", _sc_added.player_spawn_empty.name)
                        self.dict_stages_info.add(_sc_index, _temp_dict)
                        _sc_index += 1
                    case "player":
                        self.export_player_info(context, _sc)
                        context.window.scene = bpy.data.scenes["B2G_GameManager"]
        bpy.ops.scene.set_godot_project_environment_operator()
        context.window.scene = bpy.data.scenes["B2G_GameManager"]
        self.export_stages_info(context)
        context.window.scene = bpy.data.scenes["B2G_GameManager"]
        self.export_icon(context)
        context.window.scene = bpy.data.scenes["B2G_GameManager"]
        self.export_godot_project_settings(context)
        context.window.scene = bpy.data.scenes["B2G_GameManager"]
    
    def export_godot_project_settings(self, context):
        print("Exporting project settings...")

        self.find_godot_project_settings_file_path(context)

        # Config name
        self.dict_godot_project_settings.add("application/config/name", context.scene.game_name)
        # Startup scene
        self.dict_godot_project_settings.add("application/run/main_scene", context.scene.startup_scene.name)
        # Display settings
        self.dict_godot_project_settings.add("display/window/size/width", context.scene.display_width)
        self.dict_godot_project_settings.add("display/window/size/height", context.scene.display_height)
        self.dict_godot_project_settings.add("display/window/size/resizable", context.scene.display_resizable)
        self.dict_godot_project_settings.add("display/window/size/borderless", context.scene.display_borderless)
        self.dict_godot_project_settings.add("display/window/size/fullscreen", context.scene.display_fullscreen)
        self.dict_godot_project_settings.add("display/window/size/always_on_top", context.scene.display_alwaysontop)
        # Boot splash settings
        self.dict_godot_project_settings.add("application/boot_splash/show_image", context.scene.splash_showimage)
        self.dict_godot_project_settings.add("application/boot_splash/image", context.scene.splash_imagefilepath)
        self.dict_godot_project_settings.add("application/boot_splash/fullsize", context.scene.splash_fullsize)
        self.dict_godot_project_settings.add("application/boot_splash/use_filter", context.scene.splash_usefilter)
        _color_string = str(context.scene.splash_bgcolor[0]) + "," + str(context.scene.splash_bgcolor[1]) + "," + str(context.scene.splash_bgcolor[2]) + "," + str(context.scene.splash_bgcolor[3])
        self.dict_godot_project_settings.add("application/boot_splash/bg_color", _color_string)

        self.data_settings = json.dumps(self.dict_godot_project_settings, indent=1, ensure_ascii=True)
        with open(self.godot_project_settings_filepath, 'w') as outfile:
            outfile.write(self.data_settings + '\n')

        print("Project settings exported.")
    
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
    
    def export_player_info(self, context, _player_scene):
        print("Exporting player...")
        self.find_player_info_file_path(context)
        # GENERAL PROPS
        self.dict_player_info.add("PlayerSceneName", _player_scene.name)
        self.dict_player_info.add("GravityOn", _player_scene.player_gravity_on)
        # DIMENSIONS
        self.dict_player_info.add("PlayerDimensions", {"DimX" : _player_scene.player_object.dimensions.x,
                                                       "DimY" : _player_scene.player_object.dimensions.y,
                                                       "DimZ" : _player_scene.player_object.dimensions.z})
        # PLAYER CAMERA
        self.dict_player_info.add("PlayerCameraObject", {"CameraName" : _player_scene.camera_object.name,
                                                         "PosX" : _player_scene.camera_object.location.x,
                                                         "PosY" : _player_scene.camera_object.location.y,
                                                         "PosZ" : _player_scene.camera_object.location.z,
                                                         "RotX" : _player_scene.camera_object.rotation_euler.x,
                                                         "RotY" : _player_scene.camera_object.rotation_euler.y,
                                                         "RotZ" : _player_scene.camera_object.rotation_euler.z})
        # ANIMATIONS
        _action_dictionary = my_dictionary()
        for _player_action in bpy.data.actions:
            _action_dictionary.add(_player_action.animation_type , _player_action.name)
        self.dict_player_info.add("PlayerAnimations", _action_dictionary)
        # CONTROLS
        _controls_dictionary = my_dictionary()
        for _control_setting in _player_scene.controls_settings:
            _controls_dictionary.add(_control_setting.motion_input_blender, _control_setting.motion_input_godot)
        self.dict_player_info.add("PlayerControls", _controls_dictionary)
        # EXPORT JSON
        self.data_player_info = json.dumps(self.dict_player_info, indent=1, ensure_ascii=True)
        with open(self.player_info_filepath, 'w') as outfile:
            outfile.write(self.data_player_info + '\n')   

    def export_scene(self, context, _scene):
        print("Exporting scene", _scene.name)
        context.window.scene = _scene
        model_path = os.path.join(self.models_folder_path, _scene.name)
        for ob in _scene.objects:
            ob.select_set(ob.godot_exportable)
        if len(_scene.objects) > 0:
            bpy.ops.export_scene.gltf(filepath=model_path, use_selection=True, export_apply=True, export_lights=True, use_active_scene=True)
            print("Scene", _scene.name, "exported.")
        else:
            print("Scene ", _scene.name, " empty!")
    
    def export_stages_info(self, context):
        self.find_stages_info_file_path(context)
        self.data_stages_info = json.dumps(self.dict_stages_info, indent=1, ensure_ascii=True)
        with open(self.stages_info_filepath, 'w') as outfile:
            outfile.write(self.data_stages_info + '\n')   

    def find_colliders_file_path(self, context):
        self.colliders_filepath = os.path.join(context.scene.project_folder, "colliders_info", "colliders.json")
        print("Colliders json filepath:", self.colliders_filepath)
    
    def find_lights_file_path(self, context):
        self.lights_info_filepath = os.path.join(context.scene.project_folder, "lights_info", "lights_info.json")
        print("Lights json filepath:", self.lights_info_filepath)
        
    def find_player_info_file_path(self, context):
        self.player_info_filepath = os.path.join(context.scene.project_folder, "player_info", "player_info.json")
        print("Player info json filepath:", self.player_info_filepath)

    def find_godot_project_settings_file_path(self, context):
        self.godot_project_settings_filepath = os.path.join(context.scene.project_folder, "godot_project_settings_info", "godot_project_settings.json")
        print("Godot project settings info json filepath:", self.godot_project_settings_filepath)

    def find_stages_info_file_path(self, context):
        self.stages_info_filepath = os.path.join(context.scene.project_folder, "stages_info", "stages_info.json")
        print("Godot project settings info json filepath:", self.godot_project_settings_filepath)

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

def init_properties():
    bpy.types.Scene.scenes_added_index = bpy.props.IntProperty(name = "Index for my_list", default = 0)
    bpy.types.Scene.startup_scene = bpy.props.PointerProperty(type=bpy.types.Scene, name="Startup Scene")
    # Panels checkboxes
    bpy.types.Scene.advanced_tools = bpy.props.BoolProperty(name="Advanced Tools", default=False)

def clear_properties():
    del bpy.types.Scene.startup_scene
    del bpy.types.Scene.scenes_added_index
    del bpy.types.Scene.advanced_tools

def register():
    init_properties()
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
    clear_properties()

