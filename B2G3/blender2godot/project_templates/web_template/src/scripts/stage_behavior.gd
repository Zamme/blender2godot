class_name StageBehavior extends Spatial


const STAGES_INFO_JSON_PATH = "res://stages_info/stages_info.json"
const STAGE_SCENES_PREFIX = "Stage_"

var stages_json
var player_spawn
var player
onready var scenario_scene = get_child(0)


func _ready():
	print("Stage ", name, " loaded!")
	stages_json = read_json_file(STAGES_INFO_JSON_PATH)
	player_spawn = get_player_spawn()
	add_player()

func add_player():
	player = load("res://src/scenes/players/Player1Entity.tscn").instance()
	add_child(player)

func get_player_spawn():
	var _node_name_to_found
	var _stage_scenario_name = name.lstrip(STAGE_SCENES_PREFIX)
	for _stage_key in stages_json.keys():
		var _stage = stages_json[_stage_key]
		if _stage["SceneName"] == _stage_scenario_name:
			_node_name_to_found = _stage["PlayerSpawnObjectName"]
			return scenario_scene.find_node(_node_name_to_found)

func read_json_file(filepath):
	var file = File.new()
	if not file.file_exists(filepath):
		print("Missing classes.json file.")
	else:
		file.open(filepath, file.READ)
		var json = file.get_as_text()
		var json_result = JSON.parse(json)
		file.close()
		return json_result.result
