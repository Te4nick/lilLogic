from icecream import ic

from internal.nodeedit import Node


class LogicAnd(Node):

    node_type = "LogicAnd"

    def build(self):
        self.add_input("Input 1")
        self.add_input("Input 2")
        self.add_output("Output")

    def calculate(self):
        result = self.get_field_value("Input 1")
        result = result & self.get_field_value("Input 2")
        self.set_field_value("Output", result)
