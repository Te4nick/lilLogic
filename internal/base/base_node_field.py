import dearpygui.dearpygui as dpg
from typing import Any, Callable
from icecream import ic


class NodeField:

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
        self.callable_updates: dict[str: Callable] = {}  # List of other inputs update() methods

        self.dpg_attr: int | str = ""
        self.dpg_field: int | str = ""

    def __del__(self):
        dpg.delete_item(self.dpg_field)
        dpg.delete_item(self.dpg_attr)

    def __on_value_update(self):

        def value_changed(sender: Any = None, app_data: Any = None, user_data: Any = None):
            ic(self.parent + f"_{self.label}",
               self.callable_updates)

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
        # dpg.add_int_value()
        self.dpg_field = dpg.add_input_int(
            tag=self.parent + f"_{self.label}_Value",
            label=self.label,
            width=100,
            default_value=0,
            callback=self.__on_value_update(),
            parent=self.dpg_attr,
            readonly=self.readonly,
        )

    def update(self, value: int):
        self.value = value
        dpg.set_value(self.dpg_field, self.value)
        for update_call in self.callable_updates.values():
            update_call(value)

    def add_listener(self, item: int | str, listener: Callable):
        if item is int:
            item = dpg.get_item_label(item)
        self.callable_updates[item] = listener
        listener(self.value)

    def create_listener(self) -> Callable:
        def listener(v: int) -> None:
            self.update(v)
            self.callback()

        return listener

    def remove_listener(self, item: int | str) -> None:
        if item is int:
            item = dpg.get_item_label(item)
        self.callable_updates.pop(item)

    def destroy(self):
        del self.callable_updates
