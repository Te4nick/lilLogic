from internal.base.base_node import Node
from internal.base.base_node_field import NodeField

import dearpygui.dearpygui as dpg


def get_parent_node(item: int | str) -> Node | None:
    ud = dpg.get_item_user_data(item)
    if ud is not dict:
        return None

    if "class" not in ud:
        return None

    if isinstance(ud["class"], Node):
        return ud["class"]

    elif isinstance(ud["class"], NodeField):
        parent_ud = dpg.get_item_user_data(dpg.get_item_parent(item))

        if parent_ud is not dict:
            return None

        if "class" not in parent_ud:
            return None

        if isinstance(parent_ud["class"], Node):
            return parent_ud["class"]
