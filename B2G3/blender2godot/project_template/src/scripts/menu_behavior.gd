class_name MenuBehavior extends Spatial


var _json_info


# DEBUG
const B2G_HUD_FILEPATH = "res://b2g_tools/B2G_HUD.tscn"
var b2g_hud


func _ready():
#		ob.action_to_do = _menus_json[scene.name]["SpecialObjects"][ob.name]["ActionOnClick"]
	# DEBUG
	add_b2g_hud()

func get_json_info():
	var _menus_json = read_json_file(StageTemplate.MENUS_INFO_JSON_PATH)
	var _name_trimmed = name.trim_prefix("Menu_")
	if _menus_json.has(_name_trimmed):
		return _menus_json[_name_trimmed]

func get_special_object_info(_name : String):
	if not _json_info:
		_json_info = get_json_info()
	#print(_json_info)
	return _json_info["SpecialObjects"][_name]

func read_json_file(filepath):
	var file = File.new()
	if not file.file_exists(filepath):
		print("Missing classes.json file.")
	else:
		file.open(filepath, file.READ)
		var json = file.get_as_text()
		print("json ", filepath, " : ", json)
		var json_result = JSON.parse(json)
		file.close()
		return json_result.result

# DEBUG
func add_b2g_hud():
	b2g_hud = load(B2G_HUD_FILEPATH).instance()
	add_child(b2g_hud)

func show_message(_text):
	b2g_hud.show_message(_text)
