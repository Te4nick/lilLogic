import dearpygui.dearpygui as dpg
from typing import Any, Callable
from icecream import ic

from .field import Field
from internal.utils import logger


class IntField(Field):

    def __init__(
        self,
        label: str,
        parent: int | str = None,
        attribute_type: int = 0,
        callback: Any | None = None,
        readonly: bool = False,
        user_data: dict[str, Any] = None,
        default_value: int = 0,
    ):
        super().__init__(
            label=label,
            parent=parent,
            attribute_type=attribute_type,
            callback=callback,
            default_value=default_value,
        )

        self.readonly = readonly

        self.dpg_field: int | str = ""

    def __del__(self):
        super().__del__()
        dpg.delete_item(self.dpg_field)
        dpg.delete_item(self.dpg_attr)

    def _on_value_changed(self):
        dpg.set_value(self.dpg_field, self.value)

    def __on_dpg_callback(self):
        def value_changed(
            sender: Any = None, app_data: Any = None, user_data: Any = None
        ):
            logger.debug(
                f"{self.tag}: __on_dpg_callback: value: {dpg.get_value(sender)}"
            )
            self.receive_value(dpg.get_value(sender))

        return value_changed

    def build(self, user_data: dict[str, Any] = None):
        self.dpg_field = dpg.add_input_int(
            tag=self.tag + "_Value",
            label=self.label,
            width=100,
            default_value=0,
            callback=self.__on_dpg_callback(),
            parent=self.dpg_attr,
            readonly=self.readonly,
        )
