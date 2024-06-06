extends KinematicBody


const HUDS_SCENES_DIRPATH = "res://src/scenes/huds/"

const GRAVITY = -24.8
var vel = Vector3()
const MAX_SPEED = 4.5
const JUMP_SPEED = 18
const ACCEL = 4.5

var dir = Vector3()

const DEACCEL= 16
const MAX_SLOPE_ANGLE = 40

var camera : Camera

var MOUSE_SENSITIVITY = 2.5
var GAMEPAD_AXIS_SENSITIVITY = 25.0

export var gravity_enabled : bool

export var camera_inverted := true
var player_json
var player_mesh : PlayerMesh

var _animations = {}
var _actions = {}
var _controls = {}
var _hud
var mouse_rotation_axises = [false, false, false, false]

var current_delta = 0.0

var pause_control : Control


func _ready():
	player_json = read_json_file(StageTemplate.PLAYER_INFO_JSON_PATH)
	gravity_enabled = player_json["GravityOn"]
	_animations = player_json["PlayerAnimations"]
	set_json_actions()
	player_mesh = find_player_mesh()
	camera = find_camera(player_json["PlayerCameraObject"]["CameraName"])
	mouse_rotation_axises = get_mouse_rotation_axises()
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	add_hud()
	
	# TESTING
	#player_mesh._test_anim()

func add_hud():
	if player_json.has("PlayerHUD"):
		var _hud_scene_name = player_json["PlayerHUD"]["HudSceneName"]
		if _hud_scene_name != "none":
			var _hud_scene_path : String = HUDS_SCENES_DIRPATH + "Hud_" + _hud_scene_name + ".tscn"
			_hud = load(_hud_scene_path).instance()
			add_child(_hud)

func animate():
	if vel.z > 0.1:
		player_mesh._play_animation(_animations["forward"])
	elif vel.z < -0.1:
		player_mesh._play_animation(_animations["backward"])
	else:
		player_mesh._play_animation(_animations["idle"])

func create_pause():
	yield(get_tree(),"idle_frame")
	pause_control = Control.new()
	pause_control.script = load("res://b2g_tools/B2G_Pause.gd")
	add_child(pause_control)
	pause_control.pause_mode = Node.PAUSE_MODE_PROCESS

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

func get_mouse_rotation_axises():
	var mra = mouse_rotation_axises
	var mra_index = 0
	var _rotates = ["b2g_rotate_up", "b2g_rotate_down", "b2g_rotate_left", "b2g_rotate_right"]
	for _rotate in _rotates:
		for _control in player_json["PlayerControls"][_rotate]:
			if _control[0] == "mouse":
				mra[mra_index] = true
#				print("Mouse Rotation: ", _rotate, mra[mra_index])
				mra_index += 1
	return mra

func pause_game_enable(_enable):
	if _enable:
		create_pause()
	else:
		pause_control.queue_free()
	print("Paused: ", get_tree().paused)

func toogle_pause():
	pause_game_enable(!get_tree().paused)

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

func set_json_actions():
	var _json_actions = player_json["PlayerActions"]
	for _action_key in _json_actions.keys():
		_actions["b2g_" + _action_key] = _json_actions[_action_key]
	#print(_actions)

func _physics_process(delta):
	current_delta = delta
	process_input(delta)
	process_movement(delta)
	process_actions(delta)
	animate()

func process_action(_action, _delta):
	print("Action ", _action)
	match _action:
		"APause":
			pause_game_enable(true)
		"AInteract":
			pass
		"AJump":
			if is_on_floor():
				vel.y = JUMP_SPEED
		"ACrouch":
			pass
		"AUse":
			pass
		"AIMinus":
			pass
		"AIPlus":
			pass
		"AHelp":
			pass
		"AFire":
			pass

func process_actions(_delta):
	for _action_key in _actions.keys():
		if Input.is_action_just_released(_action_key):
			process_action(_actions[_action_key], _delta)

func process_input(_delta):
	# ----------------------------------
	# Walking
	dir = Vector3()
	var cam_xform = camera.get_global_transform()

	var input_movement_vector = Vector2()

	if Input.is_action_pressed("b2g_go_forward"):
		input_movement_vector.y += 1
	if Input.is_action_pressed("b2g_go_backward"):
		input_movement_vector.y -= 1
	if Input.is_action_pressed("b2g_strafe_left"):
		input_movement_vector.x -= 1
	if Input.is_action_pressed("b2g_strafe_right"):
		input_movement_vector.x += 1
	#if Input.is_key_pressed(16777217):
		#get_tree().quit()
	
	input_movement_vector = input_movement_vector.normalized()

	# Basis vectors are already normalized.
	dir += -cam_xform.basis.z * input_movement_vector.y
	dir += cam_xform.basis.x * input_movement_vector.x
	# ----------------------------------
	# Rotating
	if Input.is_action_pressed("b2g_rotate_up"):
		if camera_inverted:
			camera.rotate_x(deg2rad(GAMEPAD_AXIS_SENSITIVITY * _delta))
		else:
			camera.rotate_x(deg2rad(GAMEPAD_AXIS_SENSITIVITY * -1.0 * _delta))
	if Input.is_action_pressed("b2g_rotate_down"):
		if camera_inverted:
			camera.rotate_x(deg2rad(GAMEPAD_AXIS_SENSITIVITY * -1.0 * _delta))
		else:
			camera.rotate_x(deg2rad(GAMEPAD_AXIS_SENSITIVITY * _delta))
	if Input.is_action_pressed("b2g_rotate_left"):
		if camera_inverted:
			self.rotate_object_local(Vector3.UP, deg2rad(GAMEPAD_AXIS_SENSITIVITY * _delta))
		else:
			self.rotate_object_local(Vector3.UP, deg2rad(GAMEPAD_AXIS_SENSITIVITY * -1.0 * _delta))
	if Input.is_action_pressed("b2g_rotate_right"):
		if camera_inverted:
			self.rotate_object_local(Vector3.UP, deg2rad(GAMEPAD_AXIS_SENSITIVITY * -1.0 * _delta))
		else:
			self.rotate_object_local(Vector3.UP, deg2rad(GAMEPAD_AXIS_SENSITIVITY * _delta))
	# ----------------------------------
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
		if mouse_rotation_axises[0] or mouse_rotation_axises[1]:
			if camera_inverted:
				camera.rotate_x(deg2rad(event.relative.y * MOUSE_SENSITIVITY * current_delta))
			else:
				camera.rotate_x(deg2rad(event.relative.y * MOUSE_SENSITIVITY * -1.0 * current_delta))
		
		if mouse_rotation_axises[2] or mouse_rotation_axises[3]:
			self.rotate_object_local(Vector3.UP, deg2rad(event.relative.x * MOUSE_SENSITIVITY * -1 * current_delta))

