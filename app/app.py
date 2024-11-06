import dearpygui.dearpygui as dpg
from dearpygui import demo as dpg_demo
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
            
            with dpg.menu(label="Help"):
                dpg.add_menu_item(label="Debugger", callback=self.__on_show_debugger)
                dpg.add_menu_item(label="Item Registry", callback=self.__on_show_item_registry)
                dpg.add_menu_item(label="Demo", callback=dpg_demo.show_demo)
            
            dpg.add_menu_item(label="Close", callback=self.__on_close_program)
        
        main_window = dpg.add_window(
            tag="TableWindow",
            label="Table",
            menubar=True,
            autosize=True,
        )
        dpg.set_primary_window(main_window, True)

        table = dpg.add_table(parent=main_window, resizable=True, header_row=False)
        dpg.add_table_column(parent=table)
        dpg.add_table_column(parent=table)
        row = dpg.add_table_row(parent=table)

        self.node_editor = NodeEditor(dpg.add_child_window(parent=row))
        self.node_selector = NodeSelector(dpg.add_child_window(parent=row))

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
            self.node_editor.create_links(save_data.links)

        return on_file_open


if __name__ == "__main__":
    App()
