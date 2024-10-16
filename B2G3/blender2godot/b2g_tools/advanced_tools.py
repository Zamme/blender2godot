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
from mathutils import Vector, Matrix
from mathutils.geometry import normal
from numpy import cross, dot

import bpy
from blender2godot.addon_config import addon_config # type: ignore
from blender2godot.scene_properties import scene_properties # type: ignore

INFOS_FOLDER_NAME = "infos"
HUDS_INFO_FILENAME = "huds_info.json"
MENUS2D_INFO_FILENAME = "menus2d_info.json"
OVERLAY_MENUS_INFO_FILENAME = "overlays_info.json"
STAGES_INFO_FILENAME = "stages_info.json"
COLLIDERS_INFO_FILENAME = "colliders_info.json"
PLAYERS_INFO_FILENAME = "players_info.json"
MENUS3D_INFO_FILENAME = "menus3d_info.json"
NPCS_INFO_FILENAME = "npcs_info.json"
LOADING_INFO_FILENAME = "loadings_info.json"
LIGHTS_INFO_FILENAME = "lights_info.json"
GODOT_PROJECT_SETTINGS_INFO_FILENAME = "godot_project_settings.json"
GAME_MANAGER_INFO_FILENAME = "game_manager_info.json"

def Vector3ToString(_vector3):
    _string = str(_vector3[0]) + "," + str(_vector3[1]) + "," + str(_vector3[2])
    return _string

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
    return (((_scene.scene_type == "stage") or (_scene.scene_type == "2dmenu") or (_scene.scene_type == "3dmenu")) and (_scene.name != "B2G_GameManager") and (_scene.scene_exportable))

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
                #layout.prop(item, "scene_type", text="")
                _type_translated = ""
                for _s_type in scene_properties.scene_types:
                    if _s_type[0] == item.scene_type:
                        _type_translated = _s_type[1]
                layout.label(text=_type_translated)
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
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    #bl_options = {"DEFAULT_CLOSED"}
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
        row1 = layout.row()
        box0 = row1.box()
        box1 = box0.box()
        box1.label(text="Check scenes to export")
        if len(bpy.data.scenes) > 0:
            box1.template_list("SCENES_UL_scenes_added", "ScenesAddedList", bpy.data, "scenes", scene, "scenes_added_index")
            #box1.prop(scene, "startup_scene")
        else:
            box1.label(text="No scenes to add")

        # Export project to godot button
        row2 = box0.row()
        row2.scale_y = 2.0
        row2.operator("scene.export_project_to_godot_operator", icon="EXPORT")        
        #row2.enabled = (len(context.scene.current_export_issues) == 0)
        # ERRORS
        row5 = box0.row()
        if (len(context.scene.current_export_errors) == 0):
            row5.label(text="No errors", icon_value=addon_config.preview_collections[0]["ok_green"].icon_id)
        else:
            for _issue in context.scene.current_export_errors:
                _new_row = box0.row()
                _new_row.alert = True
                _new_row.label(text=_issue.description, icon="CANCEL")
        # WARNINGS
        if (len(context.scene.current_export_warnings) > 0):
            for _issue in context.scene.current_export_warnings:
                _new_row = box0.row()
                _new_row.label(text=_issue.description, icon="ERROR")
        # TOTAL REPORT
        row7 = box0.row()
        if (len(context.scene.current_export_warnings) == 0) and (len(context.scene.current_export_errors) == 0):
            row7.label(text="All OK", icon_value=addon_config.preview_collections[0]["ok_green"].icon_id)

        row3 = layout.row()
        row3.alignment="CENTER"
        row3.prop(context.scene, 'advanced_tools', icon="PLUS")

        if context.scene.advanced_tools:
            row4 = layout.row()
            box2 = row4.box()
            # Create project button
            box2.operator("scene.create_godot_project_operator", icon="PRESET_NEW")
            if (os.path.isdir(context.scene.project_folder) and (context.scene.godot_export_ok)):
                # Delete project button
                box2.operator(AreYouSureDeletingOperator.bl_idname, icon="TRASH")
                # Open godot project button
                box2.operator("scene.open_godot_project_operator", icon="GHOST_ENABLED")
                box2.operator("scene.open_godot_project_folder_operator", icon="FOLDER_REDIRECT")
            #row4.enabled = not self._err_detected

