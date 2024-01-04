from nodes.base_node import Node, dpg


class LogicAnd(Node):

    node_type = "LogicAnd"

    def build(self):
        self.add_input("Input 1")
        self.add_input("Input 2")
        self.add_output("Output")

    def calculate(self):
        result = self.inputs["Input 1"]
        result = result & self.inputs["Input 2"]
        self.set_output_value("Output", result)
