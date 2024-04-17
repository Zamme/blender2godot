# Blender2Godot (Blender3D addon) #

For Blender3D artists and game developers.

A free tool (GPL) developed for a quick scenario testing and virtual tour deploying.

Blender2Godot is a Blender 3D addon that exports a Blender 3D scene to a Godot Engine project.

This addon is in alpha state. It has a lot of bugs and it works as it is currently. Sorry ;-)

See known issues below.

## Current features (v0.1) ##

- Works in all platforms (Linux, MacOS, Windows).

- Scenario colliders setup.

- Lighting setup available. Only "Point" lights allowed for the moment.

- Sky setup. Basic for the moment.

- Gravity setup. (for player, not for the objects)

- First Person navigation.

- Multiplatform executable deploying (Linux, MacOS, Windows, Web).

- From Blender 3.x and 4.x, to Godot 3.x. (working on 4.x)

## Installing ##
First of all, if Godot is not installed in your system, download it at:
https://godotengine.org/download
And install it (if you have to). Remember the installation path, you will need it.

If you want to export game binaries to some platform, install the Godot export templates (read how at https://www.zammedev.com/home/wip_projects/blender2godot).

Then, you have to download the Blender2Godot addon at:

https://gitlab.com/Zamme/blender2godot

Finally, follow the tutorial at https://www.zammedev.com/home/wip_projects/blender2godot

## Known issues ##
- Blend file has to be saved before exporting.

- Game update not allowed. The hole project has to be reimported every time.

- Icon required.

- Camera required. (Just the first camera will be exported as player)

## Roadmap (v1.0) ##
- Fix known issues.

- Game project update, without overwriting.

- Android deployment.

- Smart collider creation.

- Blender shading nodes translations.

- Improve lighting.

- Improve materials.

- Better UI ;-)

- More....

