extends Sprite


const PAUSE_TIME = 0.25

var _timer : Timer
var _areas
var _player_scene


func _ready():
	pause_mode = Node.PAUSE_MODE_PROCESS
	_areas = get_areas()
	connect_areas_signals(_areas)
#	get_tree().paused = true

func connect_areas_signals(areas):
	for _area in areas:
		_area.connect("input_event", _area, "_on_Button_Area2D_input_event")
		print("Area ", _area.name, " connected")

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
	_player_scene.stage_scene.is_paused = false
	queue_free()

func _process(delta):
	if Input.is_action_just_pressed("b2g_pause_game"):
		if !_timer:
			create_exit_timer()

#func _input(_event):
#	if _event is InputEventMouseButton:
#		if _event.pressed:
#			print("Mouse button pressed")
#			print(_event.position)
#			var space_state = get_world_2d().direct_space_state
#			print(space_state.intersect_point(_event.position))
#			print(space_state.intersect_ray(_event.position, _event.position))
