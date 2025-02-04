import dearpygui.dearpygui as dpg
from .widgets.node_editor import NodeEditor
from .widgets.node_selector import NodeSelector
from .widgets.file_menu import FileMenu
from .widgets.help_menu import HelpMenu


class App:
    def __init__(self):
        dpg.create_context()
        dpg.create_viewport(title="Node Editor Template", width=1500, height=768)

        main_window = dpg.add_window(
            tag="TableWindow",
            menubar=True,
            autosize=True,
        )
        dpg.set_primary_window(main_window, True)

        table = dpg.add_table(
            parent=main_window, resizable=True, hideable=True, header_row=False
        )
        dpg.add_table_column(parent=table)
        dpg.add_table_column(parent=table, width=200)
        row = dpg.add_table_row(parent=table)

        self.node_editor = NodeEditor(dpg.add_child_window(parent=row))
        self.node_selector = NodeSelector(dpg.add_child_window(parent=row))

        menu_bar = dpg.add_viewport_menu_bar()
        FileMenu(menu_bar)
        HelpMenu(menu_bar)
        # dpg.add_menu_item(label="Close", callback=self.__on_close_program)

        # Main Loop
        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    @staticmethod
    def __on_close_program(sender, data):
        dpg.stop_dearpygui()


if __name__ == "__main__":
    App()
