from uuid import uuid4
from typing import Any, Callable
import dearpygui.dearpygui as dpg
from icecream import ic

from internal.base.base_node_field import NodeField


class Node:
    node_type: str = "BaseNode"

    def __init__(self, user_data: dict[str, Any] = None):
        if user_data is None:
            user_data = {}

        self.__fields: dict[str, NodeField] = {}

        self.__build_node(user_data)
        self.build()
        self.__build_fields()

        self.calculate()

    def __del__(self):
        for field in self.__fields.values():
            field.__del__()
        del self.__fields
        dpg.delete_item(self.alias)

    def __build_node(self, user_data):
        user_data["class"] = self
        self.alias = dpg.add_node(
            tag=str(uuid4()) + "_" + self.node_type + "_Node",  # Unique node alias
            user_data=user_data,
            parent="NodeEditor",
            label=self.node_type,
            pos=user_data["pos"] if "pos" in user_data.keys() else [0, 0]
        )
        ic(dpg.get_item_user_data(self.alias))

    def __build_fields(self):
        for field in self.__fields.values():
            field.build()

    # def __alias2id(self, alias):
    #     pass

    def calculate(self):
        pass

    def build(self):
        pass

    def add_input(self, label: str, readonly: bool = False):
        self.__fields[label] = NodeField(label,
                                         self.alias,
                                         dpg.mvNode_Attr_Input,
                                         self.calculate,
                                         readonly)

    def add_output(self, label: str, readonly: bool = True):
        self.__fields[label] = NodeField(label,
                                         self.alias,
                                         dpg.mvNode_Attr_Output,
                                         self.calculate,
                                         readonly)

    def add_static(self, label: str, readonly: bool = False):
        self.__fields[label] = NodeField(label,
                                         self.alias,
                                         dpg.mvNode_Attr_Static,
                                         self.calculate,
                                         readonly)

    def set_field_value(self, label: str, value: int):
        self.__fields[label].update(value)

    def get_field_value(self, label) -> int:
        return self.__fields[label].value

    def get_field(self, item: int | str) -> NodeField:
        label = item
        if item is int:
            label = dpg.get_item_label(item)
        return self.__fields[label]
