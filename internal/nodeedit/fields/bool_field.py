from .field import Field
import dearpygui.dearpygui as dpg
from typing import Any

from loguru import logger
import sys
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")


class BoolField(Field):
    def __init__(self,
                 label: str,
                 parent: int | str = None,
                 attribute_type: int = 0,
                 callback: Any | None = None,
                 readonly: bool = False,
                 user_data: dict[str, Any] = None,
                 ):
        super().__init__(parent + f"_{label}", callback)

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

    def _on_value_changed(self):
        dpg.set_value(self.dpg_field, bool(self.value))

    def __on_dpg_callback(self):
        def value_changed(sender: Any = None, app_data: Any = None, user_data: Any = None):
            # ic(self.parent + f"_{self.label}",
            #    self.__links_to)
            logger.debug(f"{self.tag}: __on_dpg_callback: value: {dpg.get_value(sender)}")
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
        self.dpg_field = dpg.add_checkbox(
            tag=self.parent + f"_{self.label}_Value",
            label=self.label,
            # width=100,
            default_value=False,
            callback=self.__on_dpg_callback(),
            parent=self.dpg_attr,
            # readonly=self.readonly,
        )
