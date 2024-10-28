from internal.nodeedit import Node
from internal.nodeedit.fields import BoolField


class BinOut(Node):
    node_type = "BinOut"

    def build(self):
        self.add_field(
            "Result",
            BoolField(
                "Result", parent=self.alias, callback=self.calculate, attribute_type=0
            ),
        )
