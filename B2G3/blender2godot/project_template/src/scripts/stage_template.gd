tool
class_name StageTemplate extends Spatial


enum COLLIDER_TYPE {CONVEX, MESH, SMART}

const MODELS_PATH = "res://assets/models/"
const HUDS_TEXTURES_PATH = "res://assets/huds/"
const MENUS2D_TEXTURES_PATH = "res://assets/menus2d/"
const SCENES_PATH = "res://src/scenes/"
const SCRIPTS_PATH = "res://src/scripts/"
const STAGE_BEHAVIOR_SCRIPT_PATH = SCRIPTS_PATH + "stage_behavior.gd"
const PLAYER_ENTITIES_PATH = SCENES_PATH + "players/"
const STAGES_PATH = SCENES_PATH + "stages/"
const STAGE_TEMPLATE_PATH = STAGES_PATH + "Stage_Template.tscn"
const STAGE_SCENES_PREFIX = "Stage_"

const PLAYER_SCENE_PATH = SCENES_PATH + "Player_Template.tscn"
const PLAYER_BEHAVIOR_PATH = "res://src/scripts/player_template.gd"
const PLAYER_MESH_BEHAVIOR_PATH = "res://src/scripts/player_mesh_behavior.gd"

const MENUS_PATH = SCENES_PATH + "menus/"
const MENU_SCENES_PREFIX = "Menu_"
const MENU_BEHAVIOR_PATH = "res://src/scripts/menu_behavior.gd"
const BUTTON_BEHAVIOR_PATH = "res://src/scripts/menu_button_class.gd"

const HUDS_PATH = SCENES_PATH + "huds/"
const HUD_SCENES_PREFIX = "Hud_"
const HUD_BEHAVIOR_FILEPATH = "res://src/scripts/hud_behavior.gd"

const MENUS2D_PATH = SCENES_PATH + "menus2d/"
const MENUS2D_SCENES_PREFIX = "Menu2d_"
const MENUS2D_BEHAVIOR_FILEPATH = "res://b2g_tools/B2G_Pause.gd"

const LIGHTS_SCENE_PATH = SCENES_PATH + "Lights.tscn"
const INFOS_DIRPATH = "res://infos/"
const COLLIDERS_JSON_PATH = INFOS_DIRPATH + "colliders_info.json"
const LIGHTS_JSON_PATH = INFOS_DIRPATH + "lights_info.json"
const PLAYER_INFO_JSON_PATH = INFOS_DIRPATH + "players_info.json"
const MENUS_INFO_JSON_PATH = INFOS_DIRPATH + "menus_info.json"
const HUDS_JSON_PATH = INFOS_DIRPATH + "huds_info.json"
const COLLIDERS_MATRIX_PATH = INFOS_DIRPATH + "colliders_matrix.txt"
const GODOT_PROJECT_SETTINGS_JSON_PATH = INFOS_DIRPATH + "godot_project_settings.json"
const STAGES_INFO_JSON_PATH = INFOS_DIRPATH + "stages_info.json"
const MENUS2D_INFO_JSON_PATH = INFOS_DIRPATH + "menus2d_info.json"

#const PLAYER_SPAWN_OBJECT_NAME = "B2G_PlayerSpawn"

#var camera_instance : Camera = null
#var player_instance : KinematicBody = null
var lights_instance : Spatial = null
#
#var player_height : float = 1.5
#var player_radius : float = 0.2
#var player_velocity : float = 1.0 # TODO: manage from blender
#
##var minimum_collider_size = 0.1
#var initial_player_position : Vector3 = Vector3.ZERO
#var initial_player_rotation : Vector3 = Vector3.ZERO
#export var player_gravity_on : bool
#export var player_camera_inverted : bool

var imported_scenes : Array
var scene_objects_list : Array
var scene_collider : StaticBody = null

var scene_colliding_matrix : Array
var matrix_dims : Vector3 = Vector3(50,50,50)
var matrix_offset : Vector3

var lights_to_remove_from_scene = []

var quit_timer : Timer

# JSONS
var _stages_json
var _player_json
var _menus_json
var _colliders_json
var _lights_json
var _huds_json
var _menus2d_json


func _ready():
	if Engine.editor_hint:
		print("Stage template present!")
		if ProjectSettings.get_setting("application/run/main_scene").find("Stage_Template.tscn"):
			_stages_json = read_json_file(STAGES_INFO_JSON_PATH)
			_player_json = read_json_file(PLAYER_INFO_JSON_PATH)
			_menus_json = read_json_file(MENUS_INFO_JSON_PATH)
			_colliders_json = self.read_json_file(COLLIDERS_JSON_PATH)
			_lights_json = self.read_json_file(LIGHTS_JSON_PATH)
			_huds_json = self.read_json_file(HUDS_JSON_PATH)
			_menus2d_json = self.read_json_file(MENUS2D_INFO_JSON_PATH)
			if !self.mount_scenes():
				return
			yield(get_tree(),"idle_frame")
			apply_new_config()
			yield(get_tree(),"idle_frame")
			yield(get_tree().create_timer(2.0), "timeout")
			yield(get_tree(),"idle_frame")
			push_warning("StageTemplateDone")
			yield(get_tree(),"idle_frame")
			get_tree().quit()
		else:
			self.update_scene() # TODO
	else:
		self.play_game()


