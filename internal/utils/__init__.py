from typing import Any
import dearpygui.dearpygui as dpg
from .logger import LLLog

__all__ = ["LLLog", "dpg2class", "get_dpg_value"]


def dpg2class(item: int | str) -> Any:
    return dpg.get_item_user_data(item)["class"]


def get_dpg_value(item: int | str) -> Any:
    return dpg.get_value(item)
