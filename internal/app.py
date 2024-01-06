import os

import dearpygui.dearpygui as dpg
from internal.node_db import NodeDB
from internal.node_importer.node_packages_importer import NodeImporter

LastNodePosition = [100, 100]


# Destroy window if closed
def callback_close_window(sender):
    dpg.delete_item(sender)


class NodeEditor:
    def __init__(self):

        self.node_db = NodeDB()

        self.nimport = NodeImporter(os.path.join(os.getcwd(), "nodes"))

        with dpg.window(tag="NodeEditorWindow",
                        label="NodeEditor",
                        width=1000,
                        height=700,
                        pos=[50, 50],
                        menubar=True,
                        on_close=callback_close_window):
            # Add a menu bar to the window
            with dpg.menu_bar(label="MenuBar"):

                for package_name in self.nimport.get_package_names():
                    with dpg.menu(label=package_name):
                        for node_name in self.nimport.get_package_node_names(package_name):
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
                    callback=save_last_node_position
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
            link = dpg.add_node_link(app_data[0], app_data[1], parent=sender)
            self.node_db.register_link(link, app_data[0], app_data[1])

        return link_callback

    # callback runs when user attempts to disconnect attributes
    def __on_delink_callback(self):
        def delink_callback(sender, app_data):
            # app_data -> link_id
            dpg.delete_item(app_data)
            self.node_db.unregister_link(app_data)

        return delink_callback

    def __on_add_item_callback(self, package_name: str, node_name: str):
        def add_item_callback(sender):
            node = self.nimport.get_node_class(package_name, node_name)
            self.node_db.register_node(node())

        return add_item_callback

    def __on_delete_item_callback(self):
        def delete_item_callback(sender):
            # for selected_node in dpg.get_selected_nodes("NodeEditor"):
            #     # Deleting node and attached links
            #     ## Extract all children of the deleted node
            #     selected_node_children = dpg.get_item_children(selected_node)[1]
            #     ## Extract all existing links in the Node Editor
            #     node_editor_links = dpg.get_item_children("NodeEditor")[0]
            #     ## Iterate through NodeEditor elements and delete attached links
            #     for link in node_editor_links:
            #         if dpg.get_item_configuration(link)["attr_1"] in selected_node_children or \
            #                 dpg.get_item_configuration(link)["attr_2"] in selected_node_children:
            #             dpg.delete_item(link)
            #     ## Iterate trough LinkList and remove attached links
            #     for item in LinkList:
            #         for sub_item in item:
            #             if dpg.get_item_alias(selected_node) in sub_item:
            #                 LinkList.remove(item)
            #     # Deleting node
            #     dpg.delete_item(selected_node)
            # for selected_link in dpg.get_selected_links("NodeEditor"):
            #     func_link_destroyed("NodeEditor", selected_link)
            pass

        return delete_item_callback


# Saving the position of the last selected node
def save_last_node_position():
    global LastNodePosition
    if not dpg.get_selected_nodes("NodeEditor"):
        pass
    else:
        LastNodePosition = dpg.get_item_pos(dpg.get_selected_nodes("NodeEditor")[0])

