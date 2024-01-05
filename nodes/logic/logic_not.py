from internal.base.base_node import Node


class LogicNot(Node):

    node_type = "LogicNot"

    def build(self):
        self.add_input("Input")
        self.add_output("Output")

    def calculate(self):
        n = self.get_field_value("Input")
        shift = 1 if n == 0 else n.bit_length()
        result = n ^ ((1 << shift) - 1)
        self.set_field_value("Output", result)
