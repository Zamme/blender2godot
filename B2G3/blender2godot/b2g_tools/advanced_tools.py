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


INFOS_FOLDER_NAME = "infos"
HUDS_INFO_FILENAME = "huds_info.json"
STAGES_INFO_FILENAME = "stages_info.json"
COLLIDERS_INFO_FILENAME = "colliders_info.json"
PLAYERS_INFO_FILENAME = "players_info.json"
MENUS_INFO_FILENAME = "menus_info.json"
NPCS_INFO_FILENAME = "npcs_info.json"
LOADING_INFO_FILENAME = "loadings_info.json"
LIGHTS_INFO_FILENAME = "lights_info.json"
GODOT_PROJECT_SETTINGS_INFO_FILENAME = "godot_project_settings.json"

class my_dictionary(dict): 
    # __init__ function 
    def __init__(self): 
        self = dict() 
          
    # Function to add key:value 
    def add(self, key, value): 
        self[key] = value 

def get_controls_list():
    _controls_list = None
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "b2g_misc"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "b2g_misc")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _filepath = os.path.join(p_path, "b2g_controls_list.json")
            if os.path.isfile(_filepath):
                with open(_filepath, 'r') as outfile:
                    _controls_list = json.load(outfile)
                    break
            else:
                pass
    return _controls_list

def poll_startupable_scenes(self, _scene):
    return (((_scene.scene_type == "stage") or (_scene.scene_type == "2dmenu") or (_scene.scene_type == "3dmenu")) and (_scene.name != "B2G_GameManager"))

def show_error_popup(message = [], title = "Message Box", icon = 'INFO'):
    def draw(self, context):
        for _error in message:
           self.layout.label(text=_error, icon="ERROR")
    bpy.context.window_manager.popup_menu(draw, title=title, icon=icon)

class SCENES_UL_scenes_added(bpy.types.UIList):
    def filter_items(self, context, data, propname):
        _scenes = getattr(data, propname)

        filter_flags = [0] * len(_scenes)
        visible = 1 << 30

        for i, me in enumerate(_scenes):
            if me.name != context.scene.gamemanager_scene_name:
                filter_flags[i] = visible

        return filter_flags, ()

    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):
        custom_icon = 'SCENE'
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.label(text=item.name, icon = custom_icon)
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

class AreYouSureDeletingOperator(bpy.types.Operator):
    """Really?"""
    bl_idname = "scene.are_you_sure_deleting_operator"
    bl_label = "Delete Godot Project"
    bl_description = "Delete de Godot project folder"
    
    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        bpy.ops.scene.delete_project_operator()
        self.report({'INFO'}, "Project deleted!")
        print("Project deleted.")
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

class CreateGodotProjectOperator(bpy.types.Operator):
    """Create Godot Project Operator"""
    bl_idname = "scene.create_godot_project_operator"
    bl_label = "Create Godot Project"
    
    project_file = None
    godot_project_template_path = ""
    
    def add_initial_files(self, context):
        if os.path.isdir(context.scene.project_folder):
            print("Folder exists...")
        else:
            print("Creating project tree from template...")
            shutil.copytree(self.godot_project_template_path, context.scene.project_folder)
            print("Godot project tree created.")
    
    def find_project_template_dir_path(self, context):
        possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "project_template"),
        os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "project_template")]
        for p_path in possible_paths:
            if os.path.isdir(p_path):
                self.godot_project_template_path = p_path
        print("Godot project template directory:", self.godot_project_template_path)
           
    def main(self, context):
        context.scene.game_folder = bpy.path.abspath("//")
        self.find_project_template_dir_path(context)
        context.scene.project_folder = os.path.join(context.scene.game_folder, context.scene.game_name + "_Game")
        self.add_initial_files(context)

    def execute(self, context):
        self.main(context)
        return {'FINISHED'}

