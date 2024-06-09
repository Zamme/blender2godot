class_name Menu3d_Button extends MeshInstance


export var action_to_do : String = "None"
export var action_parameter = "None"

var _button_collider : StaticBody


func _ready():
	_button_collider = get_collider()
	add_on_click_event()

func add_on_click_event():
	_button_collider.connect("input_event", self, "_on_click_event")

func do_click_action():
	var _msg : String = action_to_do + " " + action_parameter
	print(_msg)
#	get_parent().get_parent().show_message(_msg)
	var _param : String
	match action_to_do:
		"load_stage":
			_param = StageTemplate.STAGES_PATH + action_parameter + ".tscn"
			get_tree().current_scene.load_scene(_param, true)
		"menu_stage":
			_param = StageTemplate.MENUS3D_PATH + action_parameter + ".tscn"
			get_tree().current_scene.load_scene(_param, true)
		"quit_game":
			get_tree().quit()

func get_collider():
	for _child in get_children():
		if _child is StaticBody:
			return _child

func _on_click_event(_cam, _event, _pos, _norm, _s_idx):
	if _event is InputEventMouseButton:
		if _event.pressed:
			print("clicked")
			do_click_action()
		else:
			print("unclicked")
	#elif _event is InputEventMouseMotion:
		#print("hovering")
