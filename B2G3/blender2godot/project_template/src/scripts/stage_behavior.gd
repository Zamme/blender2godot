class_name StageBehavior extends Spatial


const STAGE_SCENES_PREFIX = "Stage_"
const PLAYERS_DIRPATH = "res://src/scenes/players/"

var player_spawn
var player

onready var scenario_scene = get_child(0)

# DEBUG
const B2G_HUD_FILEPATH = "res://b2g_tools/B2G_HUD.tscn"
var b2g_hud


func _ready():
	print("Stage ", name, " loaded!")
	var stages_json = read_json_file(StageTemplate.STAGES_INFO_JSON_PATH)
	var player_json = read_json_file(StageTemplate.PLAYER_INFO_JSON_PATH)
	player_spawn = get_player_spawn(stages_json)
	var _player_name : String = player_json["PlayerSceneName"]
	add_player(_player_name)
	# DEBUG
	add_b2g_hud()

func add_player(_player_name : String):
	var _player_entity_path : String = PLAYERS_DIRPATH + _player_name + "Entity.tscn"
	player = load(_player_entity_path).instance()
	add_child(player)

func get_player_spawn(_stages_json):
	var _node_name_to_found
	var _stage_scenario_name = name.lstrip(STAGE_SCENES_PREFIX)
	for _stage_key in _stages_json.keys():
		var _stage = _stages_json[_stage_key]
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



	# DEBUG
func add_b2g_hud():
	b2g_hud = load(B2G_HUD_FILEPATH).instance()
	add_child(b2g_hud)

func show_message(_text):
	b2g_hud.show_message(_text)