func add_collider(scene_object, collider_type, scene_to_save):
	"""
	if scene_collider == null:
		scene_collider = StaticBody.new()
		scene_collider.name = scene_to_save.name + "_Area"
		scene_to_save.add_child(scene_collider)
		scene_collider.set_owner(scene_to_save)
	var object_collider : CollisionShape = create_collision_shape(scene_object)
	object_collider.name = scene_object.name + "_collider"
	scene_collider.add_child(object_collider)
	object_collider.set_owner(scene_to_save)
	object_collider.transform.origin = scene_object.transform.origin
	"""
	match collider_type:
		COLLIDER_TYPE.CONVEX:
#			print("Creating convex collider on: " + scene_object.name)
			self.create_convex_collision_shape(scene_object)
		COLLIDER_TYPE.MESH:
#			print("Creating mesh collider on: " + scene_object.name)
			self.create_trimesh_collision_shape(scene_object)
		COLLIDER_TYPE.SMART:
			pass
			#self.create_collision_shape(scene_object, scene_to_save)


""" TODO
func add_light_area(scene_object, light_parameters):
	var new_arealight : 
	new_directionallight = DirectionalLight.new()
	lights_instance.add_child(new_directionallight)
	new_directionallight.set_owner(lights_instance)
	new_directionallight.global_transform.origin = light_parameters["position"]
	# Lacks rotation
	new_directionallight.light_color = light_parameters["color"]
	new_directionallight.light_energy = light_parameters["energy"]/1000 # Aprox
	new_directionallight.shadow_enabled = true
	#new_directionallight.omni_range = light_parameters["range"]
"""

func add_light_directional(scene_object, light_parameters):
	var new_directionallight : DirectionalLight
	new_directionallight = DirectionalLight.new()
	lights_instance.add_child(new_directionallight)
	new_directionallight.set_owner(lights_instance)
	new_directionallight.global_transform.origin = light_parameters["position"]
	new_directionallight.rotation_degrees = light_parameters["rotation"]
	new_directionallight.light_color = light_parameters["color"]
	new_directionallight.light_energy = light_parameters["energy"]
	new_directionallight.shadow_enabled = true
	#new_directionallight.omni_range = light_parameters["range"]


func add_light_point(scene_object, light_parameters):
	var new_omnilight : OmniLight
	new_omnilight = OmniLight.new()
	lights_instance.add_child(new_omnilight)
	new_omnilight.set_owner(lights_instance)
	new_omnilight.global_transform.origin = light_parameters["position"]
	new_omnilight.rotation_degrees = light_parameters["rotation"]
	new_omnilight.light_color = light_parameters["color"]
	new_omnilight.light_energy = light_parameters["energy"]/1000 # Aprox
	new_omnilight.shadow_enabled = true
	new_omnilight.omni_range = light_parameters["range"]


func add_light_spot(scene_object, light_parameters):
	var new_spotlight : SpotLight
	new_spotlight = SpotLight.new()
	lights_instance.add_child(new_spotlight)
	new_spotlight.set_owner(lights_instance)
	new_spotlight.global_transform.origin = light_parameters["position"]
	new_spotlight.rotation_degrees = light_parameters["rotation"]
	new_spotlight.light_color = light_parameters["color"]
	new_spotlight.light_energy = light_parameters["energy"]
	new_spotlight.shadow_enabled = true
	new_spotlight.spot_range = light_parameters["range"]


#func add_player(position, rotation):
#	player_instance = KinematicBody.new()
#	var player_collision_shape : CollisionShape = CollisionShape.new()
#	player_instance.add_child(player_collision_shape)
#	player_collision_shape.set_owner(player_instance)
#	var caps_shape : CapsuleShape = CapsuleShape.new()
#	caps_shape.height = player_height
#	caps_shape.radius = player_radius
#	player_collision_shape.shape = caps_shape
#	add_child(player_instance)
#	player_collision_shape.global_rotate(Vector3.RIGHT, deg2rad(-90.0))
#	player_instance.script = load(PLAYER_BEHAVIOR_PATH)
#	self.initial_player_position = position
#	player_instance.global_transform.origin = position
#	player_instance.global_transform.basis = Basis(rotation)
#	var camera_pos = position + Vector3(0, player_height/2,0)
#	self.create_camera(camera_pos, rotation)
#
#	var packed_scene = PackedScene.new()
#	packed_scene.pack(player_instance)
#	ResourceSaver.save(PLAYER_SCENE_PATH, packed_scene)
#	player_instance.queue_free()


