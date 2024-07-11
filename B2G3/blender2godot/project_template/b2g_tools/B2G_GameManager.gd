class_name GameManager extends Node


const STAGES_DIRPATH = "res://src/scenes/stages/"
const MENUS3D_DIRPATH = "res://src/scenes/menus3d/"
const MENUS2D_DIRPATH = "res://src/scenes/menus2d/"
const PLAYERS_DIRPATH = "res://src/scenes/players/"
const HUDS_SCENES_DIRPATH = "res://src/scenes/huds/"
const MENU2D_BUTTON_BEHAVIOR_PATH = "res://b2g_tools/B2G_Menu2dButton.gd"
const SELECTED_OBJECT_OVERLAY_COLOR = Color(1.0, 1.0, 1.0, 0.75)

enum GameState {None, Starting, Loading, Menu, Playing, Pause, Finished}

export var gm_dict : Dictionary

export var debug_hud_enabled : bool

#var current_stage_node_loaded

var b2g_current_scene
var current_state = GameState.None

# DEBUG
const B2G_HUD_FILEPATH = "res://b2g_tools/B2G_HUD.tscn"
var b2g_hud


func _ready():
	print("GameManager Loaded")
	# DEBUG
	if debug_hud_enabled:
		add_b2g_hud()
	# END DEBUG
	self.start_gm()

func get_node_next_node(_tree, _node_name):
	var _node
	var _next_node
	_node = self.get_tree_node(_tree, _node_name)
	if _node.has("NextNode"):
		_next_node = self.get_tree_node(_tree, _node["NextNode"])
	return _next_node

func get_tree_node(_tree, _node_name):
	var _node
	for _tree_node_key in _tree["Nodes"].keys():
		if _tree_node_key == _node_name:
			_node = _tree["Nodes"][_tree_node_key]
	return _node

func fix_startup_scene_filepath(_filepath, _type):
	var _prefix_dict : Dictionary = {"B2G_Stage_Scene_Node" : ["Stage_", STAGES_DIRPATH],
									"B2G_2dMenu_Scene_Node" : ["Menu2d_", MENUS2D_DIRPATH],
									"B2G_3dMenu_Scene_Node" : ["Menu3d_", MENUS3D_DIRPATH]}
	var _filepath_fixed : String = _filepath
	_filepath_fixed =  _prefix_dict[_type][1] + _prefix_dict[_type][0] + _filepath + ".tscn"
	return _filepath_fixed

static func get_all_children(in_node,arr:=[]):
	arr.push_back(in_node)
	for child in in_node.get_children():
		arr = get_all_children(child,arr)
	return arr

func load_menu2d():
	pass

func load_menu3d(_menu_filepath):
	load_scene(_menu_filepath)

func load_scene(_new_scene_path : String = "", _unload_current : bool = false, _optional_dict : Dictionary = {}):
	if _unload_current:
		b2g_current_scene.queue_free()
	print("Loading menu", _new_scene_path)
	var _file : File = File.new()
	if _file.file_exists(_new_scene_path):
		b2g_current_scene = load(_new_scene_path).instance()
		if not _optional_dict.empty():
			b2g_current_scene.set_optional_dict(_optional_dict)
	else:
		b2g_current_scene = Spatial.new()
	add_child(b2g_current_scene)

func load_stage(_stage_filepath, _stage_node):
	load_scene(_stage_filepath, false, _stage_node)

func quit_game():
	push_warning("Game Finished")

func set_state(_state):
	current_state = _state
	update_state()

func start_gm():
	var start_node_next_node = self.get_node_next_node(self.gm_dict, "Start")
	var startup_scene_filepath : String = ""
	var startup_scene_type : String = ""
	if start_node_next_node.has("SceneName"):
		startup_scene_filepath = start_node_next_node["SceneName"]
		startup_scene_type = start_node_next_node["Type"]
	if startup_scene_filepath == "":
		print("No startup scene.")
		show_message("No startup scene")
	else:
		startup_scene_filepath = self.fix_startup_scene_filepath(startup_scene_filepath, start_node_next_node["Type"])
		match startup_scene_type:
			"B2G_Stage_Scene_Node":
				load_stage(startup_scene_filepath, start_node_next_node)
			"B2G_3dMenu_Scene_Node":
				load_menu3d(startup_scene_filepath)
		set_state(GameState.Starting)

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

	# DEBUG
func add_b2g_hud():
	b2g_hud = load(B2G_HUD_FILEPATH).instance()
	add_child(b2g_hud)

func show_message(_text):
	if b2g_hud:
		b2g_hud.show_message(_text)
