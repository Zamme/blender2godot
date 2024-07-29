class_name Menu2DBehavior extends Control


const PAUSE_TIME = 0.15

var _timer : Timer
var _areas
var _player_scene

var selectable_objects = []
var current_selected_object_index = -1
export var optional_dict : Dictionary
export var node_name : String
export var node_info : Dictionary

var special_objects : Dictionary


func _ready():
	pause_mode = Node.PAUSE_MODE_PROCESS
	Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	selectable_objects = get_selectable_objects()
	if len(selectable_objects) > 0:
		if optional_dict.has("DefaultButtonSelected"):
			select_object_by_name(optional_dict["DefaultButtonSelected"])
		else:
			select_object_by_index(0)
	setup_menu()
#	setup_controls()

func get_selectable_objects():
	var _sel_objects = []
	for _object in get_tree().current_scene.get_all_children(self):
		if _object.is_in_group("menus2d_buttons"):
			_sel_objects.append(_object)
	return _sel_objects

func inc_index(_current : int, _min : int, _max : int, _loop : bool):
	var _result : int = _current + 1
	if _result > _max:
		if _loop:
			_result = _min
		else:
			_result = _current
	return _result

func dec_index(_current : int, _min : int, _max : int, _loop : bool):
	var _result : int = _current - 1
	if _result < _min:
		if _loop:
			_result = _max
		else:
			_result = _current
	return _result

func do_action():
	selectable_objects[current_selected_object_index].do_click_action()

func select_object_by_index(_index : int):
	current_selected_object_index = _index
	update_objects()

func select_object_by_name(_name : String):
	for _sel_obj_index in range(len(selectable_objects)):
		if selectable_objects[_sel_obj_index].name == _name:
			current_selected_object_index = _sel_obj_index
			update_objects()
			break

func select_object_by_navigation(_navigation_key):
	var _current_object = selectable_objects[current_selected_object_index]
	if _current_object.navigation_dict.has(_navigation_key):
		var next_selected_object_name = _current_object.navigation_dict[_navigation_key]
		for _sel_obj_index in range(len(selectable_objects)):
			if selectable_objects[_sel_obj_index].name == next_selected_object_name:
				current_selected_object_index = _sel_obj_index
				update_objects()
				break

func set_optional_dict(_dict : Dictionary):
	self.optional_dict = _dict

#func setup_controls():
#	# MENU CONTROLS
#	var _controls = optional_dict["MenuControls"]
#	if _controls:
#		for _control_prop_key in _controls.keys():
#			var _action = InputEventAction.new()
#			var _prop_path : String = "input/" + _control_prop_key
#			ProjectSettings.set(_prop_path, 0)
#			var property_info = {
#				"name": _prop_path,
#				"type": TYPE_INT,
#				"hint": PROPERTY_HINT_ENUM,
#				"hint_string": ""
#			}
#			ProjectSettings.add_property_info(property_info)
#			var _input_evs = []
#			for _input_entry in _controls[_control_prop_key]:
#				match _input_entry[0]:
#					"keyboard":
#						var event_key = InputEventKey.new()
#						event_key.scancode = int(_input_entry[3])
#						_input_evs.append(event_key)
#					"gamepad":
#						var event_joypad
#						if _input_entry[1].find("BUTTON") > -1:
#							event_joypad = InputEventJoypadButton.new()
#							event_joypad.button_index = int(_input_entry[3])
#						else:
#							event_joypad = InputEventJoypadMotion.new()
#							event_joypad.axis = int(_input_entry[3])
#							if _input_entry[4]:
#								event_joypad.axis_value = -1.0
#							else:
#								event_joypad.axis_value = 1.0
#						_input_evs.append(event_joypad)
#					"mouse":
#						var event_mouse
#						if _input_entry[3] != null:
#							event_mouse = InputEventMouseButton.new()
#							event_mouse.button_index = int(_input_entry[3])
#							_input_evs.append(event_mouse)
#			var _total_input = {
#								"deadzone": 0.5,
#								"events": _input_evs
#								}
#			ProjectSettings.set_setting(_prop_path, _total_input)
#		ProjectSettings.save()

func setup_menu():
#	print(optional_dict)
	if node_info.has("SpecialObjects"):
		special_objects = node_info["SpecialObjects"]
		for _special_object_key in special_objects.keys():
			for _selectable_object in selectable_objects:
				if _special_object_key == _selectable_object.name:
					print("Selectable Object:", _selectable_object.name)
					_selectable_object.button_dict = special_objects[_special_object_key]
	pass

func update_objects():
	var _index : int = 0
	for _object in selectable_objects:
		_object.select_object(_index == current_selected_object_index)
		_index += 1

func connect_areas_signals(areas):
	for _area in areas:
		_area.connect("input_event", _area, "_on_Button_Area2D_input_event")
#		print("Area ", _area.name, " connected")

func create_exit_timer():
	_timer = Timer.new()
	_timer.connect("timeout", self,"_on_exit_timer")
	add_child(_timer)
	_timer.start(PAUSE_TIME)

#func get_areas():
#	var areas = []
#	for _child in get_children():
#		if _child is Area2D:
#			areas.append(_child)
#	return areas

func set_player_scene(_scene):
	_player_scene = _scene

func _on_exit_timer():
#	get_tree().paused = false
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	if _player_scene:
		_player_scene.stage_scene.is_paused = false
	else:
		var _children = get_tree().current_scene.get_child_count()
		if get_tree().current_scene.debug_hud_enabled:
			_children -= 1
#		print("GM children: " + str(_children))
		if _children == 1:
			get_tree().quit()
		else:
#			for _child in get_tree().current_scene.get_children():
#				print("Child ", _child.name)
			queue_free()

func _process(delta):
#	if Input.is_action_just_pressed("b2g_pause_game"):
#		if !_timer:
#			create_exit_timer()
	if Input.is_action_just_released("b2g_go_up"):
		select_object_by_navigation("NavigationUp")
	if Input.is_action_just_released("b2g_go_down"):
		select_object_by_navigation("NavigationDown")
	if Input.is_action_just_released("b2g_go_left"):
		select_object_by_navigation("NavigationLeft")
	if Input.is_action_just_released("b2g_go_right"):
		select_object_by_navigation("NavigationRight")
	if Input.is_action_just_released("b2g_action_0"):
		do_action()
	pass

