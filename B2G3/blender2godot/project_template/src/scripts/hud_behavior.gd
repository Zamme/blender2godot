class_name HudBehavior extends Control


export var hud_objects_info : Dictionary
export var hud_settings : Dictionary

var fade_timer : Timer
var fade_tween : Tween

onready var hud_bg : TextureRect = get_child(0)


func _ready():
	modulate = Color(0.0, 0.0, 0.0, 0.0)
	config_hud()
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

func config_hud():
	for _hud_object_info in hud_objects_info.keys():
#		print(_hud_object_info)
		match hud_objects_info[_hud_object_info]["Type"]:
			"FONT":
				print(hud_objects_info[_hud_object_info]["Location"])
				var _new_label : Label = Label.new()
				_new_label.name = _hud_object_info
				hud_bg.add_child(_new_label)
				_new_label.set_anchors_preset(Control.PRESET_CENTER, true)
				_new_label.align = Label.ALIGN_CENTER
				_new_label.valign = Label.VALIGN_CENTER
#				_new_label.owner = self
				_new_label.text = hud_objects_info[_hud_object_info]["Body"]
				var _location_split = hud_objects_info[_hud_object_info]["Location"].split(",")
				_new_label.rect_position += Vector2(float(_location_split[0]), float(_location_split[1]))

func read_json_file(filepath):
	var file = File.new()
	if not file.file_exists(filepath):
		print("Missing classes.json file.")
	else:
		file.open(filepath, file.READ)
		var json = file.get_as_text()
#		print("json ", filepath, " : ", json)
		var json_result = JSON.parse(json)
		file.close()
		return json_result.result

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

func _on_fade_timer_timeout():
	start_fade()

