from internal.nodeedit import Node
from internal.nodeedit.fields import IntField, BoolField


class Combiner(Node):
    node_type = "Combiner"

    def __on_bits_changed(self):
        bits = self.get_field_value("Bits")
        if bits < 2:
            self.set_field_value("Bits", 2)
            return

        if bits > self.__bits:
            self.__bits = bits
            self.set_field_value("Bits", bits)
            new_field = BoolField(
                f"X{bits - 1}",
                parent=self.alias,
                callback=self.calculate,
                attribute_type=0,
            )
            self.add_field(f"X{bits - 1}", new_field)
            new_field.build()
            return

        if bits < self.__bits:
            self.__bits = bits
            self.set_field_value("Bits", bits)
            self.delete_field(f"X{bits}")
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

        self.add_output("Y0")

        self.add_field(
            "X0",
            BoolField(
                "X0", parent=self.alias, callback=self.calculate, attribute_type=0
            ),
        )
        self.add_field(
            "X1",
            BoolField(
                "X1", parent=self.alias, callback=self.calculate, attribute_type=0
            ),
        )

    def calculate(self):
        result = 0
        for i in range(self.__bits):
            value = self.get_field_value(f"X{i}")
            result += value << i
        self.set_field_value("Y0", result)
