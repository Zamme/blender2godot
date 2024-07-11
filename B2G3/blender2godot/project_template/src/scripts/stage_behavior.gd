class_name StageBehavior extends Spatial


const STAGE_SCENES_PREFIX = "Stage_"
const FREE_CAMERA_SCRIPT_FILEPATH = "res://b2g_tools/B2G_FreeCamera.gd"

export var player_spawn_name : String = ""

var player_spawn
var player
var is_paused : bool

var free_camera : Camera

onready var scenario_scene = get_child(0)

var optional_dict : Dictionary
var gm_ref


func _ready():
	print("Stage ", name, " loaded!")
	self.gm_ref = get_tree().current_scene
	if player_spawn_name != "":
		player_spawn = get_player_spawn()
		if player_spawn:
			var player_node
			if optional_dict.has("Player"):
				player_node = self.gm_ref.get_tree_node(self.gm_ref.gm_dict, optional_dict["Player"])
			var _player_name : String = ""
			if player_node:
				_player_name = player_node["SceneName"]
			if  _player_name == "":
				print("No player found. Loading free camera...")
				get_tree().current_scene.show_message("No player detected")
				add_free_camera()
			else:
				add_player(_player_name, player_node)
		else:
			print("No player spawn found. Loading free camera...")
			get_tree().current_scene.show_message("No player spawn found")
			add_free_camera()
	else:
		print("No player spawn defined. Loading free camera...")
		get_tree().current_scene.show_message("No player spawn defined")
		add_free_camera()

func add_free_camera():
	free_camera = Camera.new()
	free_camera.script = load(FREE_CAMERA_SCRIPT_FILEPATH)
	add_child(free_camera)

func add_player(_player_name : String, _player_node : Dictionary = {}):
	var _player_entity_path : String = get_tree().current_scene.PLAYERS_DIRPATH + _player_name + "Entity.tscn"
	var _fileobject : File = File.new()
	if _fileobject.file_exists(_player_entity_path):
		player = load(_player_entity_path).instance()
		if not _player_node.empty():
			player.set_optional_dict(_player_node)
		add_child(player)
		player.set_stage_scene(self)
	else:
		get_tree().current_scene.show_message("Empty player")
		add_free_camera()

func get_player_spawn():
	return scenario_scene.find_node(player_spawn_name)

func set_optional_dict(_dict : Dictionary):
	self.optional_dict = _dict
