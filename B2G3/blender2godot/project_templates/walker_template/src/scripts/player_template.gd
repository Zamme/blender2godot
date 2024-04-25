extends KinematicBody

const GRAVITY = -24.8
var vel = Vector3()
const MAX_SPEED = 4.5
const JUMP_SPEED = 18
const ACCEL = 4.5

var dir = Vector3()

const DEACCEL= 16
const MAX_SLOPE_ANGLE = 40

var camera
var rotation_helper

var MOUSE_SENSITIVITY = 0.05

var home_spatial : Spatial
var gravity_enabled : bool

export var camera_inverted := true

func _ready():
	#camera = $Rotation_Helper/Camera
	#rotation_helper = $Rotation_Helper
	#rotation_helper = self
	#camera = $Camera
	home_spatial = get_parent()
	
	#Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)

func process_input(delta):
	if Input.is_action_pressed("ui_cancel"):
		get_tree().quit()

func _physics_process(delta):
	process_input(delta)

"""
func _physics_process(delta):
	process_input(delta)
	process_movement(delta)

func process_input(delta):

	# ----------------------------------
	# Walking
	dir = Vector3()
	var cam_xform = camera.get_global_transform()

	var input_movement_vector = Vector2()

	if Input.is_action_pressed("ui_up"):
		input_movement_vector.y += 1
	if Input.is_action_pressed("ui_down"):
		input_movement_vector.y -= 1
	if Input.is_action_pressed("ui_left"):
		input_movement_vector.x -= 1
	if Input.is_action_pressed("ui_right"):
		input_movement_vector.x += 1
	if Input.is_action_pressed("ui_cancel"):
		get_tree().quit()
	
	input_movement_vector = input_movement_vector.normalized()

	# Basis vectors are already normalized.
	dir += -cam_xform.basis.z * input_movement_vector.y
	dir += cam_xform.basis.x * input_movement_vector.x
	# ----------------------------------

	# ----------------------------------
	# Jumping
	if is_on_floor():
		if Input.is_action_just_pressed("ui_select"):
			vel.y = JUMP_SPEED
	# ----------------------------------

	# ----------------------------------
	# Capturing/Freeing the cursor
	if Input.is_action_just_pressed("ui_cancel"):
		if Input.get_mouse_mode() == Input.MOUSE_MODE_VISIBLE:
			Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
		else:
			Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
	# ----------------------------------

func process_movement(delta):
	if self.gravity_enabled:
		dir.y = 0
		dir = dir.normalized()
		
		vel.y += delta * GRAVITY
	
		var hvel = vel
		hvel.y = 0
	
		var target = dir
		target *= MAX_SPEED
	
		var accel
		if dir.dot(hvel) > 0:
			accel = ACCEL
		else:
			accel = DEACCEL
	
		hvel = hvel.linear_interpolate(target, accel * delta)
		vel.x = hvel.x
		vel.z = hvel.z
		vel = move_and_slide(vel, Vector3(0, 1, 0), 0.05, 4, deg2rad(MAX_SLOPE_ANGLE))
	else:
		dir = dir.normalized()
		
		var hvel = vel
	
		var target = dir
		target *= MAX_SPEED
	
		var accel
		if dir.dot(hvel) > 0:
			accel = ACCEL
		else:
			accel = DEACCEL
	
		hvel = hvel.linear_interpolate(target, accel * delta)
		vel = hvel
		vel = move_and_slide(vel, Vector3(0, 1, 0), 0.05, 4, deg2rad(MAX_SLOPE_ANGLE))

func _input(event):
	if event is InputEventMouseMotion and Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED:
		if camera_inverted:
			rotation_helper.rotate_x(deg2rad(event.relative.y * MOUSE_SENSITIVITY))
		else:
			rotation_helper.rotate_x(deg2rad(event.relative.y * MOUSE_SENSITIVITY * -1.0))
		
		self.rotate_y(deg2rad(event.relative.x * MOUSE_SENSITIVITY * -1))

		var camera_rot = rotation_helper.rotation_degrees
		camera_rot.x = clamp(camera_rot.x, -70, 70)
		rotation_helper.rotation_degrees = camera_rot
"""