func add_scene(scene_file_path, with_name = "Scene"):
	print("Adding scene " + scene_file_path)
	var _dir : Directory = Directory.new()
	if _dir.file_exists(scene_file_path):
		var scene_instance = load(scene_file_path).instance()
		scene_instance.name = with_name
		add_child(scene_instance)
		scene_instance.set_owner(self)
	else:
		print("Scene not found: ", scene_file_path)

func add_scene_to_scene(to_scene, scene_file_path, with_name = "Scene"):
	print("Adding scene " + scene_file_path)
	var _dir : Directory = Directory.new()
	if _dir.file_exists(scene_file_path):
		var scene_instance = load(scene_file_path).instance()
		#scene_instance.name = with_name
		to_scene.add_child(scene_instance)
		scene_instance.set_owner(to_scene)
#		if scene_instance.name == "Player":
#			print("Positioning player at:")
#			print(self.initial_player_position)
#			scene_instance.global_transform.origin = self.initial_player_position
	else:
		print("Scene not found: ", scene_file_path)

func add_scenes(scene_filepaths):
	for scene_filepath in scene_filepaths:
		self.add_scene(scene_filepath)

func add_scenes_to_new_scene(new_scene_name, scene_filepaths):
	var _new_scene : Spatial = Spatial.new()
	for scene_filepath in scene_filepaths:
		_new_scene.name = new_scene_name
		self.add_scene_to_scene(_new_scene, scene_filepath, new_scene_name)
	return _new_scene

func add_smart_collider(scene):
	print("Adding smart colliding...")
	
	# Create parent static body
	if scene_collider == null:
		scene_collider = StaticBody.new()
		scene_collider.name = scene.name + "_Area"
		scene.add_child(scene_collider)
		scene_collider.set_owner(scene)
		
	# Create boolean 3d matrix
	for x in range(matrix_dims.x):
		scene_colliding_matrix.append([])
		for y in range(matrix_dims.y):
			scene_colliding_matrix[x].append([])
			for z in range(matrix_dims.z):
				scene_colliding_matrix[x][y].append(false)
	#print(scene_colliding_matrix[34][24][9])
	
	# Get matrix bounds
	var min_x_object = null
	var min_y_object = null
	var min_z_object = null
	for ob in scene.get_children():
		if min_x_object == null:
			min_x_object = ob
		if min_y_object == null:
			min_y_object = ob
		if min_z_object == null:
			min_z_object = ob
		if ob is MeshInstance:
			# With AABB to start
			var ob_position : Vector3 = ob.transform.origin
			if ob_position.x < min_x_object.transform.origin.x:
				min_x_object = ob
			if ob_position.y < min_y_object.transform.origin.y:
				min_y_object = ob
			if ob_position.z < min_z_object.transform.origin.z:
				min_z_object = ob
	var corner_position : Vector3 = Vector3(min_x_object.transform.origin.x, min_y_object.transform.origin.y, min_z_object.transform.origin.z)
#	print("Corner position: {" + str(corner_position.x) + "," + str(corner_position.y) + "," + str(corner_position.z) + "}")
	matrix_offset = corner_position
	
	# Fill matrix
	for ob in scene.get_children():
		if ob is MeshInstance:
			# With AABB to start
			var ob_aabb : AABB = ob.mesh.get_aabb()
			var position_with_offset : Vector3 = ob_aabb.position + ob.transform.origin - matrix_offset
			var rounded_position : Vector3 = position_with_offset.round()
			var aabb_size : Vector3 = ob_aabb.size.round()
			for x in range(aabb_size.x):
				for y in range(aabb_size.y):
					for z in range(aabb_size.z):
						scene_colliding_matrix[rounded_position.x + x][rounded_position.y + y][rounded_position.z + z] = true
	
	# Output matrix to text file
	output_matrix()
	
	# Recreate matrix
	for x in range(matrix_dims.x):
				for y in range(matrix_dims.y):
					for z in range(matrix_dims.z):
						pass
						# Try to group in rectangles before colliders creation
						"""
						if scene_colliding_matrix[x][y][z] == true:
							var new_collider_collision_shape : CollisionShape = CollisionShape.new()
							var box_shape : BoxShape = BoxShape.new()
							new_collider_collision_shape.shape = box_shape
							scene_collider.add_child(new_collider_collision_shape)
							new_collider_collision_shape.set_owner(scene)
							new_collider_collision_shape.transform.origin = Vector3(x,y,z)
						"""


func apply_import_changes(scene):
	print("Aplying changes to " + scene.name)
	self.get_all_scene_objects(scene)
	for ob in self.scene_objects_list:
#		print("Changes to " + ob.name)
		if ob is MeshInstance: # MESHES
			if _colliders_json.has(ob.name):# ON SCENARIOS
				if _colliders_json[ob.name] == "none":
					pass