class DeleteProjectOperator(bpy.types.Operator):
    """Delete Project Operator"""
    bl_idname = "scene.delete_project_operator"
    bl_label = "Delete Project"
    
    def delete_project(self, context):
        if os.path.isdir(context.scene.project_folder):
            print("Deleting project...", context.scene.project_folder)
            shutil.rmtree(context.scene.project_folder)
            print("Project deleted")
        else:
            print("Project not found.")
        executables_path = os.path.join(context.scene.game_folder, "builds")
        if os.path.isdir(executables_path):
            print("Deleting executables...", executables_path)
            shutil.rmtree(executables_path)
            print("Executables deleted")
        else:
            print("Executables not found.")
    
    def main(self, context):
        self.delete_project(context)        

    def execute(self, context):
        self.main(context)
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
        
        if not bpy.data.is_saved:       
            return
        if context.scene.godot_exporting or context.scene.is_game_exporting:       
            layout.enabled = False
        else:
            layout.enabled = True

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
            if (os.path.isdir(context.scene.project_folder) and (context.scene.godot_export_ok)):
                # Delete project button
                box2.operator(AreYouSureDeletingOperator.bl_idname, icon="TRASH")
                # Open godot project button
                box2.operator("scene.open_godot_project_operator", icon="GHOST_ENABLED")
                box2.operator("scene.open_godot_project_folder_operator", icon="FOLDER_REDIRECT")

