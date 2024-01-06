import dearpygui.dearpygui as dpg
from icecream import install as icinstall
from internal.app import NodeEditor


def callback_close_program(sender, data):
    exit(0)


def callback_show_debugger(sender, data):
    dpg.show_debug()


def callback_show_item_registry(sender, data):
    dpg.show_item_registry()


if __name__ == "__main__":  # TODO: extract to App.py ?
    icinstall()

    dpg.create_context()
    dpg.create_viewport(title="Node Editor Template",
                        width=1500,
                        height=768)

    with dpg.viewport_menu_bar():
        dpg.add_menu_item(label="Debugger", callback=callback_show_debugger)
        dpg.add_menu_item(label="Item Registry", callback=callback_show_item_registry)
        dpg.add_menu_item(label="Close", callback=callback_close_program)

        nodeEditor = NodeEditor()

    # Main Loop
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
