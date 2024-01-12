import dearpygui.dearpygui as dpg
from typing import Any, Callable
from icecream import ic

from .linkable import Linkable


class NodeField(Linkable):

    def __init__(self,
                 label: str,
                 parent: int | str = None,
                 attribute_type: int = 0,
                 callback: Any | None = None,
                 readonly: bool = False,
                 user_data: dict[str, Any] = None,
                 ):
        super().__init__(callback)

        self.label = label
        self.parent = parent
        self.attribute_type = attribute_type
        self.readonly = readonly

        self.dpg_attr: int | str = ""
        self.dpg_field: int | str = ""

    def __del__(self):
        super().__del__()
        dpg.delete_item(self.dpg_field)
        dpg.delete_item(self.dpg_attr)

    def _on_set_value(self):
        dpg.set_value(self.dpg_field, self.value)

    def __on_value_changed(self):
        def value_changed(sender: Any = None, app_data: Any = None, user_data: Any = None):
            # ic(self.parent + f"_{self.label}",
            #    self.__links_to)
            self.receive_value(dpg.get_value(sender))

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
