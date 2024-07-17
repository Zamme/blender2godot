class_name Menu2DBehavior extends Control


const PAUSE_TIME = 0.15

var _timer : Timer
var _areas
var _player_scene

var selectable_objects = []
var current_selected_object_index = -1
export var optional_dict : Dictionary


func _ready():
	pause_mode = Node.PAUSE_MODE_PROCESS
	selectable_objects = get_selectable_objects()
	if len(selectable_objects) > 0:
		select_object(0)
	setup_menu()

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

func select_object(_index : int):
	current_selected_object_index = _index
	update_objects()

func set_optional_dict(_dict : Dictionary):
	self.optional_dict = _dict

func setup_menu():
	print(optional_dict)
	for _special_object_key in optional_dict["SpecialObjects"].keys():
		for _selectable_object in selectable_objects:
			print("Selectable Object:", _selectable_object.name)
			if _special_object_key == _selectable_object.name:
				_selectable_object.button_dict = optional_dict["SpecialObjects"][_special_object_key]

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

func get_areas():
	var areas = []
	for _child in get_children():
		if _child is Area2D:
			areas.append(_child)
	return areas

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
	if Input.is_action_just_pressed("b2g_pause_game"):
		if !_timer:
			create_exit_timer()
	if Input.is_action_just_released("b2g_go_forward"):
		select_object(dec_index(current_selected_object_index, 0, len(selectable_objects)-1, false))
	if Input.is_action_just_released("b2g_go_backward"):
		select_object(inc_index(current_selected_object_index, 0, len(selectable_objects)-1, false))
	if Input.is_action_just_released("b2g_action_0"):
		do_action()

