class_name PlayerBehavior extends KinematicBody


export var optional_dict : Dictionary
export var node_info : Dictionary

export var PAUSE_MENU_PATH : String = ""
export var gravity_enabled : bool

export var hud_scene_name : String
export var camera_inverted : bool = true

var _hud_dict : Dictionary
var _controls : Dictionary
var _animations : Dictionary
var _player_mesh_name : String = ""
var _actions : Dictionary
var _entity_properties : Dictionary
var _properties_linked : Dictionary

# TODO: PASS TO NODES
const GRAVITY = -24.8
const MAX_SPEED = 4.5
const JUMP_SPEED = 18
const ACCEL = 4.5
const DEACCEL= 16
const MAX_SLOPE_ANGLE = 40

var dir = Vector3()
var vel = Vector3()


var camera : Camera

var MOUSE_SENSITIVITY = 2.5
var GAMEPAD_AXIS_SENSITIVITY = 25.0

var player_mesh
var _hud
var mouse_rotation_axises = [false, false, false, false]

var current_delta = 0.0

var pause_control

var stage_scene

var gm_ref


func _ready():
	self.gm_ref = get_tree().current_scene
	gravity_enabled = optional_dict["GravityOn"] # TODO: pending to pass to nodes
	setup_dictionaries()
	player_mesh = find_player_mesh()
	camera = find_camera(optional_dict["PlayerCameraObject"]["CameraName"])
	mouse_rotation_axises = get_mouse_rotation_axises()
	Input.set_mouse_mode(Input.MOUSE_MODE_CAPTURED)
	if not _hud_dict.empty():
		add_hud()
	
	# TESTING
	#player_mesh._test_anim()

func add_hud():
	if _hud_dict.has("SceneName"):
		hud_scene_name = _hud_dict["SceneName"]
	if hud_scene_name != "":
		print("Adding HUD:", hud_scene_name)
		var _hud_scene_path : String = get_tree().current_scene.HUDS_SCENES_DIRPATH + "Hud_" + hud_scene_name + ".tscn"
		_hud = load(_hud_scene_path).instance()
		_hud.hud_settings = _hud_dict["Settings"]
		add_child(_hud)

func animate():
	if player_mesh:
		if not(_animations.empty()):
			if vel.z > 0.1:
				player_mesh._play_animation(_animations["forward"])
			elif vel.z < -0.1:
				player_mesh._play_animation(_animations["backward"])
			else:
				player_mesh._play_animation(_animations["idle"])

func create_pause():
	print(PAUSE_MENU_PATH)
	if PAUSE_MENU_PATH.ends_with("none.tscn"):
		get_tree().quit()
	else:
		stage_scene.is_paused = true
		Input.set_mouse_mode(Input.MOUSE_MODE_VISIBLE)
		yield(get_tree(),"idle_frame")
		var _pause_control_file = File.new()
		if _pause_control_file.file_exists(PAUSE_MENU_PATH): 
			pause_control = load(PAUSE_MENU_PATH).instance()
			pause_control.pause_mode = Node.PAUSE_MODE_PROCESS
			pause_control.set_player_scene(self)
			add_child(pause_control)
		else:
			get_tree().quit()

func find_camera(_camera_object_name):
#	print("Searching ", _camera_object_name, " on ", self.name)
	var _camera
	_camera = find_child_by_name(self, _camera_object_name)
	if not _camera:
		_camera = Camera.new()
		_camera.name = "TestCamera"
		add_child(_camera)
		get_tree().current_scene.show_message("No player camera found")
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
		if _child.name == _player_mesh_name:
			_player_mesh = _child
			break
	return _player_mesh

func get_mouse_rotation_axises():
	var mra = mouse_rotation_axises
	var mra_index = 0
	var _rotates = ["b2g_rotate_up", "b2g_rotate_down", "b2g_rotate_left", "b2g_rotate_right"]
	for _rotate in _rotates:
		for _control in _controls[_rotate]:
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

func set_entity_property_value(_property_name, _value):
	var _translated_value
	match typeof(_value):
		TYPE_BOOL:
			_translated_value = _value
		TYPE_INT:
			_translated_value = int(_value)
		TYPE_REAL:
			_translated_value = float(_value)
		TYPE_STRING:
			_translated_value = String(_value)
	_entity_properties[_property_name]["Value"] = _translated_value
	# TODO: EMIT A SIGNAL TO LINKED CONTROLS?

func setup_dictionaries():
	if self.node_info.has("HUD"):
		self._hud_dict = self.gm_ref.get_tree_node(node_info["HUD"], self.gm_ref.gm_dict)
		self._properties_linked = self.node_info["PropertiesLinked"]
	if self.optional_dict.has("PlayerAnimations"):
		self._animations = self.optional_dict["PlayerAnimations"]
	if self.optional_dict.has("PlayerControls"):
		self._controls = self.optional_dict["PlayerControls"]
	else:
		print("PlayerControls not found on optional_dict")
	if self.optional_dict.has("PlayerEntityProperties"):
		self._entity_properties = self.optional_dict["PlayerEntityProperties"]
	if self.node_info.has("ActionsSettings"):
		self._actions = self.node_info["ActionsSettings"]

func toogle_pause():
	pause_game_enable(!get_tree().paused)

func set_optional_dict(_dict : Dictionary):
	self.optional_dict = _dict

func set_stage_scene(_scene):
	stage_scene = _scene

func _physics_process(delta):
	if not stage_scene.is_paused:
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
			print("pressed")
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
			self.rotate_object_local(Vector3.UP, deg2rad(GAMEPAD_AXIS_SENSITIVITY * -_delta))
	if Input.is_action_pressed("b2g_rotate_right"):
		if camera_inverted:
			self.rotate_object_local(Vector3.UP, deg2rad(GAMEPAD_AXIS_SENSITIVITY * -_delta))
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
	if not stage_scene.is_paused:
		if event is InputEventMouseMotion and (Input.get_mouse_mode() == Input.MOUSE_MODE_CAPTURED):
			if mouse_rotation_axises[0] or mouse_rotation_axises[1]:
				if camera_inverted:
					camera.rotate_x(deg2rad(event.relative.y * MOUSE_SENSITIVITY * current_delta))
				else:
					camera.rotate_x(deg2rad(event.relative.y * MOUSE_SENSITIVITY * -current_delta))

			if mouse_rotation_axises[2] or mouse_rotation_axises[3]:
				self.rotate_object_local(Vector3.UP, deg2rad(event.relative.x * MOUSE_SENSITIVITY * -current_delta))

