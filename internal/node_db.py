from internal.base.base_node import Node
import dearpygui.dearpygui as dpg
from icecream import ic


class NodeDB:
    def __init__(self):
        self.__node_map: dict[int | str, Node] = {}
        self.__link_map: dict[int | str, tuple[int, int]] = {}

    def get_parent_node(self, item_id: int | str) -> Node:
        return self.__node_map[dpg.get_item_parent(item_id)]

    def register_node(self, node: Node):
        self.__node_map[dpg.get_alias_id(node.node)] = node
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
