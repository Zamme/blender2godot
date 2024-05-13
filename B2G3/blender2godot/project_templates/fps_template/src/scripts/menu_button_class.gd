class_name Menu_Button extends MeshInstance


const STAGES_PATHDIR = "res://src/scenes/stages/"
const MENUS_PATHDIR = "res://src/scenes/menus/"

var action_to_do : String = "None"
var action_parameter = "None"

var _button_collider : StaticBody


func _ready():
	_button_collider = get_collider()
	add_on_click_event()
	setup_functionality()

func add_on_click_event():
	_button_collider.connect("input_event", self, "_on_click_event")

func do_click_action():
	var _msg : String = action_to_do + " " + action_parameter
	print(_msg)
	get_tree().current_scene.show_message(_msg)
	var _param : String
	match action_to_do:
		"load_stage":
			_param = STAGES_PATHDIR + action_parameter + ".tscn"
			get_tree().change_scene_to(load(_param))
		"menu_stage":
			_param = MENUS_PATHDIR + action_parameter + ".tscn"
			get_tree().change_scene_to(load(_param))
		"quit_game":
			get_tree().quit()

func get_collider():
	for _child in get_children():
		if _child is StaticBody:
			return _child

func setup_functionality():
	var _info = get_tree().current_scene.get_special_object_info(name)
	if _info.has("ActionOnClick"):
		action_to_do = _info["ActionOnClick"]
	if _info.has("ActionParameter"):
		action_parameter = _info["ActionParameter"]

func _on_click_event(_cam, _event, _pos, _norm, _s_idx):
	if _event is InputEventMouseButton:
		if _event.pressed:
			print("clicked")
			do_click_action()
		else:
			print("unclicked")
	#elif _event is InputEventMouseMotion:
		#print("hovering")
