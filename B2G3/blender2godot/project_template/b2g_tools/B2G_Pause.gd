extends Control


const PAUSE_TIME = 0.25

var _timer : Timer


func _ready():
	get_tree().paused = true

func create_exit_timer():
	_timer = Timer.new()
	_timer.connect("timeout", self,"_on_exit_timer")
	add_child(_timer)
	_timer.start(PAUSE_TIME)

func _on_exit_timer():
	get_tree().paused = false
	queue_free()

func _process(delta):
	if Input.is_action_just_pressed("b2g_pause_game"):
		if !_timer:
			create_exit_timer()
