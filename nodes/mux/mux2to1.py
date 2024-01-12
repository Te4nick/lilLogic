from internal.nodeedit import Node
from internal.nodeedit.fields import BoolField


class Mux2to1(Node):

    node_type = "2Mux1"

    def build(self):
        self.add_input("D0")
        self.add_input("D1")
        self.add_field("A0",
                       BoolField(
                           "A0",
                           parent=self.alias,
                           callback=self.calculate
                       ))
        self.add_output("Output")

    def calculate(self):
        d0 = self.get_field_value("D0")
        d1 = self.get_field_value("D1")
        a0 = self.get_field_value("A0")

        result = d0 if not a0 else d1
        self.set_field_value("Output", result)
