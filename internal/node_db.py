from internal.base.base_node import Node
import dearpygui.dearpygui as dpg


class NodeDB:
    def __init__(self):
        self.__node_map: dict[int | str, Node] = {}
        self.__link_map: dict[int | str, tuple[int, int]] = {}

    def get_parent_node(self, item_id: int | str) -> Node:
        return self.__node_map[dpg.get_item_parent(item_id)]

    def register_node(self, node: Node):
        self.__node_map[dpg.get_alias_id(node.node)] = node

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

    def unregister_link(self, link_id: int):
        from_attr_id, to_attr_id = self.__link_map[link_id]
        (self.get_parent_node(from_attr_id)
             .get_field(dpg.get_item_label(from_attr_id + 1))
             .remove_listener(to_attr_id + 1)
         )
