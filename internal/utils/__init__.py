from typing import Any
import dearpygui.dearpygui as dpg

__all__ = ["dpg2class", "get_dpg_value"]


def dpg2class(item: int | str) -> Any:
    return dpg.get_item_user_data(item)["class"]


def get_dpg_value(item: int | str) -> Any:
    return dpg.get_value(item)
