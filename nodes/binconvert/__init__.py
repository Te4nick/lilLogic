from icecream import ic

from internal.nodeedit import Node
from internal.nodeedit.fields import IntField, BoolField


__all__ = ["Splitter", "Combiner"]


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
                attribute_type=1
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
        self.add_field("Bits",
                       IntField(
                           "Bits",
                           parent=self.alias,
                           callback=self.__on_bits_changed,
                           attribute_type=2
                       ))
        self.add_input("X0")
        self.add_field("Y0", BoolField(
            "Y0",
            parent=self.alias,
            callback=self.calculate,
            attribute_type=1
        ))
        self.add_field("Y1", BoolField(
            "Y1",
            parent=self.alias,
            callback=self.calculate,
            attribute_type=1
        ))

    def calculate(self):
        value = self.get_field_value("X0")

        for i in range(self.__bits):
            self.set_field_value(f"Y{i}", bool(value & (1 << i)))


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
                attribute_type=0
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
        self.add_field("Bits",
                       IntField(
                           "Bits",
                           parent=self.alias,
                           callback=self.__on_bits_changed,
                           attribute_type=2
                       ))

        self.add_output("Y0")

        self.add_field("X0", BoolField(
            "X0",
            parent=self.alias,
            callback=self.calculate,
            attribute_type=0
        ))
        self.add_field("X1", BoolField(
            "X1",
            parent=self.alias,
            callback=self.calculate,
            attribute_type=0
        ))

    def calculate(self):
        result = 0
        for i in range(self.__bits):
            value = self.get_field_value(f"X{i}")
            result += value << i
            ic(f"COMBINER FIELD: X{i}")
            ic(f"comb value: {value}")
            ic(f"result: {result}")
        self.set_field_value("Y0", result)
