class_name GameManager extends Node


const SRC_PATH = "res://src/"
const SCENES_PATH = SRC_PATH + "scenes/"
const STAGES_DIRPATH = SCENES_PATH + "stages/"
const MENUS3D_DIRPATH = SCENES_PATH + "menus3d/"
const MENUS2D_DIRPATH = SCENES_PATH + "menus2d/"
const PLAYERS_DIRPATH = SCENES_PATH + "players/"
const HUDS_SCENES_DIRPATH = SCENES_PATH + "huds/"
const MENU2D_BUTTON_BEHAVIOR_PATH = "res://b2g_tools/B2G_Menu2dButton.gd"
const SELECTED_OBJECT_OVERLAY_COLOR = Color(1.0, 1.0, 1.0, 0.75)
const STAGE_SCENES_PREFIX = "Stage_"
const MENU3D_SCENES_PREFIX = "Menu3d_"
const MENUS2D_SCENES_PREFIX = "Menu2d_"
const SCENE_EXTENSION = ".tscn"
const _prefix_dict : Dictionary = {"B2G_Stage_Scene_Node" : ["Stage_", STAGES_DIRPATH],
								"B2G_2dMenu_Scene_Node" : ["Menu2d_", MENUS2D_DIRPATH],
								"B2G_3dMenu_Scene_Node" : ["Menu3d_", MENUS3D_DIRPATH]}

export var gm_dict : Dictionary

export var debug_hud_enabled : bool

#var current_stage_node_loaded

var b2g_current_scene
enum GameState {None, Starting, Loading, Menu, Playing, Pause, Finished}
var current_state = GameState.None
var current_node

# DEBUG
const B2G_HUD_FILEPATH = "res://b2g_tools/B2G_HUD.tscn"
var b2g_hud


func _ready():
	print("GameManager Loaded")
	# DEBUG
	if debug_hud_enabled:
		add_b2g_hud()
	# END DEBUG
	self.resume_gm()

func execute_command(_command : String, _parameter : String):
	var _param : String
	match _command:
		"load_stage":
			if _parameter != "":
				self.current_node = self.get_tree_node(_parameter, self.gm_dict)
				if self.current_node:
					var _scene_name = self.current_node["SceneName"]
					_param = self.STAGES_DIRPATH + self.STAGE_SCENES_PREFIX + _scene_name + self.SCENE_EXTENSION
					print("Current node:", self.current_node)
#					print("action parameter:", _parameter)
					self.load_stage(_param)
		"load_3dmenu":
			if _parameter != "":
				_param = self.MENUS3D_DIRPATH + _parameter + self.SCENE_EXTENSION
				self.load_menu3d(_param)
		"load_2dmenu":
			if _parameter != "":
				_param = self.MENUS2D_DIRPATH + _parameter + self.SCENE_EXTENSION
				self.load_menu2d(_param)
		"quit_game":
			self.quit_game()

func get_node_next_node(_tree, _node_name):
	var _node
	var _next_node
	_node = self.get_tree_node(_node_name, _tree)
	if _node.has("NextNode"):
		_next_node = self.get_tree_node(_node["NextNode"], _tree)
	return _next_node

func get_tree_node(_node_name, _tree):
	var _node
	for _tree_node_key in _tree["Nodes"].keys():
		if _tree_node_key == _node_name:
			_node = _tree["Nodes"][_tree_node_key]
	return _node

func get_scene_filepath(_filepath, _type):
	var _filepath_fixed : String = _filepath
	_filepath_fixed =  _prefix_dict[_type][1] + _prefix_dict[_type][0] + _filepath + SCENE_EXTENSION
	return _filepath_fixed

static func get_all_children(in_node,arr:=[]):
	arr.push_back(in_node)
	for child in in_node.get_children():
		arr = get_all_children(child,arr)
	return arr

func load_menu2d(_menu_filepath):
	load_scene(_menu_filepath, true, self.current_node)

func load_menu3d(_menu_filepath):
	load_scene(_menu_filepath, true, self.current_node)

func load_scene(_new_scene_path : String = "", _unload_current : bool = false, _optional_dict : Dictionary = {}):
	if _unload_current:
		if b2g_current_scene:
			b2g_current_scene.queue_free()
	print("Loading ", _new_scene_path)
	var _file : File = File.new()
	if _file.file_exists(_new_scene_path):
		b2g_current_scene = load(_new_scene_path).instance()
		if not _optional_dict.empty():
			b2g_current_scene.set_optional_dict(_optional_dict)
	else:
		b2g_current_scene = Spatial.new()
		print("Scene filepath not found")
	add_child(b2g_current_scene)

func load_stage(_stage_filepath):
	load_scene(_stage_filepath, true, self.current_node)

func quit_game():
	push_warning("Game Finished")
	get_tree().quit()

func resume_gm():
	if not self.current_node:
		self.current_node = self.get_node_next_node(self.gm_dict, "Start")
	
	var _scene_filepath : String = ""
	var _scene_type : String = ""
	if current_node.has("SceneName"):
		_scene_filepath = current_node["SceneName"]
		_scene_type = current_node["Type"]
	if _scene_filepath == "":
		print("No scene to load.")
		show_message("No scene to load")
	else:
		_scene_filepath = self.get_scene_filepath(_scene_filepath, current_node["Type"])
		match _scene_type:
			"B2G_Stage_Scene_Node":
				load_stage(_scene_filepath)
			"B2G_3dMenu_Scene_Node":
				load_menu3d(_scene_filepath)
			"B2G_2dMenu_Scene_Node":
				load_menu2d(_scene_filepath)
		set_state(GameState.Starting)


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

	# DEBUG
func add_b2g_hud():
	b2g_hud = load(B2G_HUD_FILEPATH).instance()
	add_child(b2g_hud)

func show_message(_text):
	if b2g_hud:
		b2g_hud.show_message(_text)
