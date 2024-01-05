import dearpygui.dearpygui as dpg
from nodes.logic.logic_and import LogicAnd
from nodes.logic.logic_out import LogicOut
from nodes.logic.logic_in import LogicIn
from nodes.logic.logic_not import LogicNot
from internal.node_db import NodeDB

if __name__ == "__main__":  # TODO: extract to App.py ?

    node_db = NodeDB()

    dpg.create_context()

    # callback runs when user attempts to connect attributes
    def link_callback(sender, app_data):
        # app_data -> (link_id1, link_id2)
        link = dpg.add_node_link(app_data[0], app_data[1], parent=sender)
        node_db.register_link(link, app_data[0], app_data[1])

    # callback runs when user attempts to disconnect attributes
    def delink_callback(sender, app_data):
        # app_data -> link_id
        dpg.delete_item(app_data)
        node_db.unregister_link(app_data)


    with dpg.window(label="Tutorial", width=400, height=400):
        with dpg.node_editor(tag="NodeEditor", callback=link_callback, delink_callback=delink_callback):

            node_db.register_node(LogicAnd())
            node_db.register_node(LogicAnd())
            node_db.register_node(LogicOut())
            node_db.register_node(LogicIn())
            node_db.register_node(LogicNot())

    dpg.create_viewport(title='Custom Title', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.show_item_registry()
    dpg.start_dearpygui()
    dpg.destroy_context()
