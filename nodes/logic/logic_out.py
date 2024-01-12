from internal.nodeedit import Node


class LogicOut(Node):

    node_type = "LogicOut"

    def build(self):
        self.add_input("Result", readonly=True)
