from nodes.base_node import Node


class LogicIn(Node):

    node_type = "LogicIn"

    def build(self):
        self.add_output("Value", readonly=False)
