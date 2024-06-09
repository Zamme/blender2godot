class_name Menu3dBehavior extends Spatial


var _json_info


# DEBUG
const B2G_HUD_FILEPATH = "res://b2g_tools/B2G_HUD.tscn"
var b2g_hud


func _ready():
	# DEBUG
#	add_b2g_hud()
	pass

# DEBUG
func add_b2g_hud():
	b2g_hud = load(B2G_HUD_FILEPATH).instance()
	add_child(b2g_hud)

func show_message(_text):
	b2g_hud.show_message(_text)
