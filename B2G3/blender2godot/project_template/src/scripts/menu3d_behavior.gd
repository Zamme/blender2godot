class_name Menu3dBehavior extends Spatial



onready var _menu = get_node(name.replace("Menu3d_", ""))

var selectable_objects = []
var current_selected_object_index = -1


# DEBUG
const B2G_HUD_FILEPATH = "res://b2g_tools/B2G_HUD.tscn"
var b2g_hud


func _ready():
	selectable_objects = get_selectable_objects()
	if len(selectable_objects) > 0:
		select_object(0)
	# DEBUG
#	add_b2g_hud()
	pass

func get_selectable_objects():
	var _sel_objects = []
	for _object in GameManager.get_all_children(_menu):
		if _object is Menu3d_Button:
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

func update_objects():
	var _index : int = 0
	for _object in selectable_objects:
		_object.select_object(_index == current_selected_object_index)
		_index += 1

func _process(delta):
	if Input.is_action_just_released("b2g_go_forward"):
		select_object(dec_index(current_selected_object_index, 0, len(selectable_objects)-1, false))
	if Input.is_action_just_released("b2g_go_backward"):
		select_object(inc_index(current_selected_object_index, 0, len(selectable_objects)-1, false))
	if Input.is_action_just_released("b2g_action_0"):
		do_action()
	if Input.is_action_just_released("b2g_pause_game"):
		get_tree().quit()

# DEBUG
func add_b2g_hud():
	b2g_hud = load(B2G_HUD_FILEPATH).instance()
	add_child(b2g_hud)

func show_message(_text):
	b2g_hud.show_message(_text)
