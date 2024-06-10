class_name Menu2dButton extends Area2D


export var action_to_do : String = "None"
export var action_parameter = "None"

var menu_scene
var marker_object : Polygon2D


func _ready():
	pause_mode = Node.PAUSE_MODE_PROCESS
	set_menu_scene(get_parent())
	marker_object = get_marker_object()

func do_click_action():
	var _msg : String = action_to_do + " " + action_parameter
	print(_msg)
#	get_parent().get_parent().show_message(_msg)
	var _param : String
	var _dir : Directory = Directory.new()
	match action_to_do:
		"close_menu":
			menu_scene.create_exit_timer()
		"load_stage":
			_param = StageTemplate.STAGES_PATH + StageTemplate.STAGE_SCENES_PREFIX + action_parameter + ".tscn"
			if _dir.file_exists(_param):
				get_tree().current_scene.load_scene(_param, true)
		"load_3dmenu":
			_param = StageTemplate.MENUS3D_PATH + StageTemplate.MENU3D_SCENES_PREFIX + action_parameter + ".tscn"
			if _dir.file_exists(_param):
				get_tree().current_scene.load_scene(_param, true)
		"load_2dmenu":
			_param = StageTemplate.MENUS2D_PATH + StageTemplate.MENUS2D_SCENES_PREFIX + action_parameter + ".tscn"
			if _dir.file_exists(_param):
				get_tree().current_scene.load_scene(_param, true)
		"quit_game":
			get_tree().quit()

func get_marker_object():
	var _marker
	for _child in get_children():
		if _child is Polygon2D:
			_marker = _child
			break
	return _marker

func select_object(_selected : bool):
	if _selected:
		marker_object.show()
	else:
		marker_object.hide()

func set_menu_scene(_scene):
	menu_scene = _scene

func _on_Button_Area2D_input_event(viewport, event, shape_idx):
	if (event is InputEventMouseButton && event.pressed):
		do_click_action()
