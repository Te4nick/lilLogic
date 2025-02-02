import dearpygui.dearpygui as dpg
from dearpygui import demo as dpg_demo


class HelpMenu:
    def __init__(self, parent: int | str = None):
        with dpg.menu(label="Help", parent=parent):
            dpg.add_menu_item(label="Debugger", callback=self.__on_show_debugger)
            dpg.add_menu_item(
                label="Item Registry", callback=self.__on_show_item_registry
            )
            dpg.add_menu_item(label="Demo", callback=dpg_demo.show_demo)

    @staticmethod
    def __on_show_debugger(sender, data):
        dpg.show_debug()

    @staticmethod
    def __on_show_item_registry(sender, data):
        dpg.show_item_registry()
