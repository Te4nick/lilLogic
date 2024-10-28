from internal.nodeedit import Node
from internal.nodeedit.fields import IntField, BoolField


class Splitter(Node):
    node_type = "Splitter"

    def __on_bits_changed(self):
        bits = self.get_field_value("Bits")
        if bits < 2:
            self.set_field_value("Bits", 2)
            return

        if bits > self.__bits:
            self.__bits = bits
            self.set_field_value("Bits", bits)
            new_field = BoolField(
                f"Y{bits - 1}",
                parent=self.alias,
                callback=self.calculate,
                attribute_type=1,
            )
            self.add_field(f"Y{bits - 1}", new_field)
            new_field.build()
            return

        if bits < self.__bits:
            self.__bits = bits
            self.set_field_value("Bits", bits)
            self.delete_field(f"Y{bits}")
            return

    def build(self):
        self.__bits = 2
        self.add_field(
            "Bits",
            IntField(
                "Bits",
                parent=self.alias,
                callback=self.__on_bits_changed,
                attribute_type=2,
            ),
        )
        self.add_input("X0")
        self.add_field(
            "Y0",
            BoolField(
                "Y0", parent=self.alias, callback=self.calculate, attribute_type=1
            ),
        )
        self.add_field(
            "Y1",
            BoolField(
                "Y1", parent=self.alias, callback=self.calculate, attribute_type=1
            ),
        )

    def calculate(self):
        value = self.get_field_value("X0")

        for i in range(self.__bits):
            self.set_field_value(f"Y{i}", bool(value & (1 << i)))