#					print("...without collider!")
				elif _colliders_json[ob.name] == "convex":
#					print("...with convex collider!")
					self.add_collider(ob, COLLIDER_TYPE.CONVEX, scene)
				elif _colliders_json[ob.name] == "mesh":
#					print("...with mesh collider!")
					self.add_collider(ob, COLLIDER_TYPE.MESH, scene)
				elif _colliders_json[ob.name] == "smart":
#					print("...with smart collider!")
					self.add_collider(ob, COLLIDER_TYPE.SMART, scene)
			elif _menus_json.has(scene.name):
				if _menus_json[scene.name]["SpecialObjects"].has(ob.name):
#					print("Special Object", ob.name, "found")
					match _menus_json[scene.name]["SpecialObjects"][ob.name]["ObjectType"]:
						"button":
							self.add_collider(ob, COLLIDER_TYPE.CONVEX, scene)
							ob.script = load(BUTTON_BEHAVIOR_PATH)
		elif _lights_json.has(ob.name):
			if lights_instance == null:
				lights_instance = Spatial.new()
				lights_instance.name = "Lights"
				self.add_child(lights_instance)
				#lights_instance.set_owner(self)
#			print("Adding light on :" + ob.name)
			var new_light_color : Color = Color(_lights_json[ob.name + "ColorR"], _lights_json[ob.name + "ColorG"], _lights_json[ob.name + "ColorB"])
			var new_light_position : Vector3 = Vector3(_lights_json[ob.name + "PositionX"], _lights_json[ob.name + "PositionZ"], -_lights_json[ob.name + "PositionY"])
			var new_light_rotation : Vector3 = Vector3(_lights_json[ob.name + "RotationX"] -90.0, _lights_json[ob.name + "RotationZ"], -_lights_json[ob.name + "RotationY"])
			var new_light_energy : float = _lights_json[ob.name + "Energy"]
			match _lights_json[ob.name]:
				"POINT":
					var light_params_dict = {
						"color" : new_light_color,
						"energy" : new_light_energy,
						"range" : _lights_json[ob.name + "Range"],
						"position" : new_light_position,
						"rotation" : new_light_rotation
					}
					self.add_light_point(ob, light_params_dict)
				"SUN":
					var light_params_dict = {
						"color" : new_light_color,
						"energy" : new_light_energy,
						"range" : _lights_json[ob.name + "Range"],
						"position" : new_light_position,
						"rotation" : new_light_rotation
					}
					self.add_light_directional(ob, light_params_dict)
				"SPOT":
					var light_params_dict = {
						"color" : new_light_color,
						"energy" : new_light_energy,
						"range" : _lights_json[ob.name + "Range"],
						"position" : new_light_position,
						"rotation" : new_light_rotation
					}
					self.add_light_spot(ob, light_params_dict)
				"AREA":
					var light_params_dict = {
						"color" : new_light_color,
						"energy" : new_light_energy,
						"range" : _lights_json[ob.name + "Range"],
						"position" : new_light_position,
						"rotation" : new_light_rotation
					}
					self.add_light_point(ob, light_params_dict) # TODO: Pending to update
			ob.get_parent().remove_child(ob)
			ob.queue_free()
#			lights_to_remove_from_scene.append(ob)
#	self.clear_lights(scene)
	#self.add_smart_collider(scene)
	"""
	if camera_instance == null:
		if player_info_json.has("GravityOn"):
			self.player_gravity_on = player_info_json["GravityOn"]
			print("Player gravity enabled:" + str(self.player_gravity_on))
			self.player_camera_inverted = player_info_json["CameraInverted"]
			print("Player camera inverted:" + str(self.player_camera_inverted))
		if player_info_json.has("InitialPositionX"):
			self.initial_player_position = Vector3(player_info_json["InitialPositionX"], player_info_json["InitialPositionZ"], -player_info_json["InitialPositionY"])
			if player_info_json.has("InitialRotationX"):
				self.initial_player_rotation = Vector3(0.0, player_info_json["InitialRotationZ"], player_info_json["InitialRotationY"])
		self.add_player(self.initial_player_position, self.initial_player_rotation)
	"""
	return scene


func apply_import_changes_to_list(scenes_list, path):
	for scene in scenes_list:
		self.apply_import_changes(scene)


#func clear_imported_scenes():
#	clear_lights()

