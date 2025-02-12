from internal.nodeedit import Node
from internal.nodeedit.fields import BoolField


class DTrigger(Node):

    node_type = "D-Trigger"

    def build(self):
        self.add_field(
            BoolField(
                "D",
                parent=self.alias,
                callback=self.calculate,
                attribute_type=0,
            ),
        )
        self.add_field(
            BoolField(
                "C",
                parent=self.alias,
                callback=self.calculate,
                attribute_type=0,
            ),
        )
        self.add_field(
            BoolField(
                "Q",
                parent=self.alias,
                callback=self.calculate,
                attribute_type=1,
                readonly=True,
            ),
        )
        self.add_field(
            BoolField(
                "NOT Q",
                parent=self.alias,
                callback=self.calculate,
                attribute_type=1,
                readonly=True,
                default_value=True,
            ),
        )
        self.__q = False

    def calculate(self):
        d = self.get_field_value("D")
        c = self.get_field_value("C")
        self.__q = d if c else self.__q
        self.set_field_value("Q", self.__q)
        self.set_field_value("NOT Q", not self.__q)
