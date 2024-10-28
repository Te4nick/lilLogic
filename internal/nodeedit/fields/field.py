from .linkable import Linkable
from ..abc.field import FieldABC
from typing import Any, Callable

import dearpygui.dearpygui as dpg
from loguru import logger
import sys
logger.add(sys.stdout, colorize=True, format="<green>{time}</green> <level>{message}</level>")


class Field(Linkable, FieldABC):

    field_type = "Field"

    def __init__(self, tag: str, callback: Callable[..., Any]):
        super().__init__(tag, callback)



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

class FieldAttributeType:
    input: int = 0
    output: int = 1
    static: int = 2