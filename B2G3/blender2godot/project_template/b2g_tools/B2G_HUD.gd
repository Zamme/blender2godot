class_name B2G_HUD extends Control


onready var hud_message_label : Label = find_node("HudMessageLabel")
onready var hud_message_label_animator : AnimationPlayer = find_node("HudMessageLabelAnimationPlayer")
onready var hud_timer : Timer = find_node("b2g_hud_Timer")

var _showing_message : bool
var _pending_messages = []


func _ready():
	show_message("Debug hud enabled")

func show_message(_text):
	_pending_messages.append(_text)
	if _showing_message:
		pass
	else:
		_on_b2g_hud_Timer_timeout()

func _show_message(_text):
	_showing_message = true
	hud_message_label.text = _text
	hud_message_label.visible = true
	hud_message_label.modulate.a = 1.0
	hud_timer.start(2.0)

func _on_b2g_hud_Timer_timeout():
	hud_message_label_animator.play("fade_out")

func _on_HudMessageLabelAnimationPlayer_animation_finished(anim_name):
	hud_message_label.visible = false
	_showing_message = false
	if len(_pending_messages) > 0:
		_show_message(_pending_messages.pop_front())

