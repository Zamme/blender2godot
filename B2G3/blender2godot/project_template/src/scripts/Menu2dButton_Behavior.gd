class_name Menu2dButton_Behavior extends Button


var gm_ref
export var button_dict : Dictionary
export var navigation_dict : Dictionary

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




#var _param : String
#	var _dir : Directory = Directory.new()
#	match action_to_do:
#		"close_menu":
#			menu_scene.create_exit_timer()
#		"load_stage":
#			_param = STAGES_PATH + STAGE_SCENES_PREFIX + action_parameter + ".tscn"
#			if _dir.file_exists(_param):
#				get_tree().current_scene.load_scene(_param, true)
#		"load_3dmenu":
#			_param = MENUS3D_PATH + MENU3D_SCENES_PREFIX + action_parameter + ".tscn"
#			if _dir.file_exists(_param):
#				get_tree().current_scene.load_scene(_param, true)
#		"load_2dmenu":
#			_param = MENUS2D_PATH + MENUS2D_SCENES_PREFIX + action_parameter + ".tscn"
#			if _dir.file_exists(_param):
#				get_tree().current_scene.load_scene(_param, true)
#		"quit_game":
#			get_tree().quit()


func select_object(_selected : bool):
	if _selected:
		self.grab_focus()

func _on_click_button():
	do_click_action()

