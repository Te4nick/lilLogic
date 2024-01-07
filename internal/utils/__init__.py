from typing import Any
import dearpygui.dearpygui as dpg

__all__ = ["dpg2class"]


def dpg2class(item: int | str) -> Any:
    return dpg.get_item_user_data(item)["class"]
