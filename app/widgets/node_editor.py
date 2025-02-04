import dearpygui.dearpygui as dpg
from icecream import ic

from internal.nodeedit import NodeLink, Node, NodeLinkData
from internal.managers import SaveData
from internal.utils import dpg2class


# Destroy window if closed
def callback_close_window(sender):
    dpg.delete_item(sender)


class NodeEditor:
    def __init__(self, parent):
        self.__last_node_pos = [0, 0]

        self.__init_window(parent)

    def __init_window(self, parent):
        # Add node editor to the window
        self.dpg_node_editor = dpg.add_node_editor(
            parent=parent,
            tag="NodeEditor",
            minimap=True,
            minimap_location=dpg.mvNodeMiniMap_Location_BottomLeft,
            # Function call for updating all nodes if a new link is created
            callback=self.__on_link_callback,
            # Function call for updating if a link is destroyed
            delink_callback=self.__on_delink_callback,
            user_data={"class": self},
        )

        with dpg.handler_registry():
            dpg.add_mouse_click_handler(callback=self.__on_save_last_node_position)

        with dpg.handler_registry():
            dpg.add_key_release_handler(
                key=dpg.mvKey_Delete, callback=self.__on_delete_item_callback
            )

    # End note editor
    @staticmethod
    def __on_link_callback(_, app_data):
        NodeLink(app_data[0], app_data[1], parent="NodeEditor")
        pass

    @staticmethod
    def __on_delink_callback(_, app_data):  # app_data -> link_id
        ic(app_data)
        dpg2class(app_data).__del__()
        pass

    @staticmethod
    def __on_delete_item_callback(_):
        for selected_link in dpg.get_selected_links("NodeEditor"):
            ic(dpg.get_item_label(selected_link))
            dpg2class(selected_link).__del__()
        for selected_node in dpg.get_selected_nodes("NodeEditor"):
            ic(dpg.get_item_label(selected_node))
            dpg2class(selected_node).__del__()
            # ic(self.__node_links)

    def __on_save_last_node_position(self):
        if dpg.get_selected_nodes("NodeEditor"):
            self.__last_node_pos = dpg.get_item_pos(
                dpg.get_selected_nodes("NodeEditor")[0]
            )

    def clear_canvas(self) -> None:
        children = dpg.get_item_children(
            self.dpg_node_editor
        )  # {0: links, 1: nodes, 2: ..., 3: ...}
        print(children)
        for i in range(len(children[0])):
            link: NodeLink = dpg2class(children[0][i])
            print(link)
            link.__del__()
        for i in range(len(children[1])):
            node: Node = dpg2class(children[1][i])
            print(node)
            node.__del__()

    def get_nodes_data(self) -> SaveData:
        children = dpg.get_item_children(
            self.dpg_node_editor
        )  # {0: links, 1: nodes, 2: ..., 3: ...}
        nodes: list[dict] = []
        links: list[dict] = []
        for i in range(len(children[1])):
            node: Node = dpg2class(children[1][i])
            nodes.append(node.serialize())
        for i in range(len(children[0])):
            link: NodeLink = dpg2class(children[0][i])
            links.append(link.serialize())
        return SaveData(nodes=nodes, links=links)

    def create_links(self, links: list[NodeLinkData]) -> None:
        for link in links:
            NodeLink(link.from_field, link.to_field, parent="NodeEditor")
