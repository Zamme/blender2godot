class_name StageBehavior extends Spatial


const STAGE_SCENES_PREFIX = "Stage_"


export var player_spawn_name : String = ""

var player_spawn
var player
var is_paused : bool

onready var scenario_scene = get_child(0)

# DEBUG
const B2G_HUD_FILEPATH = "res://b2g_tools/B2G_HUD.tscn"
var b2g_hud


func _ready():
	print("Stage ", name, " loaded!")
	player_spawn = get_player_spawn()
	add_player(get_tree().current_scene.current_player_name)
	player.set_stage_scene(self)
	# DEBUG
#	add_b2g_hud()

func add_player(_player_name : String):
	var _player_entity_path : String = get_tree().current_scene.PLAYERS_DIRPATH + _player_name + "Entity.tscn"
	player = load(_player_entity_path).instance()
	add_child(player)

func get_player_spawn():
	return scenario_scene.find_node(player_spawn_name)


	# DEBUG
func add_b2g_hud():
	b2g_hud = load(B2G_HUD_FILEPATH).instance()
	add_child(b2g_hud)

func show_message(_text):
	b2g_hud.show_message(_text)