func apply_new_config():
	var startup_scene_type : String
	var godot_project_settings_json = self.read_json_file(GODOT_PROJECT_SETTINGS_JSON_PATH)
	for _key in godot_project_settings_json.keys():
		match _key:
			"startup_scene_type":
				startup_scene_type = godot_project_settings_json["startup_scene_type"]
			"application/run/main_scene":
				var _start_scene_path : String
				match startup_scene_type:
					"stage":
						_start_scene_path = STAGES_PATH + STAGE_SCENES_PREFIX + str(godot_project_settings_json["application/run/main_scene"]) + ".tscn"
					"3dmenu":
						_start_scene_path = MENUS_PATH + MENU_SCENES_PREFIX + str(godot_project_settings_json["application/run/main_scene"]) + ".tscn"
				ProjectSettings.set_setting("application/run/main_scene", _start_scene_path)
			"application/boot_splash/bg_color":
				var _splits = godot_project_settings_json["application/boot_splash/bg_color"].split(",")
				var _color : Color = Color(_splits[0], _splits[1], _splits[2], _splits[3])
				ProjectSettings.set_setting("application/boot_splash/bg_color", _color)
			_:
				ProjectSettings.set_setting(_key, godot_project_settings_json[_key])


func clear_lights(_scene):
	print("Clearing lights...")
	for _light in lights_to_remove_from_scene:
		_light.queue_free()
		#print(_light.name, " cleared from ", _scene.name)
	print("End clearing lights.")
#	repack_scene(_scene, MODELS_PATH)

func create_camera(_camera_name):
	var camera_instance = Camera.new()
	camera_instance.name = _camera_name
	return camera_instance

#func create_collision_shape(scene_object, scene_to_save):
func create_collision_shape(scene_object):
	# TODO : SMART COLLIDER SET
	#scene_object.create_trimesh_collision()
	var new_collider_collision_shape : CollisionShape = CollisionShape.new()
	var sc_ob_mesh : Mesh = scene_object.get_mesh()
	new_collider_collision_shape.shape = sc_ob_mesh.create_convex_shape()
	return new_collider_collision_shape

func create_convex_collision_shape(scene_object):
	scene_object.create_convex_collision()

func create_player(_player_mesh_scene_name, _camera_props, _shape_props, _controls_props):
	print("Creating player...")
	var player_entity_instance : KinematicBody = KinematicBody.new()
	player_entity_instance.name = _player_mesh_scene_name + "Entity"
	var player_collision_shape : CollisionShape = CollisionShape.new()
	player_entity_instance.add_child(player_collision_shape)
	player_collision_shape.set_owner(player_entity_instance)
	var caps_shape : CapsuleShape = CapsuleShape.new()
	caps_shape.height = _shape_props["DimZ"]/2.0
	caps_shape.radius = max(_shape_props["DimX"], _shape_props["DimY"])/2.0
	player_collision_shape.shape = caps_shape
	player_entity_instance.script = load(PLAYER_BEHAVIOR_PATH)
	var _player_mesh_scene = load(SCENES_PATH + _player_mesh_scene_name + ".tscn").instance()
	player_entity_instance.add_child(_player_mesh_scene)
	_player_mesh_scene.set_owner(player_entity_instance)
	_player_mesh_scene.script = load(PLAYER_MESH_BEHAVIOR_PATH)
	var _player_camera = self.create_camera(_camera_props["CameraName"])
	player_entity_instance.add_child(_player_camera)
	_player_camera.set_owner(player_entity_instance)
	
	add_child(player_entity_instance)
	yield(get_tree(), "idle_frame")
	# TRANSFORMATIONS
	player_collision_shape.translate(Vector3(0.0, _shape_props["DimZ"]/2.5, 0.0))
	player_collision_shape.global_rotate(Vector3.RIGHT, deg2rad(-90.0))
	_player_camera.translate(Vector3(_camera_props["PosX"], _camera_props["PosZ"], -_camera_props["PosY"]))
	_player_camera.rotation_degrees = Vector3(rad2deg(_camera_props["RotX"]) - 90.0, rad2deg(_camera_props["RotZ"]), rad2deg(_camera_props["RotY"]))
	_player_camera.fov = rad2deg(_camera_props["FOV"])
	match _camera_props["KeepFOV"]:
		"AUTO":
			_player_camera.keep_aspect = Camera.KEEP_WIDTH
		"VERTICAL":
			_player_camera.keep_aspect = Camera.KEEP_HEIGHT
		"HORIZONTAL":
			_player_camera.keep_aspect = Camera.KEEP_WIDTH
	yield(get_tree(), "idle_frame")
	
	var packed_scene = PackedScene.new()
	packed_scene.pack(player_entity_instance)
	ResourceSaver.save(PLAYER_ENTITIES_PATH + _player_mesh_scene_name + "Entity" + ".tscn", packed_scene)
	player_entity_instance.queue_free()
	print("Player created.")
	
	# PLAYER CONTROLS
	for _control_prop_key in _controls_props.keys():
		var _action = InputEventAction.new()
		var _prop_path : String = "input/" + _control_prop_key
		ProjectSettings.set(_prop_path, 0)
		var property_info = {
			"name": _prop_path,
			"type": TYPE_INT,
			"hint": PROPERTY_HINT_ENUM,
			"hint_string": ""
		}
		ProjectSettings.add_property_info(property_info)
		var _input_evs = []
		for _input_entry in _controls_props[_control_prop_key]:
			match _input_entry[0]:
				"keyboard":
					var event_key = InputEventKey.new()
					event_key.scancode = int(_input_entry[3])
					_input_evs.append(event_key)
				"gamepad":
					var event_joypad
					if _input_entry[1].find("BUTTON") > -1:
						event_joypad = InputEventJoypadButton.new()
						event_joypad.button_index = int(_input_entry[3])
					else:
						event_joypad = InputEventJoypadMotion.new()
						event_joypad.axis = int(_input_entry[3])
						if _input_entry[4]:
							event_joypad.axis_value = -1.0
						else:
							event_joypad.axis_value = 1.0
					_input_evs.append(event_joypad)
				"mouse":
					var event_mouse
					if _input_entry[3] != null:
						event_mouse = InputEventMouseButton.new()
						event_mouse.button_index = int(_input_entry[3])
						_input_evs.append(event_mouse)
		var _total_input = {
							"deadzone": 0.5,
							"events": _input_evs
							}
		ProjectSettings.set_setting(_prop_path, _total_input)
	ProjectSettings.save()


