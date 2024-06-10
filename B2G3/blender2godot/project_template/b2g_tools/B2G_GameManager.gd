class_name GameManager extends Node


const PLAYERS_DIRPATH = "res://src/scenes/players/"
const HUDS_SCENES_DIRPATH = "res://src/scenes/huds/"

const SELECTED_OBJECT_OVERLAY_COLOR = Color(1.0, 1.0, 1.0, 0.75)

enum GameState {None, Starting, Loading, Menu, Playing, Pause, Finished}

export var startup_scene_filepath : String = ""
export var current_player_name : String = ""

var b2g_current_scene
var current_state = GameState.None


func _ready():
	print("GameManager Loaded")
	if startup_scene_filepath == "":
		print("No startup scene.")
	else:
		load_scene(startup_scene_filepath)
		set_state(GameState.Starting)

static func get_all_children(in_node,arr:=[]):
	arr.push_back(in_node)
	for child in in_node.get_children():
		arr = get_all_children(child,arr)
	return arr

func load_menu2d():
	pass

func load_menu3d():
	pass

func load_scene(_new_scene_path : String = "", _unload_current : bool = false):
	if _unload_current:
		b2g_current_scene.queue_free()
	b2g_current_scene = load(_new_scene_path).instance()
	add_child(b2g_current_scene)

func load_stage():
	pass

func set_state(_state):
	current_state = _state
	update_state()

func update_state():
	match current_state:
		GameState.None:
			pass
		GameState.Starting:
			pass
		GameState.Loading:
			pass
		GameState.Menu:
			pass
		GameState.Playing:
			pass
		GameState.Finished:
			pass
