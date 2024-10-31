import dearpygui.dearpygui as dpg
from .widgets.node_editor import NodeEditor
from .widgets.node_selector import NodeSelector
from internal.managers import SaveMan


class App:
    def __init__(self):
        dpg.create_context()
        dpg.create_viewport(title="Node Editor Template", width=1500, height=768)

        with dpg.viewport_menu_bar():
            with dpg.menu(label="File"):
                dpg.add_menu_item(label="Save", callback=self.__on_file_save())
                dpg.add_menu_item(label="Save As", callback=self.__on_file_save())
                dpg.add_menu_item(label="Open", callback=self.__on_file_open())
            dpg.add_menu_item(label="Debugger", callback=self.__on_show_debugger)
            dpg.add_menu_item(
                label="Item Registry", callback=self.__on_show_item_registry
            )
            dpg.add_menu_item(label="Close", callback=self.__on_close_program)

            self.node_editor = NodeEditor()
            self.node_selector = NodeSelector()

        # Main Loop
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    @staticmethod
    def __on_close_program(sender, data):
        dpg.stop_dearpygui()

    @staticmethod
    def __on_show_debugger(sender, data):
        dpg.show_debug()

    @staticmethod
    def __on_show_item_registry(sender, data):
        dpg.show_item_registry()

    def __on_file_save(self):
        def on_file_save(sender, data):  # TODO: into separate widget
            SaveMan.write_save("test_save", self.node_editor.get_nodes_data())

        return on_file_save

    def __on_file_open(self):
        def on_file_open(sender, data):  # TODO: remove hardcode path
            save_data = SaveMan.read_save(
                SaveMan.get_default_save_path() / "test_save.json"
            )
            self.node_editor.clear_canvas()
            print(save_data)
            self.node_selector.add_from_data(save_data.nodes)

        return on_file_open


if __name__ == "__main__":
    App()
