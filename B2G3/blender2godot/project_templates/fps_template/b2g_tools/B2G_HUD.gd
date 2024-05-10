class_name B2G_HUD extends Control


onready var hud_message_label : Label = find_node("HudMessageLabel")
onready var hud_timer : Timer = find_node("b2g_hud_Timer")


func _ready():
	pass

func show_message(_text):
	hud_message_label.visible = true
	hud_message_label.text = _text
	hud_timer.start(5.0)

func _on_b2g_hud_Timer_timeout():
	hud_message_label.visible = false
