class_name OverlayButton_Behavior extends Button


var gm_ref
export var button_dict : Dictionary

func _ready():
	self.gm_ref = get_tree().current_scene
	pause_mode = Node.PAUSE_MODE_PROCESS
	connect("button_up", self, "_on_click_button")

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
#	print("Message: ", _msg)
#	self.gm_ref.execute_command(_action_to_do, _action_parameter)
#	print("ActionToDo: ", _action_to_do)
#	print("ActionParameter: ", _action_parameter)
	match _action_to_do:
		"close_overlay":
			self.gm_ref.continue_game()
		"load_2dmenu":
			self.gm_ref.execute_node(_action_parameter)
		"load_3dmenu":
			self.gm_ref.execute_node(_action_parameter)
		"load_stage":
			self.gm_ref.execute_node(_action_parameter)
		"quit_game":
			self.gm_ref.quit_game()
		_:
			print("Action unknown!")
			self.gm_ref.show_message("Action Unknown")

func select_object(_selected : bool):
	if _selected:
		self.grab_focus()

func _on_click_button():
	do_click_action()

