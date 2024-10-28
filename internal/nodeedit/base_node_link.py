import dearpygui.dearpygui as dpg
from typing import Any
from internal.nodeedit.abc.link import Link
from internal.nodeedit.abc.linkableabc import LinkableABC
from internal.utils import dpg2class


class NodeLink(Link):
    def __init__(
        self, from_attr: int | str, to_attr: int | str, parent: int | str = None
    ):
        self.__from_attr = from_attr
        self.__to_attr = to_attr

        self.__from_field: LinkableABC = dpg2class(from_attr)
        self.__to_field: LinkableABC = dpg2class(to_attr)

        self.__from_field.add_link(self.__to_attr, self, True)
        self.__to_field.add_link(self.__from_attr, self, False)

        self.__dpg_node_link = dpg.add_node_link(
            from_attr, to_attr, user_data={"class": self}, parent=parent
        )

    def __del__(self):
        self.__from_field.delete_link(self.__to_attr, True)
        self.__to_field.delete_link(self.__from_attr, False)
        dpg.delete_item(self.__dpg_node_link)

    def send(self, value: Any):
        self.__to_field.receive_value(value)

    def get_dpg(self) -> int | str:
        return self.__dpg_node_link
