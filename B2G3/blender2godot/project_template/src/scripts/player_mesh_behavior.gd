class_name PlayerMesh extends Node


onready var animation_player : AnimationPlayer = find_node("AnimationPlayer")

export var _entity_properties : Dictionary


func _ready():
	pass

func _play_animation(_name):
	if animation_player.has_animation(_name):
		if animation_player.is_playing():
			if animation_player.current_animation != _name:
				animation_player.play(_name)
		else:
			animation_player.play(_name)
