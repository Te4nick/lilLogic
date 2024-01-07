from typing import Any

from internal.base.base_node import Node
from internal.node_importer.node_packages_importer import NodeImporter
import dearpygui.dearpygui as dpg
from icecream import ic


class NodeDB:
    def __init__(self, importer: NodeImporter):
        self.__nimport: NodeImporter = importer

        self.__node_map: dict[int | str, Node] = {}

    def add_node(self, package_name: str, node_name: str, user_data: dict[str: Any]):
        node = self.__nimport.get_node_class(package_name, node_name)(user_data)
        self.__node_map[dpg.get_alias_id(node.alias)] = node
        ic(self.__node_map)

    def get_node_packages_names(self):
        return self.__nimport.get_package_names()

    def get_package_nodes_names(self, package_name: str):
        return self.__nimport.get_package_nodes(package_name)

    def delete_node(self, node: int | str | Node):
        if node is str:
            node = dpg.get_alias_id(node)
        elif isinstance(node, Node):
            node = dpg.get_alias_id(node.alias)
        node = self.__node_map.pop(node)
        node.__del__()
        ic(self.__node_map)
