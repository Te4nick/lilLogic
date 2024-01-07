import dearpygui.dearpygui as dpg
from typing import Any, Callable
from icecream import ic

from internal.base.base_node_link import Link, Linkable


class NodeField(Linkable):

    def __init__(self,
                 label: str,
                 parent: int | str = None,
                 attribute_type: int = 0,
                 callback: Any | None = None,
                 readonly: bool = False,
                 user_data: dict[str, Any] = None,
                 ):
        self.label = label
        self.parent = parent
        self.attribute_type = attribute_type
        self.callback = callback
        self.readonly = readonly

        self.value: int = 0

        self.__links_to: dict[str: Link] = {}
        self.__links_from: dict[str: Link] = {}

        self.dpg_attr: int | str = ""
        self.dpg_field: int | str = ""

    def __del__(self):
        for link in self.__links_to.values():
            link.__del__()
        for link in self.__links_from.values():
            link.__del__()
        del self.__links_to
        del self.__links_from
        dpg.delete_item(self.dpg_field)
        dpg.delete_item(self.dpg_attr)

    def __on_value_changed(self):

        def value_changed(sender: Any = None, app_data: Any = None, user_data: Any = None):
            ic(self.parent + f"_{self.label}",
               self.__links_to)

            self.update(dpg.get_value(sender))
            self.callback()

        return value_changed

    def build(self, user_data: dict[str, Any] = None):
        if user_data is None:
            user_data = {}
        user_data["class"] = self
        self.dpg_attr = dpg.add_node_attribute(
            tag=self.parent + f"_{self.label}",
            user_data=user_data,
            attribute_type=self.attribute_type,
            parent=self.parent,
        )
        self.dpg_field = dpg.add_input_int(
            tag=self.parent + f"_{self.label}_Value",
            label=self.label,
            width=100,
            default_value=0,
            callback=self.__on_value_changed(),
            parent=self.dpg_attr,
            readonly=self.readonly,
        )

    def update(self, value: int):
        self.value = value
        dpg.set_value(self.dpg_field, self.value)
        for link in self.__links_to.values():
            link.send(value)

    def add_to_link(self, item: int | str, link: Link):
        self.__links_to[item] = link
        link.send(self.value)

    def delete_to_link(self, item: int | str):
        self.__links_to.pop(item)

    def add_from_link(self, item: int | str, link: Link):
        self.__links_from[item] = link

    def delete_from_link(self, item: int | str):
        self.__links_from.pop(item)

    def receive_value(self, value: Any):
        self.update(value)
        self.callback()