func create_trimesh_collision_shape(scene_object):
	scene_object.create_trimesh_collision()


func dir_contents(path, file_type = ".glb"):
	var files_to_import = []
	var dir = Directory.new()
	if dir.open(path) == OK:
		dir.list_dir_begin()
		var file_name = dir.get_next()
		while file_name != "":
			if dir.current_is_dir():
				pass
			else:
				print("Found file: " + file_name)
				if file_name.ends_with(file_type):
					files_to_import.append(file_name)
			file_name = dir.get_next()
	else:
		print("An error occurred when trying to access the path " + MODELS_PATH)
	return files_to_import


func get_all_scene_objects(scene):
	for ob in scene.get_children():
		self.scene_objects_list.append(ob)
		if ob.get_child_count() > 0:
			self.get_all_scene_objects(ob)

func import_file(file_name):
	var filename_path = MODELS_PATH + file_name
	print("Importing " + file_name)
	var file_scene = load(filename_path).instance()
	var modified_scene = self.apply_import_changes(file_scene)
	var packed_scene = PackedScene.new()
	packed_scene.pack(modified_scene)
	var scene_file_path = SCENES_PATH + modified_scene.name + ".tscn"
	ResourceSaver.save(scene_file_path, packed_scene)
	file_scene.queue_free()
	#modified_scene.queue_free()
	imported_scenes.append(scene_file_path)


func import_files(files_to_import):
	if len(files_to_import) > 0:
		for f in files_to_import:
			self.import_file(f)
	else:
		print("No files to import.")


