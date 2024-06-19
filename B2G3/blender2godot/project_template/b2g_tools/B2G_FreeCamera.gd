class_name FreeCamera extends Camera

const MOUSE_SENSITIVITY = 0.1
const MOTION_SPEED = 5.0

var current_delta

var rot_x = 0
var rot_y = 0

func _ready():
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func _input(event):
	if Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
		if current_delta:
			if event is InputEventMouseMotion:
				rot_x += event.relative.x * MOUSE_SENSITIVITY * -current_delta
				rot_y += event.relative.y * MOUSE_SENSITIVITY * -current_delta
				transform.basis = Basis() # reset rotation
				rotate_object_local(Vector3(0, 1, 0), rot_x) # first rotate in Y
				rotate_object_local(Vector3(1, 0, 0), rot_y) # then rotate in X

func _physics_process(delta):
	current_delta = delta
	if Input.is_action_pressed("ui_up"):
		translate(Vector3.FORWARD * delta * MOTION_SPEED)
	if Input.is_action_pressed("ui_down"):
		translate(Vector3.BACK * delta * MOTION_SPEED)
	if Input.is_action_pressed("ui_left"):
		translate(Vector3.LEFT * delta * MOTION_SPEED)
	if Input.is_action_pressed("ui_right"):
		translate(Vector3.RIGHT * delta * MOTION_SPEED)
	if Input.is_action_just_released("ui_cancel"):
		get_tree().quit()
	if Input.is_action_just_pressed("ui_focus_next"):
		if Input.get_mouse_mode() == Input.MOUSE_MODE_VISIBLE:
			Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
		else:
			Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
