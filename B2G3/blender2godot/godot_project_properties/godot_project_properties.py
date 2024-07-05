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
For Godot project creation
"""

import os
import shutil
import json

import bpy
#from bpy.app.handlers import persistent
from blender2godot.addon_config import addon_config # type: ignore


'''
@persistent
def load_handler(dummy):
    #print("Load Handler:", bpy.data.filepath)
    bpy.ops.scene.update_current_template_operator()
'''

def get_project_templates(self, context):
    _templates = []
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "project_template"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "project_template")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _dirs_list = os.listdir(p_path)
            _index = 0
            for _dir_name in _dirs_list:
                _template_dirpath = os.path.join(p_path, _dir_name)
                if os.path.isdir(_template_dirpath):
                    _name = _dir_name.removesuffix("_template")
                    _new_template_tuple = (_dir_name, _name.capitalize(), _name.upper())
                    _templates.append(_new_template_tuple)
                    _index += 1
    return _templates

def get_templates_info(self, context, template_name):
    _template_info = None
    possible_paths = [os.path.join(bpy.utils.resource_path("USER"), "scripts", "addons", "blender2godot", "project_template"),
    os.path.join(bpy.utils.resource_path("LOCAL"), "scripts", "addons", "blender2godot", "project_template")]
    for p_path in possible_paths:
        if os.path.isdir(p_path):
            _dirs_list = os.listdir(p_path)
            _index = 0
            for _dir_name in _dirs_list:
                _template_dirpath = os.path.join(p_path, _dir_name)
                if os.path.isfile(_template_dirpath):
                    _filename = _dir_name.removesuffix("_template_requirements.json")
                    if (_filename == template_name):
                        #print("Found", _filename)
                        #print("Filepath", _template_dirpath)
                        with open(_template_dirpath, 'r') as outfile:
                            _template_info = json.load(outfile)
                            #print("from get", _template_info)
                            break
                    else:
                        pass
                        #print("not found;", _filename, template_name)
    return _template_info

def load_game_icon(self, context):
    if os.path.isfile(context.scene.game_icon):
        bpy.data.images.load(context.scene.game_icon, check_existing=True)
        if bpy.data.textures.find("gameIconImage") == -1:
            bpy.data.textures.new(name="gameIconImage", type="IMAGE")
        bpy.data.textures["gameIconImage"].image = bpy.data.images[os.path.basename(context.scene.game_icon)]
        bpy.data.textures["gameIconImage"].extension = 'CLIP'
        bpy.data.textures["gameIconImage"].use_fake_user = True

def update_scene_exportable(self, context):
    print("Updatting exportable", context.scene.scene_type)
    context.scene.scene_exportable = (context.scene.scene_type != "none")       

'''
def update_current_template(self, context):
    if context:
        context.scene.b2g_templates.clear()
        _current_template_info = get_templates_info(self, context, context.scene.project_template.removesuffix("_template"))
        context.scene.current_template_requirements.template_name = context.scene.project_template
        context.scene.current_template_requirements.template_requirements.clear()
        for _dict in _current_template_info:
            #print(_dict)
            _new_template_requirements = context.scene.current_template_requirements.template_requirements.add()
            _new_template_requirements.name = _dict["id"]
            for _key in _dict["value"]:
                _new_requirement = _new_template_requirements.requirements.add()
                _new_requirement.value = _key
        
        _scene_types_tuple = [("none", "None", "", "NONE", 0)]
        _tr = context.scene.current_template_requirements.template_requirements
        for _reqs in _tr:
            if _reqs.name == "scene_types":
                for _index,_value in enumerate(_reqs.requirements):
                    _scene_types_tuple.append((_value.value.lower(), _value.value.capitalize(), "", _value.value.upper(), _index+1))
            break
    else:
        _scene_types_tuple = [("none", "None", "", "NONE", 0)]
    
    bpy.types.Scene.scene_type = bpy.props.EnumProperty(
        items = _scene_types_tuple,
        name = "Scene Type",
        description = "Scene type",
        default = 1,
        update=update_scene_exportable)
'''

def update_game_folder(self, context):
    context.scene.game_folder = bpy.path.abspath("//")

'''
class TemplateKey(bpy.types.PropertyGroup):
    value : bpy.props.StringProperty(name="Requirement key") # type: ignore

class TemplateRequirements(bpy.types.PropertyGroup):
    name: bpy.props.StringProperty(name="Template requirement key", default="Unknown") # type: ignore
    requirements : bpy.props.CollectionProperty(type=TemplateKey, name="Template requirement string array") # type: ignore

class TemplateStruct(bpy.types.PropertyGroup):
    template_name : bpy.props.StringProperty(name="Template name") # type: ignore
    template_requirements : bpy.props.CollectionProperty(type=TemplateRequirements) # type: ignore
'''

class GodotProjectPropertiesPanel(bpy.types.Panel):
    """Godot Project Properties Panel"""
    bl_label = "Godot Project Properties"
    bl_idname = "GODOTPROJECTPROPERTIES_PT_layout"
    bl_space_type = 'NODE_EDITOR'
    bl_region_type = 'UI'
    bl_category = "Blender2Godot"
    bl_order = 1
    bl_options = {"DEFAULT_CLOSED"}

    @classmethod 
    def poll(self, context):
        return ((context.scene.name == context.scene.gamemanager_scene_name) and (bpy.data.is_saved))
    
    def draw_header(self, context):
        layout = self.layout
        layout.label(icon_value=addon_config.preview_collections[0]["godot_icon"].icon_id)        

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        
        if not bpy.data.is_saved:       
            return

        if context.scene.godot_exporting or context.scene.is_game_exporting:       
            layout.enabled = False
        else:
            layout.enabled = True

        row0 = layout.row()
        # Project properties box
        box1 = row0.box()
        box1.prop(scene, "game_name", icon="TEXT")
        if len(scene.game_name) == 0:
            box1.label(text="Give a name to your game!", icon="ERROR")
        #box1.prop(scene, "game_folder", icon="FILE_FOLDER")
        box2 = box1.box()
        box2.prop(scene, "game_icon", icon="IMAGE")
        if not scene.game_icon.endswith(".png"):
            box2.label(text="Icon must be a png image!", icon="CANCEL")
        else:
            if bpy.data.textures.find("gameIconImage") > -1:
                row1 = box2.row()
                row1.alignment = "CENTER"
                row1.template_preview(bpy.data.textures["gameIconImage"], preview_id="GameIconPreview")
        #box1.prop(scene, "project_template", icon="SHADERFX")
        #box1.prop(scene, "scene_environment", text="Default environment")

'''
class UpdateCurrentTemplateOperator(bpy.types.Operator):
    bl_idname = "scene.update_current_template_operator"
    bl_label = "UpdateCurrentTemplateOperator"

    def execute(self, context):
        update_current_template(self, context)
        return {'FINISHED'}
'''

def clear_properties():
    del bpy.types.Scene.game_name
    del bpy.types.Scene.game_folder
    del bpy.types.Scene.game_icon
    del bpy.types.Scene.project_folder
    del bpy.types.Scene.godot_project_filepath
    #del bpy.types.Scene.project_template
    #del bpy.types.Scene.game_icon_image

def init_properties():
    # Project props
    bpy.types.Scene.game_name = bpy.props.StringProperty(name="Name", default="NEW_GAME", update=update_game_folder)
    bpy.types.Scene.game_folder = bpy.props.StringProperty(name="Game Folder", subtype="DIR_PATH", default=" ")
    bpy.types.Scene.game_icon = bpy.props.StringProperty(name="Game Icon", subtype="FILE_PATH", default=" ", update=load_game_icon)
    bpy.types.Scene.project_folder = bpy.props.StringProperty(name="Project Folder", subtype="DIR_PATH", default=" ")
    bpy.types.Scene.godot_project_filepath = bpy.props.StringProperty(name="GPF", subtype="FILE_PATH", default=" ")

    '''
    bpy.types.Scene.project_template = bpy.props.EnumProperty(
                                                    items = get_project_templates,
                                                    name = "Project Template",
                                                    description = "Project type",
                                                    update=update_current_template,
                                                    default = 0)
    bpy.types.Scene.current_template_requirements = bpy.props.PointerProperty(type=TemplateStruct, name="Current Template Requirements")
    bpy.types.Scene.b2g_templates = bpy.props.CollectionProperty(type=TemplateStruct, name="Templates")
    '''
    #bpy.types.Scene.custom_godot = bpy.props.BoolProperty(name="Custom Godot", default=False)
    #bpy.types.Scene.godot_executable_downloaded_zip = bpy.props.StringProperty(name="Godot zip", subtype="FILE_PATH", default=".")
    #bpy.types.Scene.game_icon_image = bpy.props.PointerProperty(name="Game Icon Image", type=bpy.types.Image)

def register():
    #bpy.app.handlers.load_post.append(load_handler)
    #bpy.utils.register_class(UpdateCurrentTemplateOperator)
    #bpy.utils.register_class(TemplateKey)
    #bpy.utils.register_class(TemplateRequirements)
    #bpy.utils.register_class(TemplateStruct)
    init_properties()
    bpy.utils.register_class(GodotProjectPropertiesPanel)

def unregister():
    bpy.utils.unregister_class(GodotProjectPropertiesPanel)
    clear_properties()
    #bpy.utils.unregister_class(TemplateStruct)
    #bpy.utils.unregister_class(TemplateRequirements)
    #bpy.utils.unregister_class(TemplateKey)
    #bpy.utils.unregister_class(UpdateCurrentTemplateOperator)
    #bpy.app.handlers.load_post.remove(load_handler)


