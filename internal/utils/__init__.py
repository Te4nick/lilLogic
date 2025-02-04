from typing import Any
import dearpygui.dearpygui as dpg
from .logger import logger

__all__ = ["logger", "dpg2class", "get_dpg_value"]


def dpg2class(item: int | str) -> Any:
    return dpg.get_item_user_data(item)["class"]


def dpg2id(item: int | str) -> int:
    if isinstance(item, str):
        return dpg.get_alias_id(item)
    return item


def dpg2label(item: int | str) -> int:
    if isinstance(item, int):
        return dpg.get_item_label(item)
    return item


def get_dpg_value(item: int | str) -> Any:
    return dpg.get_value(item)
