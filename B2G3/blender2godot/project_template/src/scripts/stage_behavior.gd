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

var _hud_dict : Dictionary
export var hud_scene_name : String
var _hud


func _ready():
	print("Stage ", name, " loaded!")
	self.gm_ref = get_tree().current_scene
	self.setup_stage_objects()
	self.setup_player()
	self.add_hud()
	self.setup_triggers()

func add_free_camera():
	free_camera = Camera.new()
	free_camera.script = load(FREE_CAMERA_SCRIPT_FILEPATH)
	add_child(free_camera)

func add_hud():
	var hud_node_name = self.node_info["NodeInputs"]["HUD"]["SourceNodeName"]
	self._hud_dict = self.get_node_dict(hud_node_name)
	if _hud_dict.empty():
		return
	if _hud_dict.has("NodeProperties"):
		var _hud_node_properties = _hud_dict["NodeProperties"]
		if _hud_node_properties.has("source_scene_name"):
			hud_scene_name = _hud_node_properties["source_scene_name"]
	if hud_scene_name != "":
		print("Adding HUD:", hud_scene_name)
		var _hud_scene_path : String = get_tree().current_scene.HUDS_SCENES_DIRPATH + "Hud_" + hud_scene_name + ".tscn"
		_hud = load(_hud_scene_path).instance()
		_hud.node_info = _hud_dict
		_hud.hud_settings = _hud_dict["NodeProperties"]
		_hud.hud_fields = _hud_dict["NodeInputs"]
		add_child(_hud)

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

func change_player_property(_property_name, _property_value):
	if "_entity_properties" in player:
		if player._entity_properties.has(_property_name):
			player._entity_properties[_property_name] = _property_value
		else:
			print("Property not found")
	else:
		print("Properties not found")

func change_player_entity_property(_property_entity, _property_name, _operation, _property_value):
	player.change_entity_property(_property_entity, _property_name, _operation, _property_value)

func change_stage_entity_property(_property_entity, _property_name, _property_value):
	var _entity = player.find_node(_property_entity)
	if _entity:
		if "_entity_properties" in _entity:
			if _entity._entity_properties.has(_property_name):
				_entity._entity_properties[_property_name] = _property_value
			else:
				print("Property not found")
		else:
			print("Properties not found")
	else:
		print("Entity not found")

func get_node_dict(_node_name):
	var _return_dict : Dictionary = Dictionary()
	for _key in self.gm_ref.gm_dict["Nodes"].keys():
		if _key == _node_name:
			_return_dict = self.gm_ref.gm_dict["Nodes"][_key]
			break
	return _return_dict

func get_player_spawn():
	var _spawn_return = null
	var _spawn_object_name = ""
	if self.node_info["NodeProperties"].has("player_spawn_object_name"):
		_spawn_object_name = self.node_info["NodeProperties"]["player_spawn_object_name"]
		_spawn_return = scenario_scene.find_node(_spawn_object_name)
	return _spawn_return

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
		if self.node_info.has("NodeInputs"):
			var _node_inputs = self.node_info["NodeInputs"]
			if _node_inputs.has("Player"):
				var _node_input_player = _node_inputs["Player"]
				if _node_input_player.has("SourceNodeName"):
					var _player_node_name = _node_input_player["SourceNodeName"]
					player_node = self.gm_ref.get_tree_node(_player_node_name, self.gm_ref.gm_dict)
		else:
			print("Node info has no Player")
		var _player_name : String = ""
		if player_node:
			_player_name = player_node["NodeProperties"]["source_scene_name"]
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
	var _node_outputs : Dictionary = self.node_info["NodeOutputs"]
	for _node_output_key in _node_outputs.keys():
		if _node_output_key == "Stage_REF":
			var _links_keys = _node_outputs[_node_output_key].keys()
			for _link_key in _links_keys:
				var _link = _node_outputs[_node_output_key][_link_key]
				var _dest_node = self.gm_ref.get_tree_node(_link["DestNodeName"], self.gm_ref.gm_dict)
				if _dest_node["Type"] == "B2G_Trigger_Action_Node":
#					print("Setting ", _dest_node["NodeProperties"]["trigger_name"], " of ", _dest_node["Name"], " node")
					var _trigger_outputs = _dest_node["NodeOutputs"]
					var _trigger_outputs_keys = _dest_node["NodeOutputs"].keys()
					for _trigger_outputs_key in _trigger_outputs_keys:
						match _trigger_outputs_key:
							"OnEnter":
								var _trigger_node_name = _dest_node["NodeOutputs"]["OnEnter"]["0"]["DestNodeName"]
								self._enter_triggers[_dest_node["NodeProperties"]["trigger_name"]] = self.gm_ref.get_tree_node(_trigger_node_name, self.gm_ref.gm_dict)
#		print(_enter_triggers)
#	for _node_output_key in node_info["Outputs"].keys():
##		print(_node_output_key)
#		var _node_key_parts : PoolStringArray = _node_output_key.rsplit("_", true, 1)
#		match _node_key_parts[1]:
#			"Enter":
#				_enter_triggers[_node_key_parts[0]] = node_info["Outputs"][_node_output_key]
#			"Exit":
#				_exit_triggers[_node_key_parts[0]] = node_info["Outputs"][_node_output_key]
	
func stage_trigger_entered(_arg):
	var _msg : String
	var _trigger_name : String = _arg.name.rsplit("_", true, 1)[0]
	if _enter_triggers.has(_trigger_name):
		var node_to_call = _enter_triggers[_trigger_name]
		_msg = "Trigger calls " + node_to_call["Name"]
		print(_msg)
		self.gm_ref.show_message(_msg)
		self.gm_ref.execute_node(node_to_call)

func stage_trigger_exited(_arg):
	var _msg : String
	var _trigger_name : String = _arg.name.rsplit("_", true, 1)[0]
	if _exit_triggers.has(_trigger_name):
		var node_to_call = _exit_triggers[_trigger_name]
		_msg = "Trigger calls " + node_to_call["Name"]
		print(_msg)
		self.gm_ref.show_message(_msg)
		self.gm_ref.execute_node(node_to_call)
