from internal.nodeedit import Node
from internal.nodeedit.fields import BoolField


class BinIn(Node):
    node_type = "BinIn"

    def build(self):
        self.add_field(
            BoolField(
                "Value", parent=self.alias, callback=self.calculate, attribute_type=1
            ),
        )
