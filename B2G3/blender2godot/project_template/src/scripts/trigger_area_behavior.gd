class_name TriggerArea extends Area


export var on_entered_next_node_name : String
export var on_exited_next_node_name : String


func _ready():
	var _scene_to_connect = get_tree().current_scene.b2g_current_scene
	connect("body_entered", _scene_to_connect, "stage_trigger_entered", [self])
	connect("body_exited", _scene_to_connect, "stage_trigger_exited", [self])
