import dearpygui.dearpygui as dpg
from nodes.logic_and import LogicAnd
from nodes.logic_out import LogicOut
from nodes.logic_in import LogicIn
from nodes.base_node import Node


class NodeDB:
    def __init__(self):
        self.__node_map: dict[int | str, Node] = {}
        self.__link_map: dict[int | str, tuple[int, int]] = {}

    def get_parent_node(self, item_id: int | str) -> Node:
        return self.__node_map[dpg.get_item_parent(item_id)]

    def register_node(self, node: Node):
        self.__node_map[dpg.get_alias_id(node.alias)] = node

    def register_link(self, link_id: int, from_attr_id: int, to_attr_id: int):
        self.__link_map[link_id] = (
            from_attr_id,
            to_attr_id
        )

        self.get_parent_node(from_attr_id).add_output_link(
            from_attr_id + 1,
            to_attr_id + 1
        )

    def unregister_link(self, link_id: int):
        from_attr_id, to_attr_id = self.__link_map[link_id]
        self.get_parent_node(from_attr_id).delete_output_link(
            from_attr_id + 1,
            to_attr_id + 1
        )



if __name__ == "__main__":  # TODO: extract to App.py ?

    node_db = NodeDB()

    dpg.create_context()

    # callback runs when user attempts to connect attributes
    def link_callback(sender, app_data):  # TODO: mass callback refactor
        # app_data -> (link_id1, link_id2)
        link = dpg.add_node_link(app_data[0], app_data[1], parent=sender)
        node_db.register_link(link, app_data[0], app_data[1])
        # print({"link_id1": app_data[0], "link_id2": app_data[1]})
        # print({"link_id1_parent": dpg.get_item_parent(app_data[0]),
        #        "link_id2_parent": dpg.get_item_parent(app_data[1])})
        # dpg.get_item_user_data(dpg.get_item_parent(app_data[0]))["class"].add_output_link(app_data[0], app_data[1])

    # callback runs when user attempts to disconnect attributes
    def delink_callback(sender, app_data):
        # app_data -> link_id
        dpg.delete_item(app_data)
        node_db.unregister_link(app_data)


    with dpg.window(label="Tutorial", width=400, height=400):
        with dpg.node_editor(tag="NodeEditor", callback=link_callback, delink_callback=delink_callback):
            # with dpg.node(label="Node 1"):
            #     with dpg.node_attribute(label="Node A1"):
            #         dpg.add_input_int(label="F1", width=150)
            #
            #     with dpg.node_attribute(label="Node A2", attribute_type=dpg.mvNode_Attr_Output):
            #         dpg.add_input_int(label="F2", width=150)
            #
            # with dpg.node(label="Node 2"):
            #     with dpg.node_attribute(label="Node A3"):
            #         dpg.add_input_int(label="F3", width=200)
            #
            #     with dpg.node_attribute(label="Node A4", attribute_type=dpg.mvNode_Attr_Output):
            #         dpg.add_input_int(label="F4", width=200)

            node_db.register_node(LogicAnd())
            node_db.register_node(LogicAnd())
            node_db.register_node(LogicOut())
            node_db.register_node(LogicIn())

    dpg.create_viewport(title='Custom Title', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.show_item_registry()
    dpg.start_dearpygui()
    dpg.destroy_context()