func mount_scenes():
	print("Mounting scene...")
	var files_to_import = self.dir_contents(MODELS_PATH)
	import_files(files_to_import)
	if (len(files_to_import) < 1):
		print("Mount scenes finished with no imported files")
		return false
	else:
		print("Imported files: ", len(files_to_import))
	
	# Create Stages
	var _index : int = 0
	for _file_to_import in files_to_import:
		var _fn_without_ext =  _file_to_import.get_file().trim_suffix("." + _file_to_import.get_file().get_extension())
		if _stages_json:
			for _key in _stages_json.keys():
				#print("In mount stages: ", _fn_without_ext, " vs ", _stages_json[_key]["SceneName"])
				if str(_fn_without_ext) == (_stages_json[_key]["SceneName"]):
					var _new_stage_name : String = STAGE_SCENES_PREFIX + _file_to_import.get_file()
					_new_stage_name = _new_stage_name.trim_suffix("." + _new_stage_name.get_extension())
					var _new_stage = self.add_scenes_to_new_scene(_new_stage_name, [self.imported_scenes[_index]])
	#				var _spawn_object = _new_stage.find_node(_stages_json[_key]["PlayerSpawnObjectName"])
	#				_spawn_object.name = PLAYER_SPAWN_OBJECT_NAME
					var _new_stage_path : String = STAGES_PATH + _new_stage_name + ".tscn"
					_new_stage.script = load(STAGE_BEHAVIOR_SCRIPT_PATH)
					self.repack_scene(_new_stage, _new_stage_path)
					_index += 1
	
	# Create Player
	for _file_to_import in files_to_import:
		var _fn_without_ext = _file_to_import.get_file().trim_suffix("." + _file_to_import.get_file().get_extension())
		if _player_json:
			if not _player_json.empty():
				if _player_json.has("PlayerSceneName"):
					if _player_json["PlayerSceneName"] == _fn_without_ext:
						var _cam_props = _player_json["PlayerCameraObject"]
						var _shape_props = _player_json["PlayerDimensions"]
						var _anims_props = _player_json["PlayerAnimations"]
						var _controls_props = _player_json["PlayerControls"]
						create_player(_fn_without_ext, _cam_props, _shape_props, _controls_props)
						_index += 1
		else:
			print("No player added")
	
	# Create Menus
	for _file_to_import in files_to_import:
		var _fn_without_ext = _file_to_import.get_file().trim_suffix("." + _file_to_import.get_file().get_extension())
		if _menus_json:
			for _key in _menus_json.keys():
				#print("In mount menus: ", _fn_without_ext, " vs ", _key)
				if str(_fn_without_ext) == _key:
					var _new_menu_name : String = "Menu_" + _file_to_import.get_file()
					_new_menu_name = _new_menu_name.trim_suffix("." + _new_menu_name.get_extension())
					var _new_menu = self.add_scenes_to_new_scene(_new_menu_name, [self.imported_scenes[_index]])
					var _new_menu_path : String = MENUS_PATH + _new_menu_name + ".tscn"
					_new_menu.script = load(MENU_BEHAVIOR_PATH)
					var _new_camera : Camera = Camera.new()
					var _new_camera_dict = _menus_json[_key]["MenuCameraObjectDict"]
					_new_camera.name = _new_camera_dict["MenuCameraObjectName"]
					_new_menu.add_child(_new_camera)
					_new_camera.set_owner(_new_menu)
					yield(get_tree(),"idle_frame")
					_new_camera.translate(Vector3(_new_camera_dict["Position"]["PosX"], _new_camera_dict["Position"]["PosZ"], -_new_camera_dict["Position"]["PosY"]))
					_new_camera.rotation_degrees = Vector3(rad2deg(_new_camera_dict["Rotation"]["RotX"]) - 90.0, rad2deg(_new_camera_dict["Rotation"]["RotZ"]), rad2deg(_new_camera_dict["Rotation"]["RotY"]))
					_new_camera.fov = rad2deg(_new_camera_dict["FOV"])
					match _new_camera_dict["KeepFOV"]:
						"AUTO":
							_new_camera.keep_aspect = Camera.KEEP_WIDTH
						"VERTICAL":
							_new_camera.keep_aspect = Camera.KEEP_HEIGHT
						"HORIZONTAL":
							_new_camera.keep_aspect = Camera.KEEP_WIDTH
					yield(get_tree(), "idle_frame")
					#_new_stage.script = load(STAGE_BEHAVIOR_SCRIPT_PATH)
					self.repack_scene(_new_menu, _new_menu_path)
					_index += 1
	
	# Create HUDs
	for _key in _huds_json.keys():
		var _new_hud_name : String = HUD_SCENES_PREFIX + _key
		var _new_hud_path : String = HUDS_PATH + _new_hud_name + ".tscn"
		var _new_hud : Control = Control.new()
		_new_hud.name = _new_hud_name
		_new_hud.set_anchors_preset(Control.PRESET_WIDE)
		var _new_texture_rect : TextureRect = TextureRect.new()
		_new_texture_rect.name = "TextureRect_" + _new_hud_name
		_new_hud.add_child(_new_texture_rect)
		_new_texture_rect.set_owner(_new_hud)
		_new_texture_rect.set_anchors_preset(Control.PRESET_WIDE)
		var _texture_format = _huds_json[_key]["Settings"]["ExportFormat"]
		var _svg_path : String = HUDS_TEXTURES_PATH + _key + "." + _texture_format
		_new_texture_rect.texture = load(_svg_path)
		_new_texture_rect.expand = true
		_new_hud.script = load(HUD_BEHAVIOR_FILEPATH)
		self.repack_scene(_new_hud, _new_hud_path)
	
	# Create Menus2d
	for _key in _menus2d_json.keys():
		var _new_menu2d_name : String = MENUS2D_SCENES_PREFIX + _key
		var _new_menu2d_path : String = MENUS2D_PATH + _new_menu2d_name + ".tscn"
		var _directory : Directory = Directory.new()
		if !_directory.dir_exists(MENUS2D_PATH):
			_directory.make_dir(MENUS2D_PATH)
		var _new_menu2d : Control = Control.new()
		_new_menu2d.name = _new_menu2d_name
		_new_menu2d.set_anchors_preset(Control.PRESET_WIDE)
		var _new_texture_rect : TextureRect = TextureRect.new()
		_new_texture_rect.name = "TextureRect_" + _new_menu2d_name
		_new_menu2d.add_child(_new_texture_rect)
		_new_texture_rect.set_owner(_new_menu2d)
		_new_texture_rect.set_anchors_preset(Control.PRESET_WIDE)
		var _texture_path : String = MENUS2D_TEXTURES_PATH + _key + ".png"
		_new_texture_rect.texture = load(_texture_path)
		_new_texture_rect.expand = true
		_new_menu2d.script = load(MENUS2D_BEHAVIOR_FILEPATH)
		self.repack_scene(_new_menu2d, _new_menu2d_path)
	
	return true
