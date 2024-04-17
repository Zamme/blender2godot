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


import bpy


class Blender2GodotPreferences(bpy.types.AddonPreferences):
    bl_idname = "blender2godot"
    godot_executable_path: bpy.props.StringProperty(
        name="Godot Executable Path",
        description="Set the current Godot executable path on your system",
        default="/usr/local/games/godot-engine",
    )

    def draw(self, context):
        layout = self.layout

        layout.label(
            text="Here you can set the system properties")

        split = layout.split(factor=0.25)

        col = split.column()
        sub = col.column(align=True)
        sub.prop(self, "godot_executable_path")
        

def register():
    bpy.utils.register_class(Blender2GodotPreferences)


def unregister():
    bpy.utils.unregister_class(Blender2GodotPreferences)
