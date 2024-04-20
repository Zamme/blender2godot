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
Blender To Godot

This is a simple exporter from blender to godot for testing purposes.

"""

import bpy

#from blender2godot import prefs

from blender2godot.addon_config import addon_config

from blender2godot.godot_project_properties import godot_project_properties

from blender2godot.display_properties import display_properties

from blender2godot.splash_properties import splash_properties

from blender2godot.b2g_tools import (
	advanced_tools,
	general_tools,
	)

from blender2godot.scene_properties import scene_properties

from blender2godot.player_properties import player_properties

from blender2godot.test_project import test_project

from blender2godot.game_export import game_export


bl_info = {
    "name": "Blender2Godot",
    "author": "Jaume Castells",
    "version": (0,1),
    "blender": (2, 82, 0),
    "location": "View 3D/Properties",
    "description": "Blender to godot easy exporter",
    "warning": "",
    "wiki_url": "https://zammedev.com",
    "tracker_url": "https://zammedev.com",
    "category": "Interface",
}   

def init_handlers():
    #bpy.app.handlers.depsgraph_update_post.append(update_player_objects)
    pass


def clear_handlers():
    #bpy.app.handlers.depsgraph_update_post.remove(update_player_objects)
    pass


def register():
    bpy.types.Scene.gamemanager_scene_name = bpy.props.StringProperty(name="Gamemanager scene default name", default="B2G_GameManager")
    addon_config.register()
    general_tools.register()
    godot_project_properties.register()
    display_properties.register()
    splash_properties.register()
    advanced_tools.register()
    scene_properties.register()
    player_properties.register()
    test_project.register()
    game_export.register()
    """
    bpy.utils.register_class(addon_config.CreateGameManagerOperator)
    bpy.utils.register_class(game_export.OpenGodotProjectFolderOperator)
    bpy.utils.register_class(game_export.OpenGodotBuildsFolderOperator)
    bpy.utils.register_class(game_export.MessageBoxOperator)
    bpy.utils.register_class(game_export.CompileSelectedVersionsOperator)
    bpy.utils.register_class(scene_properties.SetGodotProjectEnvironmentOperator)
    bpy.utils.register_class(general_tools.ExportProjectToGodotOperator)
    bpy.utils.register_class(game_export.BuildGameOperator)
    bpy.utils.register_class(godot_project_properties.DeleteProjectButtonOperator)
    bpy.utils.register_class(godot_project_properties.AreYouSureDeletingOperator)
    bpy.utils.register_class(godot_project_properties.DeleteProjectOperator)
    bpy.utils.register_class(advanced_tools.ExportGameOperator)
    bpy.utils.register_class(advanced_tools.OpenGodotProjectOperator)
    bpy.utils.register_class(test_project.TestGameOperator)
    bpy.utils.register_class(godot_project_properties.CreateGodotProjectOperator)
    bpy.utils.register_class(addon_config.Blender2GodotPanel)
    bpy.utils.register_class(godot_project_properties.GodotProjectPropertiesPanel)
    bpy.utils.register_class(splash_properties.SplashPropertiesPanel)
    bpy.utils.register_class(display_properties.DisplayPropertiesPanel)
    bpy.utils.register_class(scene_properties.ScenePropertiesPanel)
    bpy.utils.register_class(player_properties.PlayerPropertiesPanel)
    bpy.utils.register_class(advanced_tools.B2G_ToolsPanel)
    bpy.utils.register_class(test_project.TestGamePanel)
    bpy.utils.register_class(game_export.GameExportPanel)
    """
    init_handlers()
    print("Blender2Godot addon loaded.")


def unregister():
    clear_handlers()
    addon_config.unregister()
    general_tools.unregister()
    godot_project_properties.unregister()
    display_properties.unregister()
    splash_properties.unregister()
    advanced_tools.unregister()
    scene_properties.unregister()
    player_properties.unregister()
    test_project.unregister()
    game_export.unregister()
    """
    bpy.utils.unregister_class(player_properties.PlayerPropertiesPanel)
    bpy.utils.unregister_class(game_export.GameExportPanel)
    bpy.utils.unregister_class(advanced_tools.B2G_ToolsPanel)
    bpy.utils.unregister_class(scene_properties.ScenePropertiesPanel)
    bpy.utils.unregister_class(display_properties.DisplayPropertiesPanel)
    bpy.utils.unregister_class(splash_properties.SplashPropertiesPanel)
    bpy.utils.unregister_class(godot_project_properties.GodotProjectPropertiesPanel)
    bpy.utils.unregister_class(addon_config.Blender2GodotPanel)
    bpy.utils.unregister_class(godot_project_properties.CreateGodotProjectOperator)
    bpy.utils.unregister_class(test_project.TestGamePanel)
    bpy.utils.unregister_class(test_project.TestGameOperator)
    bpy.utils.unregister_class(advanced_tools.OpenGodotProjectOperator)
    bpy.utils.unregister_class(advanced_tools.ExportGameOperator)
    bpy.utils.unregister_class(godot_project_properties.DeleteProjectOperator)
    bpy.utils.unregister_class(godot_project_properties.AreYouSureDeletingOperator)
    bpy.utils.unregister_class(godot_project_properties.DeleteProjectButtonOperator)
    bpy.utils.unregister_class(game_export.BuildGameOperator)
    bpy.utils.unregister_class(general_tools.ExportProjectToGodotOperator)
    bpy.utils.unregister_class(scene_properties.SetGodotProjectEnvironmentOperator)
    bpy.utils.unregister_class(game_export.CompileSelectedVersionsOperator)
    bpy.utils.unregister_class(game_export.MessageBoxOperator)
    bpy.utils.unregister_class(game_export.OpenGodotProjectFolderOperator)
    bpy.utils.unregister_class(game_export.OpenGodotBuildsFolderOperator)
    bpy.utils.unregister_class(addon_config.CreateGameManagerOperator)
    print("Blender2Godot addon unloaded.")
    """

if __name__ == "__main__":
    register()