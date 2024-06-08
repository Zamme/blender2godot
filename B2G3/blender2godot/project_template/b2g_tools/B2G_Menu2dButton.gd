extends Area2D


var menu_scene


func _ready():
	pause_mode = Node.PAUSE_MODE_PROCESS
	set_menu_scene(get_parent())

func set_menu_scene(_scene):
	menu_scene = _scene

func _on_Button_Area2D_input_event(viewport, event, shape_idx):
	if (event is InputEventMouseButton && event.pressed):
		print("object ", name, " clicked")
		if name.find("Quit") > -1:
			get_tree().quit()
		else:
			menu_scene.create_exit_timer()
