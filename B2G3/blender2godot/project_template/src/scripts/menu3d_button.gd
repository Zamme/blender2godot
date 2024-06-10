class_name Menu3d_Button extends MeshInstance


export var action_to_do : String = "None"
export var action_parameter = "None"

var _button_collider : StaticBody
var _selected_effect_mesh : MeshInstance


func _ready():
	_button_collider = get_collider()
	_selected_effect_mesh = create_selected_effect_mesh()
	_selected_effect_mesh.hide()
	add_on_click_event()

func add_on_click_event():
	_button_collider.connect("input_event", self, "_on_click_event")

func create_selected_effect_mesh():
	var _mesh : MeshInstance = MeshInstance.new()
	_mesh.name = "sel_mesh_" + name
	_mesh.mesh = mesh
	add_child(_mesh)
	_mesh.set_owner(get_parent())
	var _new_mat : SpatialMaterial = SpatialMaterial.new()
	_new_mat.flags_transparent = true
	_new_mat.albedo_color = GameManager.SELECTED_OBJECT_OVERLAY_COLOR
	_mesh.material_overlay = _new_mat
	return _mesh

func do_click_action():
	var _msg : String = action_to_do + " " + action_parameter
	print(_msg)
#	get_parent().get_parent().show_message(_msg)
	var _param : String
	match action_to_do:
		"load_stage":
			_param = StageTemplate.STAGES_PATH + action_parameter + ".tscn"
			get_tree().current_scene.load_scene(_param, true)
		"menu_stage":
			_param = StageTemplate.MENUS3D_PATH + action_parameter + ".tscn"
			get_tree().current_scene.load_scene(_param, true)
		"quit_game":
			get_tree().quit()

func get_collider():
	for _child in get_children():
		if _child is StaticBody:
			return _child

func select_object(_selected : bool):
	if _selected:
		_selected_effect_mesh.show()
	else:
		_selected_effect_mesh.hide()

func _on_click_event(_cam, _event, _pos, _norm, _s_idx):
	if _event is InputEventMouseButton:
		if _event.pressed:
			print("clicked")
			do_click_action()
		else:
			print("unclicked")
	#elif _event is InputEventMouseMotion:
		#print("hovering")
