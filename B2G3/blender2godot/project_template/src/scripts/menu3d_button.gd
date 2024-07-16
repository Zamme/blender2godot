class_name Menu3d_Button extends MeshInstance


#export var action_to_do : String = "None"
#export var action_parameter = "None"

var button_dict : Dictionary
var _button_collider : StaticBody
var _selected_effect_mesh : MeshInstance

var gm_ref


func _ready():
	self.gm_ref = get_tree().current_scene
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
	_new_mat.albedo_color = self.gm_ref.SELECTED_OBJECT_OVERLAY_COLOR
	_mesh.material_overlay = _new_mat
	return _mesh

func do_click_action():
	var _msg : String
	var _action_to_do : String
	var _action_parameter : String
	if self.button_dict.has("ActionOnClick"):
		_action_to_do = self.button_dict["ActionOnClick"]
		_msg = self.button_dict["ActionOnClick"]
		if self.button_dict.has("ActionParameter"):
			_action_parameter = self.button_dict["ActionParameter"]
			_msg += " " + self.button_dict["ActionParameter"]
	self.gm_ref.execute_command(_action_to_do, _action_parameter)
#	print(_msg)

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
#			print("clicked")
			do_click_action()
		else:
			pass
#			print("unclicked")
	#elif _event is InputEventMouseMotion:
		#print("hovering")
