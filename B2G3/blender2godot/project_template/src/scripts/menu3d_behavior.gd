class_name Menu3dBehavior extends Spatial



onready var _menu = get_node(name.replace("Menu3d_", ""))

var selectable_objects = []
var current_selected_object_index = -1
export var optional_dict : Dictionary
export var node_info : Dictionary

var gm_ref


func _ready():
	self.gm_ref = get_tree().current_scene
	selectable_objects = get_selectable_objects()
	if len(selectable_objects) > 0:
		if optional_dict.has("DefaultButtonSelected"):
			select_object_by_name(optional_dict["DefaultButtonSelected"])
		else:
			select_object_by_index(0)
	setup_menu()

static func get_all_children(in_node,arr:=[]):
	arr.push_back(in_node)
	for child in in_node.get_children():
		arr = get_all_children(child,arr)
	return arr

func get_selectable_objects():
	# TODO: Add by position order
	var _sel_objects = []
	for _object in get_all_children(_menu):
		if _object.is_in_group("menus3d_buttons"):
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

func setup_menu():
#	print(optional_dict)
	for _special_object_key in optional_dict["SpecialObjects"].keys():
		for _selectable_object in selectable_objects:
#			print("Selectable Object:", _selectable_object.name)
			if _special_object_key == _selectable_object.name:
				_selectable_object.button_dict = self.gm_ref.current_node["SpecialObjects"][_special_object_key]

func update_objects():
	var _index : int = 0
	for _object in selectable_objects:
		_object.select_object(_index == current_selected_object_index)
		_index += 1

func _process(delta):
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

