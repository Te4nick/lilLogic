import os

import dearpygui.dearpygui as dpg
from icecream import ic

from internal.nodeedit import NodeLink, Node
from internal.managers import SaveMan
from internal.utils import dpg2class


# Destroy window if closed
def callback_close_window(sender):
    dpg.delete_item(sender)


class NodeEditor:
    def __init__(self):
        self.__last_node_pos = [0, 0]

        self.__init_window()
    
    def print_children(self) -> None:
        children = dpg.get_item_children(self.dpg_node_editor) # {0: links, 1: nodes, 2: ..., 3: ...}
        print(SaveMan.dump_nodes(children[1]))
        

    def __init_window(self):
        with dpg.window(tag="NodeEditorWindow",
                        label="NodeEditor",
                        width=1000,
                        height=700,
                        pos=[50, 50],
                        menubar=True,
                        on_close=callback_close_window):

            with dpg.group(horizontal=True):
                dpg.add_text("Status:")
                dpg.add_text(tag="InfoBar")

            # Add node editor to the window
            self.dpg_node_editor = dpg.add_node_editor(
                    tag="NodeEditor",
                    # Function call for updating all nodes if a new link is created
                    callback=self.__on_link_callback(),
                    # Function call for updating if a link is destroyed
                    delink_callback=self.__on_delink_callback()
            )

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
            NodeLink(app_data[0], app_data[1], parent="NodeEditor")
            #ic(self.__node_links)

        return link_callback

    # callback runs when user attempts to disconnect attributes
    def __on_delink_callback(self):
        def delink_callback(sender, app_data):
            # app_data -> link_id
            ic(app_data)
            dpg2class(app_data).__del__()
            #ic(self.__node_links)

        return delink_callback

    def __on_delete_item_callback(self):
        def delete_item_callback(sender):
            for selected_node in dpg.get_selected_nodes("NodeEditor"):
                ic(dpg.get_item_label(selected_node))
                dpg2class(selected_node).__del__()
                #ic(self.__node_links)

        return delete_item_callback

    def __on_save_last_node_position(self):
        if dpg.get_selected_nodes("NodeEditor"):
            self.__last_node_pos = dpg.get_item_pos(dpg.get_selected_nodes("NodeEditor")[0])
