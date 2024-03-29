import os

import dearpygui.dearpygui as dpg
from icecream import ic

from internal.managers import NodeLinker, NodeImporter
from internal.utils import dpg2class


# Destroy window if closed
def callback_close_window(sender):
    dpg.delete_item(sender)


class NodeEditor:
    def __init__(self):

        self.__last_node_pos = [0, 0]

        self.nimport = NodeImporter(os.path.join(os.getcwd(), "nodes"))

        # self.node_db = NodeDB(nimport)

        with dpg.window(tag="NodeEditorWindow",
                        label="NodeEditor",
                        width=1000,
                        height=700,
                        pos=[50, 50],
                        menubar=True,
                        on_close=callback_close_window):
            # Add a menu bar to the window
            with dpg.menu_bar(label="MenuBar"):

                for package_name in self.nimport.get_node_packages():
                    with dpg.menu(label=package_name):
                        for node_name in self.nimport.get_package_nodes(package_name):
                            dpg.add_menu_item(tag=f"Menu_AddNode_{node_name}",
                                              label=node_name,
                                              callback=self.__on_add_item_callback(package_name, node_name),
                                              user_data=node_name)

            with dpg.group(horizontal=True):
                dpg.add_text("Status:")
                dpg.add_text(tag="InfoBar")

            # Add node editor to the window
            with dpg.node_editor(
                    tag="NodeEditor",
                    # Function call for updating all nodes if a new link is created
                    callback=self.__on_link_callback(),
                    # Function call for updating if a link is destroyed
                    delink_callback=self.__on_delink_callback()
            ):
                pass

            with dpg.handler_registry():
                dpg.add_mouse_click_handler(
                    callback=self.__on_save_last_node_position
                )

            with dpg.handler_registry():
                dpg.add_key_release_handler(
                    key=dpg.mvKey_Delete,
                    callback=self.__on_delete_item_callback()
                )
        # End note editor

    def __on_link_callback(self):
        def link_callback(sender, app_data):
            # app_data -> (link_id1, link_id2)
            NodeLinker.link(app_data[0], app_data[1], parent="NodeEditor")

        return link_callback

    # callback runs when user attempts to disconnect attributes
    def __on_delink_callback(self):
        def delink_callback(sender, app_data):
            # app_data -> link_id
            NodeLinker.unlink(app_data)

        return delink_callback

    def __on_add_item_callback(self, package_name: str, node_name: str):
        def add_item_callback(sender):
            node_class = self.nimport.get_node_class(package_name, node_name)
            node_class(user_data={"pos": self.__last_node_pos})

        return add_item_callback

    def __on_delete_item_callback(self):
        def delete_item_callback(sender):
            for selected_node in dpg.get_selected_nodes("NodeEditor"):
                ic(dpg.get_item_label(selected_node))
                dpg2class(selected_node).__del__()

        return delete_item_callback

    def __on_save_last_node_position(self):
        if dpg.get_selected_nodes("NodeEditor"):
            self.__last_node_pos = dpg.get_item_pos(dpg.get_selected_nodes("NodeEditor")[0])
