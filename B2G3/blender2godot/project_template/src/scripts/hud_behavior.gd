class_name HudBehavior extends Control


const FONT_POS_FACTOR_X = 21.5
const FONT_POS_FACTOR_Y = 42.0

const FONT_FACTOR = 40

export var hud_objects_info : Dictionary
export var hud_settings : Dictionary

var fade_timer : Timer
var fade_tween : Tween

#onready var hud_bg : TextureRect = get_child(0)


func _ready():
	modulate = Color(0.0, 0.0, 0.0, 0.0)
	link_objects()
	update_hud_objects_info()
	start_hud()

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

func link_objects():
	for _key in hud_objects_info.keys():
		hud_objects_info[_key]["LinkedControl"] = find_child_by_name(self, _key)
		if hud_objects_info[_key].has("SourceInfoScene"):
			hud_objects_info[_key]["LinkedEntity"] = find_child_by_name(get_tree().current_scene, hud_objects_info[_key]["SourceInfoScene"])

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

func update_hud_object_info(_key):
	# TODO: If is not TEXT?
	if hud_objects_info[_key].has("SourceInfoProperty"):
		var _linked_entity = hud_objects_info[_key]["LinkedEntity"]
#		print("Linked entity: " + _linked_entity.name)
		var _source_info_property_name = hud_objects_info[_key]["SourceInfoProperty"]
#		print("Property name: " + _source_info_property_name)
		var _value_to_assign = _linked_entity._entity_properties[_source_info_property_name]["Value"]
		hud_objects_info[_key]["LinkedControl"].text = str(_value_to_assign)

func update_hud_objects_info():
	for _key in hud_objects_info.keys():
		update_hud_object_info(_key)

func _on_fade_timer_timeout():
	start_fade()