#	self.add_scenes(imported_scenes)
#	if lights_instance != null:
#		repack_scene(lights_instance, LIGHTS_SCENE_PATH)
#		lights_instance.queue_free()
#	self.add_scene(PLAYER_SCENE_PATH, "Player")
#	self.add_scene(LIGHTS_SCENE_PATH, "Lights")
#
#	repack_scene(self, STAGE_TEMPLATE_PATH)
	#self.add_scene(COLLIDERS_PATH, "Colliders")


func output_matrix():
	var output_matrix_text = []
	var phrase : String
	for x in range(matrix_dims.x):
		for y in range(matrix_dims.y):
			for z in range(matrix_dims.z):
				phrase = "{" + str(x) + "," + str(y) + "," + str(z) + "} "  + str(scene_colliding_matrix[x][y][z]) + "\n"
				output_matrix_text.append(phrase)
	var file = File.new()
	file.open(COLLIDERS_MATRIX_PATH, File.WRITE)
	for ph in output_matrix_text:
		file.store_string(ph)
	file.close()


func play_game():
	print("Playing...")
#	player_instance = find_node("Player")
#	player_instance.gravity_enabled = self.player_gravity_on
#	player_instance.camera_inverted = self.player_camera_inverted


func repack_scene(scene, filepath):
	var packed_scene = PackedScene.new()
	print("Repacking Scene: " + scene.name)
	packed_scene.pack(scene)
	ResourceSaver.save(filepath, packed_scene)


func read_json_file(filepath):
	var file = File.new()
	if not file.file_exists(filepath):
		print("Missing classes.json file.")
	else:
		file.open(filepath, file.READ)
		var json = file.get_as_text()
		#print("json ", filepath, " : ", json)
		var json_result = JSON.parse(json)
		file.close()
		return json_result.result


func smart_collider_update():
	print("Starting smart collider...")


func update_scene():
	print("Updating scene...")
	smart_collider_update()


# TEMP UNUSED CODE
"""
# Pack Colliders
var colliders_packed_scene = PackedScene.new()
print("Packing " + colliders_node.name)
colliders_packed_scene.pack(colliders_node)
ResourceSaver.save(COLLIDERS_PATH, colliders_packed_scene)
colliders_node.queue_free()
"""
"""
var colliders_node = Spatial.new()
colliders_node.name = "Colliders"
add_child(colliders_node)
#colliders_node.set_owner(self)

var box_shape : BoxShape = BoxShape.new()
var aabb : AABB = scene_object.get_aabb()
box_shape.set_extents((aabb.size/2) * scene_object.global_transform.basis.get_scale())
var v : Vector3 = Vector3(box_shape.extents.x, box_shape.extents.y, box_shape.extents.z)
if v.x < minimum_collider_size:
	v.x = minimum_collider_size
if v.y < minimum_collider_size:
	v.y = minimum_collider_size
if v.z < minimum_collider_size:
	v.z = minimum_collider_size
box_shape.set_extents(v)
return box_shape
"""
"""
print("Adding collider to " + scene_object.name)
var new_collider : StaticBody = StaticBody.new()
new_collider.name = scene_object.name + "_body"
var new_collider_collision_shape : CollisionShape = CollisionShape.new()

new_collider_collision_shape.shape = self.create_collision_shape(scene_object)
new_collider.global_transform.origin = get_calibrate_collider_center(scene_object)
colliders_node.add_child(new_collider)
new_collider.add_child(new_collider_collision_shape)
new_collider.set_owner(colliders_node)
new_collider_collision_shape.set_owner(colliders_node)
"""
"""
# Fix x rotation (blender to godot -90 degrees)
var new_rot : Vector3 = player_instance.get_rotation_degrees()
new_rot = new_rot + Vector3(-90.0, 0.0, 0.0)
camera_instance.set_rotation_degrees(new_rot)
"""
"""
func get_calibrate_collider_center(scene_object):
var new_origin_pos : Vector3 = Vector3.ZERO

return new_origin_pos

"""


#scene_object.create_trimesh_collision()
#scene_object.create_convex_collision()
"""
var new_collider : StaticBody = StaticBody.new()
new_collider.name = scene_object.name + "_body"
var new_collider_collision_shape : CollisionShape = CollisionShape.new()
var sc_ob_mesh : Mesh = scene_object.get_mesh()
new_collider_collision_shape.shape = sc_ob_mesh.create_convex_shape()
#new_collider.global_transform.origin = get_calibrate_collider_center(scene_object)
scene_object.add_child(new_collider)
new_collider.add_child(new_collider_collision_shape)
new_collider.set_owner(scene_to_save)
new_collider_collision_shape.set_owner(scene_to_save)
"""

"""
	#var all_scenes = self.dir_contents(SCENES_PATH, ".tscn")
	#print("Scenes:")
	#for sc in all_scenes:
		#print(sc)
	#self.apply_import_changes_to_list(imported_scenes, SCENES_PATH)
"""
