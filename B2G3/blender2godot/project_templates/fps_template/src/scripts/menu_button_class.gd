class_name Menu_Button extends MeshInstance


var _button_collider : StaticBody


func _ready():
	_button_collider = get_collider()
	add_on_click_event()

func add_on_click_event():
	_button_collider.connect("input_event", self, "_on_click_event")

func do_click_action():
	print("Action!")
	get_tree().current_scene.show_message("Action!")

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