class ExportGameOperator(bpy.types.Operator):
    """Export Game Operator"""
    bl_idname = "scene.export_game_operator"
    bl_label = "Export Game"
    
    assets_folder_name = "assets"
    models_folder_name = "models"
    huds_folder_name = "huds"
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
    dict_menus_info = my_dictionary()
    dict_huds_info = my_dictionary()

    controls_list = get_controls_list()
    
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
        print("Colliders exporting finished.")
        self.data_colliders = json.dumps(self.dict_colliders, indent=1, ensure_ascii=True)
        with open(self.colliders_filepath, 'w') as outfile:
            outfile.write(self.data_colliders + '\n')
    
    def export_game_project(self, context):
        print("Exporting game", context.scene.project_folder)
        self.infos_dirpath = os.path.join(context.scene.project_folder, INFOS_FOLDER_NAME)
        if not os.path.isdir(self.infos_dirpath):
            os.mkdir(self.infos_dirpath)
        #self.fix_objects_names(context)
        self.models_folder_path = os.path.join(self.assets_folder_path, self.models_folder_name)
        if not os.path.isdir(self.models_folder_path):
            os.mkdir(self.models_folder_path)
        _sc_index = 0
        for _sc_added in bpy.data.scenes:
            if _sc_added.scene_exportable:
                _sc = bpy.data.scenes[_sc_added.name]
                if _sc.scene_type == "hud":
                    self.export_hud(context, _sc)
                    context.window.scene = bpy.data.scenes["B2G_GameManager"]
                    _hud_dict = my_dictionary()
                    _hud_obj_dict = my_dictionary()
                    for _hud_obj in _sc.objects:
                        _hud_obj_dict.add(_hud_obj.name, _hud_obj.type)
                    _hud_dict.add("Objects", _hud_obj_dict)
                    _hud_settings_dict = my_dictionary()
                    _hud_settings_dict.add("VisibilityType", _sc.hud_settings.visibility_type)
                    _hud_settings_dict.add("ShowTransitionType", _sc.hud_settings.show_transition_type)
                    _hud_settings_dict.add("ShowTransitionTime", _sc.hud_settings.show_transition_time)
                    _hud_settings_dict.add("HideTransitionType", _sc.hud_settings.hide_transition_type)
                    _hud_settings_dict.add("HideTransitionTime", _sc.hud_settings.hide_transition_time)
                    _hud_settings_dict.add("ExportFormat", _sc.hud_settings.hud_export_format)
                    _hud_dict.add("Settings", _hud_settings_dict)
                    self.dict_huds_info.add(_sc.name, _hud_dict)
                else:
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
                        case "3dmenu":
                            # MENUS'S CAMERA
                            _temp_dict = my_dictionary()
                            if not _sc_added.menu_camera_object:
                                _temp_dict.add("MenuCameraObjectDict", my_dictionary())
                            else:
                                _cam_dict = my_dictionary()
                                _cam_dict.add("MenuCameraObjectName", _sc_added.menu_camera_object.name)
                                _cam_dict.add("Position", {"PosX" : _sc_added.menu_camera_object.location.x,
                                                            "PosY" : _sc_added.menu_camera_object.location.y,
                                                            "PosZ" : _sc_added.menu_camera_object.location.z})
                                _cam_dict.add("Rotation", {"RotX" : _sc_added.menu_camera_object.rotation_euler.x,
                                                            "RotY" : _sc_added.menu_camera_object.rotation_euler.y,
                                                            "RotZ" : _sc_added.menu_camera_object.rotation_euler.z})
                                _cam_dict.add("FOV", _sc_added.menu_camera_object.data.angle)
                                _cam_dict.add("KeepFOV", _sc_added.menu_camera_object.data.sensor_fit)
                                _temp_dict.add("MenuCameraObjectDict", _cam_dict)
                            # MENU'S SPECIAL OBJECTS
                            _special_objects = my_dictionary()
                            for _obj in _sc_added.objects:
                                _special_objects.add(_obj.name, {
                                    "ObjectType" : _obj.special_object_info.menu_object_type,
                                    "ActionOnClick" : _obj.special_object_info.button_action_on_click
                                })
                                _action_parameter_rename = ""
                                if _obj.special_object_info.button_action_on_click == "load_stage":
                                    _action_parameter_rename = "Stage_" + _obj.special_object_info.button_action_parameter
                                elif _obj.special_object_info.button_action_on_click == "load_menu":
                                    _action_parameter_rename = "Menu_" + _obj.special_object_info.button_action_parameter
                                _special_objects[_obj.name]["ActionParameter"] = _action_parameter_rename
                            _temp_dict.add("SpecialObjects", _special_objects)
                            # ADD DICT TO INFO
                            self.dict_menus_info.add(_sc_added.name, _temp_dict)
        #bpy.ops.scene.set_godot_project_environment_operator()
        context.window.scene = bpy.data.scenes["B2G_GameManager"]
        self.export_stages_info(context)
        context.window.scene = bpy.data.scenes["B2G_GameManager"]
        self.export_menus_info(context)
        context.window.scene = bpy.data.scenes["B2G_GameManager"]
        self.export_huds_info(context)
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
        self.dict_godot_project_settings.add("startup_scene_type", context.scene.startup_scene.scene_type)
        self.dict_godot_project_settings.add("application/run/main_scene", context.scene.startup_scene.name)
        # Display settings
        self.dict_godot_project_settings.add("display/window/size/width", bpy.data.scenes["B2G_GameManager"].render.resolution_x)
        self.dict_godot_project_settings.add("display/window/size/height", bpy.data.scenes["B2G_GameManager"].render.resolution_y)
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
    
    def export_hud(self, context, _hud_scene):
        self.huds_folder_path = os.path.join(self.assets_folder_path, self.huds_folder_name)
        if not os.path.isdir(self.huds_folder_path):
            os.mkdir(self.huds_folder_path)
        print("Exporting hud scene", _hud_scene.name)
        context.window.scene = _hud_scene
        for _obj in _hud_scene.objects:
            _obj.select_set(_obj.godot_exportable)
            bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.view3d.view_camera()
        hud_path = os.path.join(self.huds_folder_path, _hud_scene.name)
        if len(_hud_scene.objects) > 0:
            match _hud_scene.hud_settings.hud_export_format:
                case "svg":
                    hud_path = hud_path + ".svg"
                    bpy.ops.wm.gpencil_export_svg(filepath=hud_path, check_existing=True, 
                                                use_fill=True,
                                                selected_object_type="SELECTED", stroke_sample=0.0,
                                                use_normalized_thickness=True, use_clip_camera=True)
                case "png":
                    hud_path = hud_path + ".png"
                    _hud_scene.render.engine = "BLENDER_EEVEE"
                    bpy.context.scene.render.filepath = hud_path
                    bpy.ops.render.render(write_still = True)
            print("Scene", _hud_scene.name, "exported.")
        else:
            print("Scene ", _hud_scene.name, " empty!")

    def export_huds_info(self, context):
        self.find_huds_info_file_path(context)
        self.data_huds_info = json.dumps(self.dict_huds_info, indent=1, ensure_ascii=True)
        with open(self.huds_info_filepath, 'w') as outfile:
            outfile.write(self.data_huds_info + '\n')   

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
    
    def export_menus_info(self, context):
        self.find_menus_info_file_path(context)
        self.data_menus_info = json.dumps(self.dict_menus_info, indent=1, ensure_ascii=True)
        with open(self.menus_info_filepath, 'w') as outfile:
            outfile.write(self.data_menus_info + '\n')   

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
                                                         "RotZ" : _player_scene.camera_object.rotation_euler.z,
                                                         "FOV" : _player_scene.camera_object.data.angle,
                                                         "KeepFOV" : _player_scene.camera_object.data.sensor_fit})
        # ANIMATIONS
        _animation_dictionary = my_dictionary()
        for _player_action in bpy.data.actions:
            _animation_dictionary.add(_player_action.animation_type , _player_action.name)
        self.dict_player_info.add("PlayerAnimations", _animation_dictionary)
        # CONTROLS
        _controls_dictionary = my_dictionary()
        for _control_setting in _player_scene.controls_settings:
            _control_inputs_array = []
            for _mot_input in _control_setting.motion_inputs:
                _inputs = [_mot_input.motion_input_type,
                            _mot_input.motion_input_blender,
                            self.controls_list[(_mot_input.motion_input_type).capitalize()][_mot_input.motion_input_blender]["GodotID"],
                            self.controls_list[(_mot_input.motion_input_type).capitalize()][_mot_input.motion_input_blender]["GodotEnumID"],
                            _mot_input.motion_input_modifier]
                _control_inputs_array.append(_inputs)
            _controls_dictionary.add(_control_setting.motion_name, _control_inputs_array)
        self.dict_player_info.add("PlayerControls", _controls_dictionary)
        # ACTIONS
        _actions_dictionary = my_dictionary()
        for _action_setting in _player_scene.actions_settings:
            _actions_dictionary.add(_action_setting.action_id, _action_setting.action_process)
        self.dict_player_info.add("PlayerActions", _actions_dictionary)
        # HUD
        _hud_dictionary = my_dictionary()
        _hud_dictionary.add("HudSceneName", _player_scene.player_hud_scene)
        self.dict_player_info.add("PlayerHUD", _hud_dictionary)
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
        self.colliders_filepath = os.path.join(self.infos_dirpath, COLLIDERS_INFO_FILENAME)
        #if not os.path.isfile(self.colliders_filepath):
        #print("Colliders json filepath:", self.colliders_filepath)
    
    def find_huds_info_file_path(self, context):
        self.huds_info_filepath = os.path.join(self.infos_dirpath, HUDS_INFO_FILENAME)
        #print("Godot huds settings info json filepath:", self.huds_info_filepath)

    def find_lights_file_path(self, context):
        self.lights_info_filepath = os.path.join(self.infos_dirpath, LIGHTS_INFO_FILENAME)
        #print("Lights json filepath:", self.lights_info_filepath)
        
    def find_player_info_file_path(self, context):
        self.player_info_filepath = os.path.join(self.infos_dirpath, PLAYERS_INFO_FILENAME)
        #print("Player info json filepath:", self.player_info_filepath)

    def find_godot_project_settings_file_path(self, context):
        self.godot_project_settings_filepath = os.path.join(self.infos_dirpath, GODOT_PROJECT_SETTINGS_INFO_FILENAME)
        #print("Godot project settings info json filepath:", self.godot_project_settings_filepath)

    def find_stages_info_file_path(self, context):
        self.stages_info_filepath = os.path.join(self.infos_dirpath, STAGES_INFO_FILENAME)
        #print("Godot stages settings info json filepath:", self.stages_info_filepath)

    def find_menus_info_file_path(self, context):
        self.menus_info_filepath = os.path.join(self.infos_dirpath, MENUS_INFO_FILENAME)
        #print("Godot menus settings info json filepath:", self.menus_info_filepath)

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
        print("Project exported!")
        return {'FINISHED'}


