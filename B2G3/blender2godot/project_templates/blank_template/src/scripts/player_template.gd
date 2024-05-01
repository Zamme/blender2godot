extends KinematicBody


const PLAYER_INFO_JSON_PATH = "res://player_info/player_info.json"

const GRAVITY = -24.8
var vel = Vector3()
const MAX_SPEED = 4.5
const JUMP_SPEED = 18
const ACCEL = 4.5

var dir = Vector3()

const DEACCEL= 16
const MAX_SLOPE_ANGLE = 40

var camera : Camera

var MOUSE_SENSITIVITY = 0.05

export var gravity_enabled : bool

export var camera_inverted := true
var player_json
var player_mesh : PlayerMesh

var _animations = {}
var _controls = {}


func _ready():
	player_json = read_json_file(PLAYER_INFO_JSON_PATH)
	gravity_enabled = player_json["GravityOn"]
	_animations = player_json["PlayerAnimations"]
	player_mesh = find_player_mesh()
	camera = find_camera(player_json["PlayerCameraObject"]["CameraName"])
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	
	# TESTING
	#player_mesh._test_anim()
	InputMap.action_erase_events("ui_end")

func animate():
	if vel.z > 0.1:
		player_mesh._play_animation(_animations["forward"])
	elif vel.z < -0.1:
		player_mesh._play_animation(_animations["backward"])
	else:
		player_mesh._play_animation(_animations["idle"])

func find_camera(_camera_object_name):
	print("Searching ", _camera_object_name, " on ", self.name)
	var _camera
	_camera = find_child_by_name(self, _camera_object_name)
	return _camera

func find_child_by_name(root_node, _object_name):
	var _object = null
	for _node in root_node.get_children():
		if _node.name == _object_name:
			_object = _node
			break
		else:
			_object = find_child_by_name(_node, _object_name)
			if _object != null:
				break
	return _object

func find_player_mesh():
	var _player_mesh = null
	for _child in get_children():
		if _child is PlayerMesh:
			_player_mesh = _child
			break
	return _player_mesh

func read_json_file(filepath):
	var file = File.new()
	if not file.file_exists(filepath):
		print("Missing classes.json file.")
	else:
		file.open(filepath, file.READ)
		var json = file.get_as_text()
		var json_result = JSON.parse(json)
		file.close()
		return json_result.result

func _physics_process(delta):
	process_input(delta)
	process_movement(delta)
	animate()

func process_input(_delta):

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
	if Input.is_action_just_pressed("ui_focus_next"):
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
			camera.rotate_x(deg2rad(event.relative.y * MOUSE_SENSITIVITY))
		else:
			camera.rotate_x(deg2rad(event.relative.y * MOUSE_SENSITIVITY * -1.0))
		
		self.rotate_y(deg2rad(event.relative.x * MOUSE_SENSITIVITY * -1))


