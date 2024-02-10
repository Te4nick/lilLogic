from icecream import ic

from internal.nodeedit import Node
from internal.nodeedit.fields import BoolField


class DTrigger(Node):

    node_type = "D-Trigger"

    def build(self):
        d_in = BoolField(
            "D",
            parent=self.alias,
            callback=self.calculate,
            attribute_type=0
        )
        self.add_field("D", d_in)
        e_in = BoolField(
            "C",
            parent=self.alias,
            callback=self.calculate,
            attribute_type=0
        )
        self.add_field("C", e_in)
        q_out = BoolField(
            "Q",
            parent=self.alias,
            callback=self.calculate,
            attribute_type=1,
            readonly=True
        )
        self.add_field("Q", q_out)
        not_q_out = BoolField(
            "NOT Q",
            parent=self.alias,
            callback=self.calculate,
            attribute_type=1,
            readonly=True,
            default_value=True
        )
        self.add_field("NOT Q", not_q_out)
        self.__q = False

    def calculate(self):
        d = self.get_field_value("D")
        c = self.get_field_value("C")
        self.__q = d if c else self.__q
        self.set_field_value("Q", self.__q)
        self.set_field_value("NOT Q", not self.__q)
