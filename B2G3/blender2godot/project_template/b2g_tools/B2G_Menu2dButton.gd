class_name Menu2dButton extends Area2D


var menu_scene
var marker_object : Polygon2D


func _ready():
	pause_mode = Node.PAUSE_MODE_PROCESS
	set_menu_scene(get_parent())
	marker_object = get_marker_object()

func do_click_action():
		if name.find("Quit") > -1:
			get_tree().quit()
		else:
			menu_scene.create_exit_timer()

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
		print("object ", name, " clicked")
		if name.find("Quit") > -1:
			get_tree().quit()
		else:
			menu_scene.create_exit_timer()
