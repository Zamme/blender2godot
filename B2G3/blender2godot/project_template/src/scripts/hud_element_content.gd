class_name HudElementContent extends Label


var node_info : Dictionary

var _source_node_properties
var current_value : String = ""

var is_variable : bool = false


func _ready():
	pass

func link_content(_gm_ref):
#	var _source_source_node
	var _source_node = _gm_ref.get_tree_node(node_info["SourceNodeName"], _gm_ref.gm_dict)
#	print(name, _source_node)
	self._source_node_properties = _source_node["NodeProperties"]
	if self._source_node_properties.has("value"):
		# FIXED VALUE
		self.current_value = str(_source_node_properties["value"])
	else:
		# ENTITY PROPERTY
		self.is_variable = true
#		self.current_ref.parse(str("No way"))
	print("Node properties: ", _source_node_properties)

func update_value():
	pass

func update_content():
	if self.is_variable:
		self.update_value()
	print("Updating content ", name)
	self.text = self.current_value
