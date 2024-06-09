class_name GameManager extends Node


export var startup_scene_filepath : String = ""

var current_scene


func _ready():
	print("GameManager Loaded")
	if startup_scene_filepath == "":
		print("No startup scene.")
	else:
		current_scene = load(startup_scene_filepath).instance()
		add_child(current_scene)
