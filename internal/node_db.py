from typing import Any

from internal.base.base_node import Node
from internal.node_importer.node_packages_importer import NodeImporter
import dearpygui.dearpygui as dpg
from icecream import ic


class NodeDB:
    def __init__(self, importer: NodeImporter):
        self.__nimport: NodeImporter = importer

        self.__node_map: dict[int | str, Node] = {}
        self.__link_map: dict[int | str, tuple[int, int]] = {}

    def add_node(self, package_name: str, node_name: str, user_data: dict[str: Any]):
        self.register_node(self.__nimport.get_node_class(
            package_name, node_name
        )(user_data))

    def get_parent_node(self, item_id: int | str) -> Node:
        return self.__node_map[dpg.get_item_parent(item_id)]

    def get_node_packages_names(self):
        return self.__nimport.get_package_names()

    def get_package_nodes_names(self, package_name: str):
        return self.__nimport.get_package_nodes(package_name)

    def delete_node(self, node: int | str | Node):
        if node is str:
            node = dpg.get_alias_id(node)
        elif isinstance(node, Node):
            node = dpg.get_alias_id(node.alias)
        node = self.unregister_node(node)
        node.__del__()

    def register_node(self, node: Node):
        self.__node_map[dpg.get_alias_id(node.alias)] = node
        ic(self.__node_map)

    def register_link(self, link_id: int, from_attr_id: int, to_attr_id: int):
        self.__link_map[link_id] = (
            from_attr_id,
            to_attr_id
        )

        (self.get_parent_node(from_attr_id)
            .get_field(dpg.get_item_label(from_attr_id + 1))
            .add_listener(
                to_attr_id + 1,
                self.get_parent_node(to_attr_id)
                .get_field(dpg.get_item_label(to_attr_id + 1))
                .create_listener()
            )
         )

    def unregister_node(self, node_id: int) -> Node:
        for link_id in set(self.__link_map.keys()):
            ic(self.__link_map)
            from_attr_id, to_attr_id = self.__link_map[link_id]
            ic(node_id,
               dpg.get_item_label(node_id),
               from_attr_id,
               to_attr_id,
               dpg.get_item_parent(from_attr_id),
               dpg.get_item_parent(to_attr_id))
            if (dpg.get_item_parent(from_attr_id) == node_id or
                    dpg.get_item_parent(to_attr_id) == node_id):
                self.unregister_link(link_id)

        ic(self.__link_map)

        node = self.__node_map.pop(node_id)
        ic(self.__node_map)
        return node

    def unregister_link(self, link_id: int):
        from_attr_id, to_attr_id = self.__link_map.pop(link_id)
        (self.get_parent_node(from_attr_id)
             .get_field(dpg.get_item_label(from_attr_id + 1))
             .remove_listener(to_attr_id + 1)
         )
