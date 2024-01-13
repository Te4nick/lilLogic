from internal.nodeedit import Node
from internal.nodeedit.fields import NodeField


class Mux4to2(Node):

    node_type = "4Mux2"

    def build(self):
        self.add_input("D0")
        self.add_input("D1")
        self.add_input("D2")
        self.add_input("D3")
        self.add_field("A0",
                       NodeField(
                           "A0",
                           parent=self.alias,
                           callback=self.calculate
                       ))
        self.add_output("Output")

    def calculate(self):
        a0 = self.get_field_value("A0")
        if not 0 <= a0 <= 3:
            a0 = 0
            self.set_field_value("A0", 0)

        result = self.get_field_value(f"D{a0}")
        self.set_field_value("Output", result)
