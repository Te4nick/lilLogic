from uuid import uuid4
from typing import Any, Callable
import dearpygui.dearpygui as dpg
from internal.base.base_node_field import NodeField


class Node:
    node_type: str = "BaseNode"

    def __init__(self, user_data: dict[str, Any] = None):
        if user_data is None:
            user_data = {}
        self.tag = str(uuid4()) + "_" + self.node_type

        self.fields: dict[str, NodeField] = {}

        self.__build_node(user_data)
        self.build()
        self.__build_fields()

        self.calculate()

    def __del__(self):
        for field in self.fields.values():
            field.__del__()
        del self.fields
        dpg.delete_item(self.node)

    def __build_node(self, user_data):
        user_data["class"] = self
        self.node = dpg.add_node(
            tag=self.tag + "_Node",
            user_data=user_data,
            parent="NodeEditor",
            label=self.node_type,
            pos=user_data["pos"] if "pos" in user_data.keys() else [0, 0]
        )

    def __build_fields(self):
        for field in self.fields.values():
            field.build()

    # def __alias2id(self, alias):
    #     pass

    def calculate(self):
        pass

    def build(self):
        pass

    def add_input(self, label: str, readonly: bool = False):
        self.fields[label] = NodeField(label,
                                       self.node,
                                       dpg.mvNode_Attr_Input,
                                       self.calculate,
                                       readonly)

    def add_output(self, label: str, readonly: bool = True):
        self.fields[label] = NodeField(label,
                                       self.node,
                                       dpg.mvNode_Attr_Output,
                                       self.calculate,
                                       readonly)

    def add_static(self, label: str, readonly: bool = False):
        self.fields[label] = NodeField(label,
                                       self.node,
                                       dpg.mvNode_Attr_Static,
                                       self.calculate,
                                       readonly)

    def set_field_value(self, label: str, value: int):
        self.fields[label].update(value)

    def get_field_value(self, label) -> int:
        return self.fields[label].value

    def get_field(self, label) -> NodeField:
        return self.fields[label]

    def destroy(self):
        for field in self.fields.values():
            field.__del__()
        del self.fields
