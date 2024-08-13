class_name StageBehavior extends Spatial


const STAGE_SCENES_PREFIX = "Stage_"
const FREE_CAMERA_SCRIPT_FILEPATH = "res://b2g_tools/B2G_FreeCamera.gd"

var player_spawn
var player
var is_paused : bool

var free_camera : Camera

onready var scenario_scene = get_child(0)
onready var scenario_scene_animation_player = scenario_scene.find_node("AnimationPlayer")

export var optional_dict : Dictionary
export var node_info : Dictionary

var stage_objects_dict : Dictionary
var gm_ref
var _enter_triggers : Dictionary
var _exit_triggers : Dictionary


func _ready():
	print("Stage ", name, " loaded!")
	self.gm_ref = get_tree().current_scene
	self.setup_stage_objects()
	self.setup_player()
	self.setup_triggers()

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
			player.node_info = _player_node
			#player._actions_dict = _player_node["ActionsSettings"]
			#player._entity_properties = _player_node["EntityProperties"]
		add_child(player)
		player.set_stage_scene(self)
		player.translation = player_spawn.translation
		player.rotation = player_spawn.rotation
	else:
		get_tree().current_scene.show_message("Empty player")
		add_free_camera()

func get_player_spawn():
	return scenario_scene.find_node(self.optional_dict["PlayerSpawnObjectName"])

func play_entity_animation(_animation_name : String, _reproduction : String, _time : float):
	if self.scenario_scene_animation_player:
		if self.scenario_scene_animation_player.has_animation(_animation_name):
			match _reproduction:
				"play_forward":
					self.scenario_scene_animation_player.play(_animation_name, -1, _time, false)
				"play_backward":
					self.scenario_scene_animation_player.play_backwards(_animation_name)

func setup_player():
	player_spawn = get_player_spawn()
	if player_spawn:
		var player_node
		if node_info.has("Player"):
			player_node = self.gm_ref.get_tree_node(node_info["Player"], self.gm_ref.gm_dict)
		var _player_name : String = ""
		if player_node:
			_player_name = player_node["SceneName"]
		else:
			print("Player node not found")
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
#else:
#	print("No player spawn defined. Loading free camera...")
#	get_tree().current_scene.show_message("No player spawn defined")
#	add_free_camera()

func set_optional_dict(_dict : Dictionary):
	self.optional_dict = _dict

func setup_stage_objects():
	stage_objects_dict = optional_dict["Objects"]

func setup_triggers():
#	print(node_info["Outputs"])
	for _node_output_key in node_info["Outputs"].keys():
#		print(_node_output_key)
		var _node_key_parts : PoolStringArray = _node_output_key.rsplit("_", true, 1)
		match _node_key_parts[1]:
			"Enter":
				_enter_triggers[_node_key_parts[0]] = node_info["Outputs"][_node_output_key]
			"Exit":
				_exit_triggers[_node_key_parts[0]] = node_info["Outputs"][_node_output_key]

func stage_trigger_entered(_body_entered, _arg):
	var _msg : String
#	_msg = _body_entered.name + " entered " + _arg.name
	var _trigger_name : String = _arg.name.rsplit("_", true, 1)[0]
	if _enter_triggers.has(_trigger_name):
		var node_to_call = _enter_triggers[_trigger_name]
		_msg = "Trigger calls " + node_to_call
		print(_msg)
		self.gm_ref.show_message(_msg)
		self.gm_ref.execute_node(node_to_call)

func stage_trigger_exited(_body_exited, _arg):
	var _msg : String
#	_msg = _body_exited.name + " exited " + _arg.name
	var _trigger_name : String = _arg.name.rsplit("_", true, 1)[0]
	if _exit_triggers.has(_trigger_name):
		var node_to_call = _exit_triggers[_trigger_name]
		_msg = "Trigger calls " + node_to_call
		print(_msg)
		self.gm_ref.show_message(_msg)
		self.gm_ref.execute_node(node_to_call)
