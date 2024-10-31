from uuid import uuid4, UUID
from typing import Any
import dearpygui.dearpygui as dpg
from icecream import ic
from pydantic import BaseModel

from .fields import Field, FieldData
from .fields import IntField


class NodeData(BaseModel):
    package: str
    node_type: str
    id: UUID
    position: list[int]
    fields: list[FieldData]


class Node:
    node_type: str = "BaseNode"
    package: str = __module__.split(".")[0]

    def __init__(
        self,
        id: UUID | None = None,
        parent: int | str = 0,
        user_data: dict[str, Any] = None,
    ):
        if user_data is None:
            user_data = {}

        if id is None:
            self.__id = uuid4()
        else:
            self.__id = id

        self.package = self.__module__.split(".")[0]
        self.__fields: dict[str, Field] = {}

        self.__build_node(user_data)
        self.build()
        self.__build_fields()

        self.calculate()

    def __del__(self):
        for field in self.__fields.values():
            field.__del__()
        del self.__fields
        dpg.delete_item(self.alias)

    def __build_node(self, user_data: dict[str, Any]):
        user_data["class"] = self
        self.alias = dpg.add_node(
            tag=str(self.__id) + "_" + self.node_type + "_Node",  # Unique node alias
            user_data=user_data,
            parent="NodeEditor",
            label=self.node_type,
            pos=user_data["pos"] if "pos" in user_data.keys() else [0, 0],
        )
        ic(dpg.get_item_user_data(self.alias))
        ic(f"Building {self.alias}")

    def __build_fields(self):
        for field in self.__fields.values():
            field.build()

    @classmethod
    def from_data(cls, data: NodeData, parent: int | str = 0) -> "Node":
        cls.package = cls.__module__.split(".")[0]
        if data.package != cls.package or data.node_type != cls.node_type:
            raise ValueError(
                f"expected: package={cls.package}, node_type={cls.node_type}, got package={data.package}, node_type={data.node_type}"
            )

        node: Node = cls(id=data.id, parent=parent, user_data={"pos": data.position})
        for field in data.fields:
            node.set_field_value(field.label, field.value)

    def calculate(self):
        pass

    def build(self):
        pass

    def add_input(self, label: str, readonly: bool = False):
        self.__fields[label] = IntField(
            label, self.alias, dpg.mvNode_Attr_Input, self.calculate, readonly
        )

    def add_output(self, label: str, readonly: bool = True):
        self.__fields[label] = IntField(
            label, self.alias, dpg.mvNode_Attr_Output, self.calculate, readonly
        )

    def add_static(self, label: str, readonly: bool = False):
        self.__fields[label] = IntField(
            label, self.alias, dpg.mvNode_Attr_Static, self.calculate, readonly
        )

    def set_field_value(self, label: str, value: int):
        self.__fields[label].set_value(value)

    def get_field_value(self, label) -> int:
        return self.__fields[label].get_value()

    def add_field(self, label: str, field: Field):
        self.__fields[label] = field
        ic(self.__fields)

    def get_field(self, item: int | str) -> Field:
        label = item
        if item is int:
            label = dpg.get_item_label(item)
        return self.__fields[label]

    def delete_field(self, label) -> bool:
        field = self.__fields[label]
        if field:
            self.__fields.pop(label)
            field.__del__()
            return True
        return False

    def serialize(self) -> NodeData:
        fields: list[FieldData] = []
        for field in self.__fields.values():
            fields.append(field.serialize())
        return NodeData(
            package=self.package,
            node_type=self.node_type,
            id=self.__id,
            position=dpg.get_item_pos(self.alias),
            fields=fields,
        )
