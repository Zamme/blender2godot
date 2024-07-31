class_name HudBehavior extends Control


const FONT_POS_FACTOR_X = 21.5
const FONT_POS_FACTOR_Y = 42.0

const FONT_FACTOR = 40

export var optional_dict : Dictionary

export var hud_settings : Dictionary
export var hud_fields : Dictionary

var hud_objects_info : Dictionary
var fade_timer : Timer
var fade_tween : Tween

var gm_ref

#onready var hud_bg : TextureRect = get_child(0)


func _ready():
	self.gm_ref = get_tree().current_scene
	modulate = Color(0.0, 0.0, 0.0, 0.0)
	setup_hud_objects_info()
	start_hud()
	update_hud_objects_info()

func add_fade_timer():
	fade_timer = Timer.new()
	fade_timer.name = "FadeTimer"
	fade_timer.one_shot = true
	add_child(fade_timer)
	fade_timer.connect("timeout", self, "_on_fade_timer_timeout")

func add_fade_tween():
	fade_tween = Tween.new()
	fade_tween.name = "FadeTween"
	add_child(fade_tween)

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

func setup_hud_objects_info():
	if optional_dict.has("Objects"):
		hud_objects_info = optional_dict["Objects"]

func start_fade():
	fade_tween.interpolate_property(self, "modulate",
			Color(1.0, 1.0, 1.0, 0.0), Color(1.0, 1.0, 1.0, 1.0), hud_settings["ShowTransitionTime"],
			Tween.TRANS_LINEAR, Tween.EASE_IN_OUT)
	fade_tween.start()

func start_hud():
	if not fade_timer:
		add_fade_timer()
	if not fade_tween:
		add_fade_tween()
	match hud_settings["VisibilityType"]:
		"always":
			fade_timer.start(hud_settings["ShowTransitionTime"])

#func update_hud_object_info(_key):
#	# TODO: If is not TEXT?
#	if hud_objects_info[_key].has("SourceInfoProperty"):
#		var _linked_entity = hud_objects_info[_key]["LinkedEntity"]
##		print("Linked entity: " + _linked_entity.name)
#		var _source_info_property_name = hud_objects_info[_key]["SourceInfoProperty"]
##		print("Property name: " + _source_info_property_name)
#		var _value_to_assign = _linked_entity._entity_properties[_source_info_property_name]["Value"]
#		hud_objects_info[_key]["LinkedControl"].text = str(_value_to_assign)

func update_hud_objects_info():
	for _hud_element in get_children():
		if self.hud_fields.has(_hud_element.name):
			var _links = self.hud_fields[_hud_element.name]
			for _link_key in _links.keys(): # MORE THAN ONE INFO INPUT?
				var _from_node = self.gm_ref.get_tree_node(_link_key, self.gm_ref.gm_dict)
				var _value_to_assign
				match _from_node["Type"]:
					"B2G_Player_Scene_Node":
						if _from_node.has("EntityProperties"):
#							print("Searching: ", _from_node["SceneName"] + "Entity")
							var _scene_node = self.gm_ref.find_node(_from_node["SceneName"] + "Entity", true, false)
							_value_to_assign = _scene_node._entity_properties[_links[_link_key]]["Value"]
#							print("Scene node found: ", _scene_node.name)
					_:
						_value_to_assign = _from_node["Value"]
				_hud_element.text = str(_value_to_assign)

#	var _parent_props : Dictionary = get_parent()._properties_linked
#	for _parent_prop_key in _parent_props.keys():
#		for _child in get_children():
#			if _parent_props[_parent_prop_key] == _child.name:
#				_child.text = str(get_parent()._entity_properties[_parent_prop_key]["Value"])

func _on_fade_timer_timeout():
	start_fade()

