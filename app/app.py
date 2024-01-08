import dearpygui.dearpygui as dpg
from .widgets.node_editor import NodeEditor
from .widgets.node_selector import NodeSelector

class App:
    def __init__(self):
        dpg.create_context()
        dpg.create_viewport(title="Node Editor Template",
                            width=1500,
                            height=768)

        with dpg.viewport_menu_bar():
            dpg.add_menu_item(label="Debugger", callback=self.__on__show_debugger)
            dpg.add_menu_item(label="Item Registry", callback=self.__on_show_item_registry)
            dpg.add_menu_item(label="Close", callback=self.__on_close_program)

            node_editor = NodeEditor()
            NodeSelector()

        # Main Loop
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    @staticmethod
    def __on_close_program(sender, data):
        dpg.stop_dearpygui()

    @staticmethod
    def __on__show_debugger(sender, data):
        dpg.show_debug()

    @staticmethod
    def __on_show_item_registry(sender, data):
        dpg.show_item_registry()


if __name__ == "__main__":
    App()

