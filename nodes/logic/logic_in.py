from internal.nodeedit import Node


class LogicIn(Node):

    node_type = "LogicIn"

    def build(self):
        self.add_output("Value", readonly=False)
