class_name PlayerMesh extends Node


onready var animation_player : AnimationPlayer = find_node("AnimationPlayer")


func _ready():
	print("Animation player found: ", animation_player.name)

func _test_anim():
	animation_player.play("run-loop")
