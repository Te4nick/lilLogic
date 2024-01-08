import dearpygui.dearpygui as dpg
from icecream import ic

from internal.managers import NodeImporter


class NodeSelector:
    def __init__(self, parent: int | str = None):
        self.__nimport = NodeImporter()

        with dpg.window(label='Node Selector',
                        pos=[10, 60],
                        width=300,
                        height=890) as node_selector:
            for package_name in self.__nimport.get_package_names():
                with dpg.tree_node(label=package_name,
                                   parent=node_selector,
                                   default_open=True,
                                   open_on_arrow=True):
                    for node_name in self.__nimport.get_package_node_names(package_name):
                        # with dpg.tree_node(label=node, parent=parent_id, default_open=True, id=node_id):
                        dpg.add_button(label=node_name,
                                       width=200,
                                       height=30,
                                       callback=self.__on_add_node(package_name, node_name))

    def __on_add_node(self, package_name: str, node_name: str):
        def on_add_node(sender, app_data):
            ic("Entering __on_add_node", package_name, node_name)
            node_class = self.__nimport.get_node_class(package_name, node_name)
            node_class()
        return on_add_node
