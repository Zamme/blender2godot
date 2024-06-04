class_name HudBehavior extends Control


var hud_objects_info
var hud_settings

var fade_timer : Timer
var fade_tween : Tween


func _ready():
	modulate = Color(0.0, 0.0, 0.0, 0.0)
	get_json_info()
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

func get_json_info():
	var _json_result = read_json_file(StageTemplate.HUDS_JSON_PATH)
	var _hud_name : String = name.trim_prefix("Hud_")
	var hud_info = _json_result[_hud_name]
	hud_objects_info = hud_info["Objects"]
	hud_settings = hud_info["Settings"]

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

