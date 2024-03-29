import dearpygui.dearpygui as dpg
from typing import Any
from internal.nodeedit.abc.link import Link
from internal.nodeedit.abc.linkableabc import LinkableABC


class NodeLink(Link):
    def __init__(self,
                 from_attr: int | str,
                 to_attr: int | str,
                 parent: int | str = None):
        self.__from_attr = from_attr
        self.__to_attr = to_attr

        self.__from_field: LinkableABC = dpg.get_item_user_data(from_attr)["class"]
        self.__to_field: LinkableABC = dpg.get_item_user_data(to_attr)["class"]

        self.__from_field.add_link(self.__to_attr, self, True)
        self.__to_field.add_link(self.__from_attr, self, False)

        self.__dpg_node_link = dpg.add_node_link(from_attr,
                                                 to_attr,
                                                 user_data={"class": self},
                                                 parent=parent)

    def __del__(self):
        self.__from_field.delete_link(self.__to_attr, True)
        self.__to_field.delete_link(self.__from_attr, False)
        dpg.delete_item(self.__dpg_node_link)

    def send(self, value: Any):
        self.__to_field.receive_value(value)
