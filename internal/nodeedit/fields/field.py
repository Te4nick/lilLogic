from .linkable import Linkable
from ..abc.field import FieldABC

from typing import Any, Callable

import dearpygui.dearpygui as dpg
from loguru import logger
from pydantic import BaseModel
import sys

logger.add(
    sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>"
)


class FieldData(BaseModel):
    label: str
    value: Any


class Field(Linkable, FieldABC):

    field_type = "Field"

    def __init__(
        self,
        label: str,
        parent: int | str = None,
        attribute_type: int = 0,
        callback: Callable[..., Any] = None,
        default_value: Any = None,
    ):
        super().__init__(parent + f"_{label}", callback)

        self.label = label
        self.parent = parent
        self.value = default_value

        self.dpg_attr = dpg.add_node_attribute(
            tag=self.tag,
            user_data={"class": self},
            attribute_type=attribute_type,
            parent=parent,
        )

    def _on_value_changed(self):
        pass

    def _on_receive_value(self):
        self._on_value_changed()

    def set_value(self, value: Any):
        logger.debug(f"{self.tag}: setting value: {value}; self.value: {self.value}")
        if value != self.value:
            self.value = value
            self.send_value()
            self._on_value_changed()

    def get_value(self) -> Any:
        return self.value

    def build(self):
        pass

    def serialize(self) -> FieldData:
        return FieldData(
            label=self.label,
            value=self.value,
        )


class FieldAttributeType:
    input: int = 0
    output: int = 1
    static: int = 2
