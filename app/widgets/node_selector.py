import dearpygui.dearpygui as dpg
from icecream import ic

from internal.managers import NodeImporter
from internal.nodeedit import Node, NodeData


class NodeSelector:
    def __init__(self, parent: int | str = None):
        self.__nimport = NodeImporter()

        self.__build(parent)
        self.__build_node_tree()

    def __on_add_node(self, package_name: str, node_name: str):
        def on_add_node(sender, app_data):
            ic("Entering __on_add_node", package_name, node_name)
            node_class: Node = self.__nimport.get_node_class(package_name, node_name)
            node_class()

        return on_add_node

    def __on_rescan(self):
        def on_rescan(sender, app_data):
            self.__nimport = NodeImporter()
            dpg.delete_item(self.__node_window, children_only=True)
            self.__build_node_tree()

        return on_rescan

    def __build(self, parent=None):
        self.__window = dpg.add_child_window(
            tag="NodeSelector",
            parent=parent,
            menubar=True,
            border=False,
            user_data={"class": self},
        )

        with dpg.menu_bar(parent=self.__window):
            dpg.add_menu_item(label="Rescan", callback=self.__on_rescan())

        # menu_bar = dpg.add_tab_bar(label="Node Selector MenuBar", parent=self.__window)
        # dpg.add_tab_button(
        #     tag=f"Menu_Rescan",
        #     label="Rescan",
        #     parent=menu_bar,
        #     callback=self.__on_rescan(),
        # )
        self.__node_window = dpg.add_child_window(
            label="Nodes", parent=self.__window, border=False
        )

    def __build_node_tree(self):
        for package_name in self.__nimport.get_package_names():
            with dpg.tree_node(
                label=package_name,
                parent=self.__node_window,
                default_open=True,
                open_on_arrow=True,
            ):
                for node_name in self.__nimport.get_package_node_names(package_name):
                    # with dpg.tree_node(label=node, parent=parent_id, default_open=True, id=node_id):
                    dpg.add_button(
                        label=node_name,
                        width=200,
                        height=30,
                        callback=self.__on_add_node(package_name, node_name),
                    )

    def add_from_data(self, nodes_data: list[NodeData]) -> None:
        for node_data in nodes_data:
            node: Node = self.__nimport.get_node_class(
                node_data.package,
                node_data.node_type,
            )
            print(node)
            node.from_data(node_data)
