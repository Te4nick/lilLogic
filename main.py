import dearpygui.dearpygui as dpg
from nodes.logic_and import LogicAnd
from nodes.base_node import Node


if __name__ == "__main__":  # TODO: extract to App.py ?

    node_db: dict[str, Node] = {}

    dpg.create_context()

    # callback runs when user attempts to connect attributes
    def link_callback(sender, app_data):  # TODO: mass callback refactor
        # app_data -> (link_id1, link_id2)
        dpg.add_node_link(app_data[0], app_data[1], parent=sender)
        print({"link_id1": app_data[0], "link_id2": app_data[1]})
        print({"link_id1_parent": dpg.get_item_parent(app_data[0]),
               "link_id2_parent": dpg.get_item_parent(app_data[1])})
        dpg.get_item_user_data(dpg.get_item_parent(app_data[0]))["class"].add_output_link(app_data[0], app_data[1])


    # callback runs when user attempts to disconnect attributes
    def delink_callback(sender, app_data):
        # app_data -> link_id
        dpg.delete_item(app_data)


    with dpg.window(label="Tutorial", width=400, height=400):
        with dpg.node_editor(tag="NodeEditor", callback=link_callback, delink_callback=delink_callback):
            # with dpg.node(label="Node 1"):
            #     with dpg.node_attribute(label="Node A1"):
            #         dpg.add_input_int(label="F1", width=150)
            #
            #     with dpg.node_attribute(label="Node A2", attribute_type=dpg.mvNode_Attr_Output):
            #         dpg.add_input_int(label="F2", width=150)
            #
            # with dpg.node(label="Node 2"):
            #     with dpg.node_attribute(label="Node A3"):
            #         dpg.add_input_int(label="F3", width=200)
            #
            #     with dpg.node_attribute(label="Node A4", attribute_type=dpg.mvNode_Attr_Output):
            #         dpg.add_input_int(label="F4", width=200)

            land1 = LogicAnd()
            node_db[land1.node] = land1

            land2 = LogicAnd()
            node_db[land2.id] = land2


    dpg.create_viewport(title='Custom Title', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.show_item_registry()
    dpg.start_dearpygui()
    dpg.destroy_context()