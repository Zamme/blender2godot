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
			Color(1.0, 1.0, 1.0, 0.0), Color(1.0, 1.0, 1.0, 1.0), hud_settings["show_transition_time"],
			Tween.TRANS_LINEAR, Tween.EASE_IN_OUT)
	fade_tween.start()

func start_hud():
	if not fade_timer:
		add_fade_timer()
	if not fade_tween:
		add_fade_tween()
	match hud_settings["visibility_type"]:
		"always":
			fade_timer.start(hud_settings["show_transition_time"])

func update_hud_objects_info():
	for _hud_element in get_children():
		if self.hud_fields.has(_hud_element.name):
			var _field = self.hud_fields[_hud_element.name]
			if _field.has("DefaultValue"):
				_hud_element.text = str(_field["DefaultValue"])
			elif _field.has("SourceNodeName"):
				var _source_node = self.gm_ref.get_tree_node(_field["SourceNodeName"], self.gm_ref.gm_dict)
				if _source_node["NodeProperties"].has("value"):
					_hud_element.text = str(_source_node["NodeProperties"]["value"])
#				else:
#					var _source_node_inputs = _

func _on_fade_timer_timeout():
	start_fade()