class ExportGameOperator(bpy.types.Operator):
    """Export Game Operator"""
    bl_idname = "scene.export_game_operator"
    bl_label = "Export Game"
    
    assets_folder_name = "assets"
    models_folder_name = "models"
    huds_folder_name = "huds"
    menus2d_folder_name = "menus2d"
    menus3d_folder_name = "menus3d"
    overlay_menus_folder_name = "overlays"
    players_folder_name = "players"
    stages_folder_name = "stages"
    colliders_filepath = ""
    player_info_filepath = ""
    lights_info_filepath = ""
    godot_project_settings_filepath = ""
    stages_info_filepath = ""
    
    #dict_colliders = my_dictionary()
    dict_players_info = my_dictionary()
    dict_lights_info = my_dictionary()
    dict_godot_project_settings = my_dictionary()
    dict_stages_info = my_dictionary()
    dict_menus3d_info = my_dictionary()
    dict_menus2d_info = my_dictionary()
    dict_overlay_menus_info = my_dictionary()
    dict_huds_info = my_dictionary()

    controls_list = get_controls_list()
  
    def check_custom_icon(self, context):
        _checked = False
        if os.path.exists(context.scene.game_icon):
            if (imghdr.what(context.scene.game_icon) == "png"):
                _checked = True
        return _checked
    
    '''
    def export_colliders(self, context, _scene):
        _last_scene = context.window.scene
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
        context.window.scene = _last_scene
    '''

    def export_environment(self, context, _scene):
        print("Exporting environment ...")
        _dict = my_dictionary()
        _sky = None
        _skydict = my_dictionary()
        if _scene.world:
            if _scene.world.use_nodes:
                _background_color = None
                _color_string = ""
                _world_nodes = _scene.world.node_tree.nodes
                for _world_node in _world_nodes:
                    print("Scanning node:", _world_node.bl_idname)
                    if _world_node.bl_idname == "ShaderNodeOutputWorld":
                        print("World output:", _world_node.name)
                        _surface_socket = _world_node.inputs["Surface"]
                        _surface_socket_links = _surface_socket.links
                        for _sslink in _surface_socket_links:
                            if _sslink.from_node.bl_idname == "ShaderNodeBackground":
                                _bg_node = _sslink.from_node
                                _background_color = _bg_node.inputs["Color"].default_value
                                _bg_color_input = _bg_node.inputs["Color"]
                                if len(_bg_color_input.links) > 0:
                                    if _bg_color_input.links[0].from_node.bl_idname == "ShaderNodeTexSky":
                                        print("Sky found!", _bg_color_input.links[0].from_node.name)
                                        _sky = _bg_color_input.links[0].from_node
                if _background_color is not None:
                    _color_string = Vector3ToString(_background_color)
                if _sky:
                    _skydict.add("Type", _sky.sky_type)
                    _skydict.add("SunDirection", Vector3ToString(_sky.sun_direction))
                    _skydict.add("SunElevation", _sky.sun_elevation)
                    _skydict.add("SunIntensity", _sky.sun_intensity)
                    _skydict.add("SunRotation", _sky.sun_rotation)
                    _skydict.add("SunSize", _sky.sun_size)
                    _dict.add("Sky", _skydict)
            else:
                _color_string = Vector3ToString(_scene.world.color)
            _dict.add("Color", _color_string)
        else:
            _dict = "None"
        print("Environment exported.")
        return _dict

    def export_game_manager(self, context):
        print("Exporting Game Manager...")
        self.find_game_manager_file_path(context)
        self.game_manager_dict = my_dictionary()
        self.game_manager_settings = my_dictionary()
        _gm_node_tree = bpy.data.node_groups.get("GameManager")
        _gm_nodes = _gm_node_tree.nodes
        _nodes_dict = my_dictionary()
        for _node in _gm_nodes:
            if _node.name == "Start":
                _starter_node_name = ""
                if len(_node.outputs[0].links) > 0:
                    _starter_node_name = _node.outputs[0].links[0].to_node.name
                self.game_manager_settings.add("StarterNode", _starter_node_name)
                self.game_manager_settings.add("DebugEnabled", _node.debug_enabled)
            else:
                print("Exporting node:", _node.name)
                _current_node_dict = my_dictionary()
                _current_node_dict.add("Name", _node.name)
                _current_node_dict.add("Type", type(_node).__name__)
                # NODE PROPERTIES
                if hasattr(_node, "node_properties"):
                    _current_node_props_dict = my_dictionary()
                    for key in _node.node_properties.__annotations__.keys():
                        the_value = getattr(_node.node_properties, key)
                        _current_node_props_dict.add(key, the_value)
                    _current_node_dict.add("NodeProperties", _current_node_props_dict)
                # NODE ACTIONS
                if hasattr(_node, "actions_settings"):
                    _current_node_actions_dict = my_dictionary()
                    for _action_setting in _node.actions_settings:
                        _current_node_actions_dict.add(_action_setting.action_id, _action_setting.action_process)
                    _current_node_dict.add("ActionsSettings", _current_node_actions_dict)
                # NODE INPUT SOCKETS
                if len(_node.inputs) > 0:
                    _current_node_inputs = my_dictionary()
                    for _input in _node.inputs:
                        _new_input_dict = my_dictionary()
                        if _input.is_linked:
                            _new_input_dict.add("SourceNodeName", _input.links[0].from_node.name)
                            _new_input_dict.add("SourceNodeSocket", _input.links[0].from_socket.name)
                        else:
                            if hasattr(_input, "default_value"):
                                _new_input_dict.add("DefaultValue", _input.default_value)
                        _current_node_inputs.add(_input.name, _new_input_dict)
                    _current_node_dict.add("NodeInputs", _current_node_inputs)
                # NODE OUTPUT SOCKETS
                if len(_node.outputs) > 0:
                    _current_node_outputs = my_dictionary()
                    for _output in _node.outputs:
                        _new_output_dict = my_dictionary()
                        if _output.is_linked:
                            for _link_index,_link in enumerate(_output.links):
                                _link_dict = my_dictionary()
                                _link_dict.add("DestNodeName", _link.to_node.name)
                                _link_dict.add("DestNodeSocket", _link.to_socket.name)
                                _new_output_dict.add(_link_index, _link_dict)
                        else:
                            if hasattr(_output, "default_value"):
                                _new_output_dict.add("DefaultValue", _output.default_value)
                        _current_node_outputs.add(_output.name, _new_output_dict)
                    _current_node_dict.add("NodeOutputs", _current_node_outputs)
                # TODO : (LAST CODE CHANGES AT DESKTOP BACKUP)

                _nodes_dict.add(_node.name, _current_node_dict)
        
        self.game_manager_dict.add("Nodes", _nodes_dict)
        self.game_manager_dict.add("Settings", self.game_manager_settings)

        self.game_manager_info = json.dumps(self.game_manager_dict, indent=1, ensure_ascii=True)
        with open(self.game_manager_filepath, 'w') as outfile:
            outfile.write(self.game_manager_info + '\n')
        print("Game Manager exported.")

    def export_game_project(self, context):
        print("Exporting game", context.scene.project_folder)
        self.infos_dirpath = os.path.join(context.scene.project_folder, INFOS_FOLDER_NAME)
        if not os.path.isdir(self.infos_dirpath):
            os.mkdir(self.infos_dirpath)
        #self.fix_objects_names(context)
        self.models_folder_path = os.path.join(self.assets_folder_path, self.models_folder_name)
        if not os.path.isdir(self.models_folder_path):
            os.mkdir(self.models_folder_path)
        for _sc_added in bpy.data.scenes:
            if _sc_added.scene_exportable:
                match _sc_added.scene_type:
                    case "hud":
                        self.export_hud(context, _sc_added)
                        self.export_hud_dict(context, _sc_added)
                    case "2dmenu":
                        self.export_menu2d(context, _sc_added)
                        self.export_menu2d_dict(context, _sc_added)
                    case "stage":
                        self.export_scene(context, _sc_added)
                        #self.export_colliders(context, _sc_added)
                        self.export_lights(context)
                        self.export_stage_info(context, _sc_added)
                    case "player":
                        self.export_scene(context, _sc_added)
                        self.export_player_info(context, _sc_added)
                    case "3dmenu":
                        self.export_scene(context, _sc_added)
                        self.export_menu3d_dict(context, _sc_added)
                    case "overlay_menu":
                        self.export_overlay_menu(context, _sc_added)
                        self.export_overlay_menu_dict(context, _sc_added)
        self.export_stages_info(context)
        self.export_players_info(context)
        self.export_menus2d_info(context)
        self.export_menus3d_info(context)
        self.export_overlay_menu_info(context)
        self.export_huds_info(context)
        self.export_icon(context)
        self.export_godot_project_settings(context)
        self.export_game_manager(context)
        # Reset GameManager Workspace
        for _area in context.screen.areas:
            if _area.type != "NODE_EDITOR":
                _area.type = "NODE_EDITOR"
                _area.ui_type = "GameManagerTreeType"

    def export_godot_project_settings(self, context):
        print("Exporting project settings...")

        self.find_godot_project_settings_file_path(context)

        self.app_settings_dict = my_dictionary()
        self.display_settings_dict = my_dictionary()
        self.other_settings_dict = my_dictionary()
        self.default_environment_dict = my_dictionary()

        # Config name
        self.app_settings_dict.add("application/config/name", context.scene.game_name)
        # Startup scene
        #if context.scene.startup_scene:
            #self.other_settings_dict.add("startup_scene_type", context.scene.startup_scene.scene_type)
            #self.app_settings_dict.add("application/run/main_scene", context.scene.startup_scene.name)
        # Display settings
        self.display_settings_dict.add("display/window/size/width", bpy.data.scenes["B2G_GameManager"].render.resolution_x)
        self.display_settings_dict.add("display/window/size/height", bpy.data.scenes["B2G_GameManager"].render.resolution_y)
        self.display_settings_dict.add("display/window/size/resizable", context.scene.display_resizable)
        self.display_settings_dict.add("display/window/size/borderless", context.scene.display_borderless)
        self.display_settings_dict.add("display/window/size/fullscreen", context.scene.display_fullscreen)
        self.display_settings_dict.add("display/window/size/always_on_top", context.scene.display_alwaysontop)
        # Boot splash settings
        self.app_settings_dict.add("application/boot_splash/show_image", context.scene.splash_showimage)
        self.app_settings_dict.add("application/boot_splash/image", context.scene.splash_image)
        self.app_settings_dict.add("application/boot_splash/fullsize", context.scene.splash_fullsize)
        self.app_settings_dict.add("application/boot_splash/use_filter", context.scene.splash_usefilter)
        _color_string = str(context.scene.splash_bgcolor[0]) + "," + str(context.scene.splash_bgcolor[1]) + "," + str(context.scene.splash_bgcolor[2]) + "," + str(context.scene.splash_bgcolor[3])
        self.app_settings_dict.add("application/boot_splash/bg_color", _color_string)
        # Default environment
        self.default_environment_dict = self.export_environment(context, context.scene)

        # Add all dicts
        self.dict_godot_project_settings.add("AppSettings", self.app_settings_dict)
        self.dict_godot_project_settings.add("DisplaySettings", self.display_settings_dict)
        self.dict_godot_project_settings.add("OtherSettings", self.other_settings_dict)
        self.dict_godot_project_settings.add("DefaultEnvironment", self.default_environment_dict)
        #self.dict_godot_project_settings.add("DebugHudEnabled", context.scene.debug_hud_enabled)

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
        _last_scene = context.window.scene
        self.huds_folder_path = os.path.join(self.assets_folder_path, self.huds_folder_name)
        if not os.path.isdir(self.huds_folder_path):
            os.mkdir(self.huds_folder_path)
        print("Exporting hud scene", _hud_scene.name)
        context.window.scene = _hud_scene
        # ENSURE 3D VIEW FOR CONTEXT
        for _area in bpy.context.screen.areas:
            if _area.type == "NODE_EDITOR":
                _area.type = "VIEW_3D"
                _area.ui_type = "VIEW_3D"
        bpy.ops.view3d.view_camera()
        _last_use_border = _hud_scene.render.use_border
        _last_use_crop_to_border = _hud_scene.render.use_crop_to_border
        _hud_scene.render.use_border = True
        _hud_scene.render.use_crop_to_border = True
        cam = _hud_scene.camera 
        camType = cam.data.type
        matrix = cam.matrix_world.normalized()
        frame = [matrix @ v for v in cam.data.view_frame(scene=_hud_scene)]
        origin = matrix.to_translation()
        frame.append(origin)
        p1, p2, p3, p4 = frame[0:4]
        l = cam.location
        v1 = p2 - p3
        v2 = p4 - p3
        normal = cross(v1, v2)
        hud_path = os.path.join(self.huds_folder_path, _hud_scene.name)
        _hud_scene.render.engine = "BLENDER_EEVEE"
        objs = []
        s1s = []
        s2s = []
        for _obj in _hud_scene.objects:
            if _obj.type == "GPENCIL":
                if _obj.godot_exportable:
                    objs.append(_obj)
                    for _obj2 in _hud_scene.objects:
                        _obj2.hide_render = (_obj2 != _obj)
                    for _layer in _obj.data.layers:
                        _layer.use_lights = False
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    s1s.clear()
                    s2s.clear()
                    verts = [_obj.matrix_world @ v.co for v in _obj.data.layers[0].active_frame.strokes[0].points]
                    for v in verts:
                        # direction of line to be parameterized, if orthogonal, direction should be normal
                        if camType == 'ORTHO':
                            direction = normal
                        else:
                            direction = l - v
                        # parametric value for projection to camera
                        t = -(dot(normal, v) - dot(p1, normal))/dot(normal, direction)
                        # vert projected to camera frustum
                        vP = v + Vector(t * direction)
                        # matrix with v1 and v2 as basis vectors (has to be square in order to invert)      
                        mtxB = Matrix((v1, v2)).to_3x3()
                        # find scalars to stretch basis vectors to projected point on frustum
                        scalars = (vP - p3) @ mtxB.inverted() 
                        # horizontal scalar append to all horizontal scalars:
                        s1s.append(scalars[0])
                        # vertical scalar append to all vertical scalars:
                        s2s.append(scalars[1])
                    x_min, y_min, x_max, y_max = min(s1s), min(s2s), max(s1s), max(s2s)

                    _hud_scene.render.border_min_x = x_min
                    _hud_scene.render.border_min_y = y_min
                    _hud_scene.render.border_max_x = x_max
                    _hud_scene.render.border_max_y = y_max

                    _file_path = hud_path + "_" + _obj.name + ".png"
                    _hud_scene.render.filepath = _file_path
                    _hud_scene.render.film_transparent = True
                    _hud_scene.view_layers["ViewLayer"].use_pass_z = True
                    bpy.ops.render.render(write_still = True, use_viewport=True)
        if len(objs) > 0:
            print("Scene", _hud_scene.name, "exported with", str(len(objs)), "objects.")
        else:
            print("Scene ", _hud_scene.name, " empty!")
        _hud_scene.render.use_border = _last_use_border
        _hud_scene.render.use_crop_to_border = _last_use_border
        for _obj in _hud_scene.objects:
            _obj.hide_render = False
        context.window.scene = _last_scene

    def export_hud_dict(self, context, _sc_added):
        _hud_dict = my_dictionary()
        _hud_objects_dict = my_dictionary()
        for _hud_obj in _sc_added.objects:
            _hud_object_dict = my_dictionary()
            #if hasattr(_hud_obj, "is_containing_element"):
                #if _hud_obj.is_containing_element:
            _hud_object_dict.add("Type", _hud_obj.type)
            _hud_object_dict.add("ElementType", _hud_obj.hud_element_properties.element_type)
            loc, rot, sca = _hud_obj.matrix_world.decompose()
            _hud_object_dict.add("Location", Vector3ToString(loc))
            match _hud_obj.type:
                case "FONT":
                    _hud_object_dict.add("FontFilepath", _hud_obj.data.font.filepath)
                    _hud_object_dict.add("Body", _hud_obj.data.body)
                    _hud_object_dict.add("Size", _hud_obj.data.size)
                case "GPENCIL":
                    _co_array = []
                    for _point in _hud_obj.data.layers[0].active_frame.strokes[0].points:
                        _co_array.append([_point.co[0], _point.co[1], _point.co[2]])
                    _hud_object_dict.add("Points", _co_array)
            _hud_objects_dict.add(_hud_obj.name, _hud_object_dict)
        _hud_dict.add("Objects", _hud_objects_dict)
        self.dict_huds_info.add(_sc_added.name, _hud_dict)

    def export_huds_info(self, context):
        self.find_huds_info_file_path(context)
        self.data_huds_info = json.dumps(self.dict_huds_info, indent=1, ensure_ascii=True)
        with open(self.huds_info_filepath, 'w') as outfile:
            outfile.write(self.data_huds_info + '\n')   

    def export_lights(self, context):
        _last_scene = context.window.scene
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
        context.window.scene = _last_scene
    
    def export_menu2d(self, context, _menu2d_scene):
        _last_scene = context.window.scene
        self.menus2d_folder_path = os.path.join(self.assets_folder_path, self.menus2d_folder_name)
        if not os.path.isdir(self.menus2d_folder_path):
            os.mkdir(self.menus2d_folder_path)
        print("Exporting menu 2d scene", _menu2d_scene.name)
        context.window.scene = _menu2d_scene
        # ENSURE 3D VIEW FOR CONTEXT
        for _area in bpy.context.screen.areas:
            if _area.type == "NODE_EDITOR":
                _area.type = "VIEW_3D"
                _area.ui_type = "VIEW_3D"
        bpy.ops.view3d.view_camera()
        _last_use_border = _menu2d_scene.render.use_border
        _last_use_crop_to_border = _menu2d_scene.render.use_crop_to_border
        _menu2d_scene.render.use_border = True
        _menu2d_scene.render.use_crop_to_border = True
        cam = _menu2d_scene.camera 
        camType = cam.data.type
        matrix = cam.matrix_world.normalized()
        frame = [matrix @ v for v in cam.data.view_frame(scene=_menu2d_scene)]
        origin = matrix.to_translation()
        frame.append(origin)
        p1, p2, p3, p4 = frame[0:4]
        l = cam.location
        v1 = p2 - p3
        v2 = p4 - p3
        normal = cross(v1, v2)
        hud_path = os.path.join(self.menus2d_folder_path, _menu2d_scene.name)
        _menu2d_scene.render.engine = "BLENDER_EEVEE"
        objs = []
        s1s = []
        s2s = []
        for _obj in _menu2d_scene.objects:
            if _obj.type == "GPENCIL":
                if _obj.godot_exportable:
                    objs.append(_obj)
                    for _obj2 in _menu2d_scene.objects:
                        _obj2.hide_render = (_obj2 != _obj)
                    for _layer in _obj.data.layers:
                        _layer.use_lights = False
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    s1s.clear()
                    s2s.clear()
                    verts = [_obj.matrix_world @ v.co for v in _obj.data.layers[0].active_frame.strokes[0].points]
                    for v in verts:
                        # direction of line to be parameterized, if orthogonal, direction should be normal
                        if camType == 'ORTHO':
                            direction = normal
                        else:
                            direction = l - v
                        # parametric value for projection to camera
                        t = -(dot(normal, v) - dot(p1, normal))/dot(normal, direction)
                        # vert projected to camera frustum
                        vP = v + Vector(t * direction)
                        # matrix with v1 and v2 as basis vectors (has to be square in order to invert)      
                        mtxB = Matrix((v1, v2)).to_3x3()
                        # find scalars to stretch basis vectors to projected point on frustum
                        scalars = (vP - p3) @ mtxB.inverted() 
                        # horizontal scalar append to all horizontal scalars:
                        s1s.append(scalars[0])
                        # vertical scalar append to all vertical scalars:
                        s2s.append(scalars[1])
                    x_min, y_min, x_max, y_max = min(s1s), min(s2s), max(s1s), max(s2s)

                    _menu2d_scene.render.border_min_x = x_min
                    _menu2d_scene.render.border_min_y = y_min
                    _menu2d_scene.render.border_max_x = x_max
                    _menu2d_scene.render.border_max_y = y_max

                    _file_path = hud_path + "_" + _obj.name + ".png"
                    _menu2d_scene.render.filepath = _file_path
                    _menu2d_scene.render.film_transparent = True
                    _menu2d_scene.view_layers["ViewLayer"].use_pass_z = True
                    bpy.ops.render.render(write_still = True, use_viewport=True)
        if len(objs) > 0:
            print("Scene", _menu2d_scene.name, "exported with", str(len(objs)), "objects.")
        else:
            print("Scene ", _menu2d_scene.name, " empty!")
        _menu2d_scene.render.use_border = _last_use_border
        _menu2d_scene.render.use_crop_to_border = _last_use_border
        for _obj in _menu2d_scene.objects:
            _obj.hide_render = False
        context.window.scene = _last_scene

    def export_menu2d_dict(self, context, _sc_added):
        _menu2d_dict = my_dictionary()
        _menu2d_objects_dict = my_dictionary()
        for _menu2d_obj in _sc_added.objects:
            _menu2d_object_dict = my_dictionary()
            _menu2d_object_dict.add("Type", _menu2d_obj.type)
            _menu2d_object_dict.add("ElementType", _menu2d_obj.menu2d_object_properties.menu2d_object_type)
            loc, rot, sca = _menu2d_obj.matrix_world.decompose()
            _menu2d_object_dict.add("Location", Vector3ToString(loc))
            _menu2d_object_dict.add("Depth", _menu2d_obj.menu2d_object_properties.object_depth)
            match _menu2d_obj.type:
                case "FONT":
                    _menu2d_object_dict.add("FontFilepath", _menu2d_obj.data.font.filepath)
                    _menu2d_object_dict.add("Body", _menu2d_obj.data.body)
                    _menu2d_object_dict.add("Size", _menu2d_obj.data.size)
                case "GPENCIL":
                    _co_array = []
                    for _point in _menu2d_obj.data.layers[0].active_frame.strokes[0].points:
                        _co_array.append([_point.co[0], _point.co[1], _point.co[2]])
                    _menu2d_object_dict.add("Points", _co_array)
            match _menu2d_obj.menu2d_object_properties.menu2d_object_type:
                case "button":
                    _nav_props = my_dictionary()
                    if _menu2d_obj.menu2d_button_navigation_properties.navigation_up:
                        _nav_props.add("NavigationUp", _menu2d_obj.menu2d_button_navigation_properties.navigation_up.name)
                    if _menu2d_obj.menu2d_button_navigation_properties.navigation_down:
                        _nav_props.add("NavigationDown", _menu2d_obj.menu2d_button_navigation_properties.navigation_down.name)
                    if _menu2d_obj.menu2d_button_navigation_properties.navigation_left:
                        _nav_props.add("NavigationLeft", _menu2d_obj.menu2d_button_navigation_properties.navigation_left.name)
                    if _menu2d_obj.menu2d_button_navigation_properties.navigation_right:
                        _nav_props.add("NavigationRight", _menu2d_obj.menu2d_button_navigation_properties.navigation_right.name)
                    _menu2d_object_dict.add("Navigation", _nav_props)
                case "button_content":
                    _menu2d_object_dict.add("Container", _menu2d_obj.parent.name)
            _menu2d_objects_dict.add(_menu2d_obj.name, _menu2d_object_dict)
        _menu2d_dict.add("Objects", _menu2d_objects_dict)
        if _sc_added.menu2d_default_button_selected:
            _menu2d_dict.add("DefaultButtonSelected", _sc_added.menu2d_default_button_selected.name)
        # CONTROLS
        _controls_dictionary = my_dictionary()
        for _control_setting in _sc_added.menu2d_controls_settings:
            _control_inputs_array = []
            for _mot_input in _control_setting.motion_inputs:
                _inputs = [_mot_input.motion_input_type,
                            _mot_input.motion_input_blender,
                            self.controls_list[(_mot_input.motion_input_type).capitalize()][_mot_input.motion_input_blender]["GodotID"],
                            self.controls_list[(_mot_input.motion_input_type).capitalize()][_mot_input.motion_input_blender]["GodotEnumID"],
                            _mot_input.motion_input_modifier]
                _control_inputs_array.append(_inputs)
            _controls_dictionary.add(_control_setting.motion_name, _control_inputs_array)
        _menu2d_dict.add("MenuControls", _controls_dictionary)
        self.dict_menus2d_info.add(_sc_added.name, _menu2d_dict)

    def export_menus2d_info(self, context):
        self.find_menus2d_info_file_path(context)
        self.data_menus2d_info = json.dumps(self.dict_menus2d_info, indent=1, ensure_ascii=True)
        with open(self.menus2d_info_filepath, 'w') as outfile:
            outfile.write(self.data_menus2d_info + '\n')   

    def export_menu3d_dict(self, context, _sc_added):
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
        _temp_dict.add("SceneName", _sc_added.name)
        # MENU'S SPECIAL OBJECTS
        _special_objects = my_dictionary()
        for _obj in _sc_added.objects:
            if hasattr(_obj, "special_object_info"):
                if _obj.special_object_info.menu_object_type != "none":
                    _obj_dict = my_dictionary()
                    _obj_dict.add("ObjectType", _obj.special_object_info.menu_object_type)
                    _nav_props = my_dictionary()
                    if _obj.menu3d_button_navigation_properties.navigation_up:
                        _nav_props.add("NavigationUp", _obj.menu3d_button_navigation_properties.navigation_up.name)
                    if _obj.menu3d_button_navigation_properties.navigation_down:
                        _nav_props.add("NavigationDown", _obj.menu3d_button_navigation_properties.navigation_down.name)
                    if _obj.menu3d_button_navigation_properties.navigation_left:
                        _nav_props.add("NavigationLeft", _obj.menu3d_button_navigation_properties.navigation_left.name)
                    if _obj.menu3d_button_navigation_properties.navigation_right:
                        _nav_props.add("NavigationRight", _obj.menu3d_button_navigation_properties.navigation_right.name)
                    _obj_dict.add("Navigation", _nav_props)
                    _special_objects.add(_obj.name, _obj_dict)
        _temp_dict.add("SpecialObjects", _special_objects)
        # ENVIRONMENT
        _temp_dict.add("DefaultEnvironment", self.export_environment(context, _sc_added))
        # ADD DICT TO INFO
        _menu_name = "Menu3d_" + _sc_added.name
        if _sc_added.menu3d_default_button_selected:
            _temp_dict.add("DefaultButtonSelected", _sc_added.menu3d_default_button_selected.name)
        self.dict_menus3d_info.add(_menu_name, _temp_dict)

    def export_menus3d_info(self, context):
        self.find_menus3d_info_file_path(context)
        self.data_menus3d_info = json.dumps(self.dict_menus3d_info, indent=1, ensure_ascii=True)
        with open(self.menus3d_info_filepath, 'w') as outfile:
            outfile.write(self.data_menus3d_info + '\n')   

    def export_overlay_menu(self, context, _overlay_menu_scene):
        _last_scene = context.window.scene
        self.overlay_menus_folder_path = os.path.join(self.assets_folder_path, self.overlay_menus_folder_name)
        if not os.path.isdir(self.overlay_menus_folder_path):
            os.mkdir(self.overlay_menus_folder_path)
        print("Exporting overlay menu scene", _overlay_menu_scene.name)
        context.window.scene = _overlay_menu_scene
        # ENSURE 3D VIEW FOR CONTEXT
        for _area in bpy.context.screen.areas:
            if _area.type == "NODE_EDITOR":
                _area.type = "VIEW_3D"
                _area.ui_type = "VIEW_3D"
        bpy.ops.view3d.view_camera()
        _last_use_border = _overlay_menu_scene.render.use_border
        _last_use_crop_to_border = _overlay_menu_scene.render.use_crop_to_border
        _overlay_menu_scene.render.use_border = True
        _overlay_menu_scene.render.use_crop_to_border = True
        cam = _overlay_menu_scene.camera 
        camType = cam.data.type
        matrix = cam.matrix_world.normalized()
        frame = [matrix @ v for v in cam.data.view_frame(scene=_overlay_menu_scene)]
        origin = matrix.to_translation()
        frame.append(origin)
        p1, p2, p3, p4 = frame[0:4]
        l = cam.location
        v1 = p2 - p3
        v2 = p4 - p3
        normal = cross(v1, v2)
        hud_path = os.path.join(self.overlay_menus_folder_path, _overlay_menu_scene.name)
        _overlay_menu_scene.render.engine = "BLENDER_EEVEE"
        objs = []
        s1s = []
        s2s = []
        for _obj in _overlay_menu_scene.objects:
            if _obj.type == "GPENCIL":
                if _obj.godot_exportable:
                    objs.append(_obj)
                    for _obj2 in _overlay_menu_scene.objects:
                        _obj2.hide_render = (_obj2 != _obj)
                    for _layer in _obj.data.layers:
                        _layer.use_lights = False
                    bpy.ops.object.mode_set(mode = 'OBJECT')
                    s1s.clear()
                    s2s.clear()
                    verts = [_obj.matrix_world @ v.co for v in _obj.data.layers[0].active_frame.strokes[0].points]
                    for v in verts:
                        # direction of line to be parameterized, if orthogonal, direction should be normal
                        if camType == 'ORTHO':
                            direction = normal
                        else:
                            direction = l - v
                        # parametric value for projection to camera
                        t = -(dot(normal, v) - dot(p1, normal))/dot(normal, direction)
                        # vert projected to camera frustum
                        vP = v + Vector(t * direction)
                        # matrix with v1 and v2 as basis vectors (has to be square in order to invert)      
                        mtxB = Matrix((v1, v2)).to_3x3()
                        # find scalars to stretch basis vectors to projected point on frustum
                        scalars = (vP - p3) @ mtxB.inverted() 
                        # horizontal scalar append to all horizontal scalars:
                        s1s.append(scalars[0])
                        # vertical scalar append to all vertical scalars:
                        s2s.append(scalars[1])
                    x_min, y_min, x_max, y_max = min(s1s), min(s2s), max(s1s), max(s2s)

                    _overlay_menu_scene.render.border_min_x = x_min
                    _overlay_menu_scene.render.border_min_y = y_min
                    _overlay_menu_scene.render.border_max_x = x_max
                    _overlay_menu_scene.render.border_max_y = y_max

                    _file_path = hud_path + "_" + _obj.name + ".png"
                    _overlay_menu_scene.render.filepath = _file_path
                    _overlay_menu_scene.render.film_transparent = True
                    _overlay_menu_scene.view_layers["ViewLayer"].use_pass_z = True
                    bpy.ops.render.render(write_still = True, use_viewport=True)
        if len(objs) > 0:
            print("Scene", _overlay_menu_scene.name, "exported with", str(len(objs)), "objects.")
        else:
            print("Scene ", _overlay_menu_scene.name, " empty!")
        _overlay_menu_scene.render.use_border = _last_use_border
        _overlay_menu_scene.render.use_crop_to_border = _last_use_border
        for _obj in _overlay_menu_scene.objects:
            _obj.hide_render = False
        context.window.scene = _last_scene

    def export_overlay_menu_dict(self, context, _sc_added):
        _overlay_menu_dict = my_dictionary()
        _overlay_menu_objects_dict = my_dictionary()
        for _overlay_menu_obj in _sc_added.objects:
            _overlay_menu_object_dict = my_dictionary()
            _overlay_menu_object_dict.add("Type", _overlay_menu_obj.type)
            _overlay_menu_object_dict.add("ElementType", _overlay_menu_obj.menu_overlay_object_properties.menu_overlay_object_type)
            loc, rot, sca = _overlay_menu_obj.matrix_world.decompose()
            _overlay_menu_object_dict.add("Location", Vector3ToString(loc))
            _overlay_menu_object_dict.add("Depth", _overlay_menu_obj.menu_overlay_object_properties.object_depth)
            match _overlay_menu_obj.type:
                case "FONT":
                    _overlay_menu_object_dict.add("FontFilepath", _overlay_menu_obj.data.font.filepath)
                    _overlay_menu_object_dict.add("Body", _overlay_menu_obj.data.body)
                    _overlay_menu_object_dict.add("Size", _overlay_menu_obj.data.size)
                case "GPENCIL":
                    _co_array = []
                    for _point in _overlay_menu_obj.data.layers[0].active_frame.strokes[0].points:
                        _co_array.append([_point.co[0], _point.co[1], _point.co[2]])
                    _overlay_menu_object_dict.add("Points", _co_array)
            if _overlay_menu_obj.menu_overlay_object_properties.menu_overlay_object_type == "button_content":
                _overlay_menu_object_dict.add("Container", _overlay_menu_obj.parent.name)
            _overlay_menu_objects_dict.add(_overlay_menu_obj.name, _overlay_menu_object_dict)
        _overlay_menu_dict.add("Objects", _overlay_menu_objects_dict)
        self.dict_overlay_menus_info.add(_sc_added.name, _overlay_menu_dict)

    def export_overlay_menu_info(self, context):
        self.find_overlay_menus_info_file_path(context)
        self.data_overlay_menus_info = json.dumps(self.dict_overlay_menus_info, indent=1, ensure_ascii=True)
        with open(self.overlay_menus_info_filepath, 'w') as outfile:
            outfile.write(self.data_overlay_menus_info + '\n')   

    def export_player_info(self, context, _player_scene):
        print("Exporting player...")
        # GENERAL PROPS
        self.dict_player_info = my_dictionary()
        self.dict_player_info.add("PlayerSceneName", _player_scene.name)
        if _player_scene.player_object:
            self.dict_player_info.add("PlayerObjectName", _player_scene.player_object.name)
        self.dict_player_info.add("GravityOn", _player_scene.player_gravity_on)
        if _player_scene.player_object:
            if _player_scene.player_object.collider != "none":
                _player_physics_groups = []
                for _group in _player_scene.player_object.physics_group:
                    _player_physics_groups.append(_group)
                self.dict_player_info.add("PhysicsGroup",_player_physics_groups)
        # SCENE PROPERTIES
        _scene_properties = my_dictionary()
        print("Jsoning scene properties...")
        for _player_scene_property in _player_scene.entity_properties:
            print("Adding property", _player_scene_property.property_name)
            _prop_value = _player_scene_property.property_value
            _scene_properties.add(_player_scene_property.property_name, {"Type" : _player_scene_property.property_type,
                                                                        "Value" : _prop_value})
        self.dict_player_info.add("PlayerSceneProperties", _scene_properties)
        # DIMENSIONS
        self.dict_player_info.add("PlayerDimensions", {"DimX" : _player_scene.player_object.dimensions.x,
                                                       "DimY" : _player_scene.player_object.dimensions.y,
                                                       "DimZ" : _player_scene.player_object.dimensions.z})
        # PLAYER CAMERA
        if _player_scene.camera_object:
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
        # TODO: DATA.ACTIONS IS RETRIEVING ALL BPY.DATA ACTIONS! RESTRICT TO PLAYER ACTIONS!
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
        # OBJECTS PROPERTIES
        _objects_properties = my_dictionary()
        print("Jsoning objects properties...")
        for _object in _player_scene.objects:
            _object_properties = my_dictionary()
            for _scene_object_property in _object.entity_properties:
                print("Adding property", _scene_object_property.property_name)
                _object_properties.add(_scene_object_property.property_name, {"Type" : _scene_object_property.property_type,
                                                                            "Value" : _scene_object_property.property_value})
            _objects_properties.add(_object.name, _object_properties)
        self.dict_player_info.add("ObjectsProperties", _objects_properties)
        
        # ADD to global
        self.dict_players_info.add(_player_scene.name, self.dict_player_info)

    def export_players_info(self, context):
        # EXPORT JSON
        #print(self.dict_players_info)
        self.find_players_info_file_path(context)
        self.data_players_info = json.dumps(self.dict_players_info, indent=1, ensure_ascii=True)
        with open(self.players_info_filepath, 'w') as outfile:
            outfile.write(self.data_players_info + '\n')   

    def export_scene(self, context, _scene):
        print("Exporting scene", _scene.name)
        _last_scene = context.window.scene
        context.window.scene = _scene
        model_path = os.path.join(self.models_folder_path, _scene.name)
        for ob in _scene.objects:
            ob.select_set(ob.godot_exportable)
        if len(_scene.objects) > 0:
            bpy.ops.export_scene.gltf(filepath=model_path, use_selection=True, export_apply=True, export_lights=True, use_active_scene=True)
            print("Scene", _scene.name, "exported.")
        else:
            print("Scene ", _scene.name, " empty!")
        context.window.scene = _last_scene
    
    def export_stage_info(self, context, _stage_scene):
        _stage_dict = my_dictionary()
        _stage_dict.add("SceneName", _stage_scene.name)
        #if not _stage_scene.player_spawn_empty:
            #_stage_dict.add("PlayerSpawnObjectName", "")
        #else:
            #_stage_dict.add("PlayerSpawnObjectName", _stage_scene.player_spawn_empty.name)
        _stage_dict.add("DefaultEnvironment", self.export_environment(context, _stage_scene))
        _stage_objects = my_dictionary()
        for _stage_object in _stage_scene.objects:
            _stage_object_dict = my_dictionary()
            #_stage_object_dict.add("Name", _stage_object.name)
            _stage_object_dict.add("Type", _stage_object.object_type)
            _stage_object_dict.add("Visible", _stage_object.is_visible)
            _stage_object_dict.add("Collider", _stage_object.collider)
            if ((_stage_object.object_type == "trigger_zone") or (_stage_object.collider != "none")):
                _stage_object_physics_groups = []
                for _group in _stage_object.physics_group:
                    _stage_object_physics_groups.append(_group)
                _stage_object_dict.add("PhysicsGroup", _stage_object_physics_groups)
            _stage_objects.add(_stage_object.name, _stage_object_dict)
        _stage_dict.add("Objects", _stage_objects)
        _stage_name = "Stage_" + _stage_scene.name
        self.dict_stages_info.add(_stage_name, _stage_dict)

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
        
    def find_menus2d_info_file_path(self, context):
        self.menus2d_info_filepath = os.path.join(self.infos_dirpath, MENUS2D_INFO_FILENAME)

    def find_overlay_menus_info_file_path(self, context):
        self.overlay_menus_info_filepath = os.path.join(self.infos_dirpath, OVERLAY_MENUS_INFO_FILENAME)

    def find_players_info_file_path(self, context):
        self.players_info_filepath = os.path.join(self.infos_dirpath, PLAYERS_INFO_FILENAME)
        #print("Player info json filepath:", self.player_info_filepath)

    def find_game_manager_file_path(self, context):
        self.game_manager_filepath = os.path.join(self.infos_dirpath, GAME_MANAGER_INFO_FILENAME)

    def find_godot_project_settings_file_path(self, context):
        self.godot_project_settings_filepath = os.path.join(self.infos_dirpath, GODOT_PROJECT_SETTINGS_INFO_FILENAME)
        #print("Godot project settings info json filepath:", self.godot_project_settings_filepath)

    def find_stages_info_file_path(self, context):
        self.stages_info_filepath = os.path.join(self.infos_dirpath, STAGES_INFO_FILENAME)
        #print("Godot stages settings info json filepath:", self.stages_info_filepath)

    def find_menus3d_info_file_path(self, context):
        self.menus3d_info_filepath = os.path.join(self.infos_dirpath, MENUS3D_INFO_FILENAME)
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
            print("Godot importing error or executable path is not correct")
            context.scene.godot_export_ok = False
            context.scene.godot_exporting = False
            show_error_popup(["Godot importing error or executable path is not correct"], "Errors detected", "CANCEL")
        if stdout.find("StageTemplateDone"):
            context.scene.godot_export_ok = True
            context.scene.godot_exporting = False
        return {'FINISHED'}

def init_properties():
    bpy.types.Scene.godot_export_ok = bpy.props.BoolProperty(name="Godot Expot OK", default=False)
    bpy.types.Scene.godot_exporting = bpy.props.BoolProperty(name="Godot Exporting", default=False)
    bpy.types.Scene.scenes_added_index = bpy.props.IntProperty(name = "Index for my_list", default = 0)
    #bpy.types.Scene.startup_scene = bpy.props.PointerProperty(type=bpy.types.Scene, name="Startup Scene", poll=poll_startupable_scenes)
    # Panels checkboxes
    bpy.types.Scene.advanced_tools = bpy.props.BoolProperty(name="Advanced Tools", default=False)

def clear_properties():
    #del bpy.types.Scene.startup_scene
    del bpy.types.Scene.scenes_added_index
    del bpy.types.Scene.advanced_tools
    del bpy.types.Scene.godot_export_ok
    del bpy.types.Scene.godot_exporting

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

