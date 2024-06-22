class_name Menu2dButton_Behavior extends Area2D


# TODO: HERE???
const SRC_PATH = "res://src/"
const SCENES_PATH = SRC_PATH + "scenes/"
const STAGES_PATH = SCENES_PATH + "stages/"
const STAGE_SCENES_PREFIX = "Stage_"
const MENUS3D_PATH = SCENES_PATH + "menus3d/"
const MENU3D_SCENES_PREFIX = "Menu3d_"
const MENUS2D_PATH = SCENES_PATH + "menus2d/"
const MENUS2D_SCENES_PREFIX = "Menu2d_"
# END HERE

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
			_param = STAGES_PATH + STAGE_SCENES_PREFIX + action_parameter + ".tscn"
			if _dir.file_exists(_param):
				get_tree().current_scene.load_scene(_param, true)
		"load_3dmenu":
			_param = MENUS3D_PATH + MENU3D_SCENES_PREFIX + action_parameter + ".tscn"
			if _dir.file_exists(_param):
				get_tree().current_scene.load_scene(_param, true)
		"load_2dmenu":
			_param = MENUS2D_PATH + MENUS2D_SCENES_PREFIX + action_parameter + ".tscn"
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
		get_tree().set_input_as_handled()
		yield(get_tree(),"idle_frame")
		do_click_action()
