class_name HudElementContent extends Label


var node_info : Dictionary

var current_value : String = ""
var is_variable : bool


func _ready():
	pass

func set_value(_value):
	self.current_value = str(_value)

func update_content():
	print("Updating content ", name)
	self.text = self.current_value