class OpenGodotProjectOperator(bpy.types.Operator): # It DOESN'T block blender execution until game exits
    """Open Godot Project Operator"""
    bl_idname = "scene.open_godot_project_operator"
    bl_label = "Open Godot Project"
    

    no_window : bpy.props.BoolProperty(name="no_window", default=False) # type: ignore

    def execute(self, context):
        print("Opening godot project...")
        _no_window_parameter = ""
        if self.no_window:
            _no_window_parameter = "--no-window"
        # TODO: Pending to fix zombie processes
        try:
            self.cmd = subprocess.Popen([bpy.path.abspath(context.scene.godot_executable), "--editor", _no_window_parameter, "--path", context.scene.project_folder], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        except:
            print("Godot executable error!")
            self.report({'INFO'}, "Godot executable error")
            context.scene.godot_export_ok = False
            context.scene.godot_exporting = False
            show_error_popup(["Godot executable error"], "Errors detected", "CANCEL")
            return {'FINISHED'}
        stdout, stderr = self.cmd.communicate()
        print("STDOUT:", stdout)
        print("STDERR:", stderr)
        if stdout.find("Godot Engine v3") < 0:
            print("Godot executable path is not correct")
            context.scene.godot_export_ok = False
            context.scene.godot_exporting = False
            show_error_popup(["Godot executable path is not correct"], "Errors detected", "CANCEL")
        if stdout.find("StageTemplateDone"):
            context.scene.godot_export_ok = True
            context.scene.godot_exporting = False
        return {'FINISHED'}

def init_properties():
    bpy.types.Scene.godot_export_ok = bpy.props.BoolProperty(name="Godot Expot OK", default=False)
    bpy.types.Scene.godot_exporting = bpy.props.BoolProperty(name="Godot Exporting", default=False)
    bpy.types.Scene.scenes_added_index = bpy.props.IntProperty(name = "Index for my_list", default = 0)
    bpy.types.Scene.startup_scene = bpy.props.PointerProperty(type=bpy.types.Scene, name="Startup Scene", poll=poll_startupable_scenes)
    # Panels checkboxes
    bpy.types.Scene.advanced_tools = bpy.props.BoolProperty(name="Advanced Tools", default=False)

def clear_properties():
    del bpy.types.Scene.startup_scene
    del bpy.types.Scene.scenes_added_index
    del bpy.types.Scene.advanced_tools

def register():
    init_properties()
    bpy.utils.register_class(AreYouSureDeletingOperator)
    bpy.utils.register_class(DeleteProjectOperator)
    bpy.utils.register_class(CreateGodotProjectOperator)
    bpy.utils.register_class(SCENES_UL_scenes_added)
    bpy.utils.register_class(RemoveSceneFromListOperator)
    bpy.utils.register_class(ExportGameOperator)
    bpy.utils.register_class(B2G_ToolsPanel)
    bpy.utils.register_class(OpenGodotProjectOperator)

def unregister():
    bpy.utils.unregister_class(AreYouSureDeletingOperator)
    bpy.utils.unregister_class(DeleteProjectOperator)
    bpy.utils.unregister_class(CreateGodotProjectOperator)
    bpy.utils.unregister_class(OpenGodotProjectOperator)
    bpy.utils.unregister_class(B2G_ToolsPanel)
    bpy.utils.unregister_class(ExportGameOperator)
    bpy.utils.unregister_class(RemoveSceneFromListOperator)
    bpy.utils.unregister_class(SCENES_UL_scenes_added)
    clear_properties()

