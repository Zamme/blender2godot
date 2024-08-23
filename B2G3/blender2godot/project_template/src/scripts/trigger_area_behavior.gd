class_name TriggerArea extends Area


export var on_entered_next_node_name : String
export var on_exited_next_node_name : String
export var physics_groups : Array = Array()


func _ready():
	yield(get_tree().create_timer(1.0), "timeout")
	self.initialize_trigger()

func initialize_trigger():
	connect("body_entered", self, "on_object_entered")
	connect("body_exited", self, "on_object_exited")

func on_object_entered(_body_entered):
	for _group in physics_groups:
		if _body_entered.is_in_group(_group):
			var _scene_to_connect = get_tree().current_scene.b2g_current_scene
			_scene_to_connect.stage_trigger_entered(self)
			break

func on_object_exited(_body_entered):
	for _group in physics_groups:
		if _body_entered.is_in_group(_group):
			var _scene_to_connect = get_tree().current_scene.b2g_current_scene
			_scene_to_connect.stage_trigger_exited(self)
			break
