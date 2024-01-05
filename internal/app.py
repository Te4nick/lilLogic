# import dearpygui.dearpygui as dpg
#
# LastNodePosition = [100, 100]
#
#
# # Destroy window if closed
# def callback_close_window(sender):
#     dpg.delete_item(sender)
#
#
# # Delete selected items
# def callback_delete_item(sender):
#     for selected_node in dpg.get_selected_nodes("NodeEditor"):
#         # Deleting node and attached links
#         ## Extract all children of the deleted node
#         selected_node_children = dpg.get_item_children(selected_node)[1]
#         ## Extract all existing links in the Node Editor
#         node_editor_links = dpg.get_item_children("NodeEditor")[0]
#         ## Iterate through NodeEditor elements and delete attached links
#         for link in node_editor_links:
#             if dpg.get_item_configuration(link)["attr_1"] in selected_node_children or dpg.get_item_configuration(link)["attr_2"] in selected_node_children:
#                 dpg.delete_item(link)
#         ## Iterate trough LinkList and remove attached links
#         for item in LinkList:
#             for sub_item in item:
#                 if dpg.get_item_alias(selected_node) in sub_item:
#                     LinkList.remove(item)
#         # Deleting node
#         dpg.delete_item(selected_node)
#     for selected_link in dpg.get_selected_links("NodeEditor"):
#         func_link_destroyed("NodeEditor", selected_link)
#
#
# class NodeEditor:
#     def __init__(self):
#         with dpg.window(tag="NodeEditorWindow",
#                         label="Node editor",
#                         width=1000,
#                         height=700,
#                         pos=[50, 50],
#                         menubar=True,
#                         on_close=callback_close_window):
#             # Add a menu bar to the window
#             with dpg.menu_bar(label="MenuBar"):
#                 with dpg.menu(label="Input/Output nodes"):
#                     dpg.add_menu_item(tag="Menu_AddNode_InputFloat",
#                                       label="Input float",
#                                       callback=callback_add_node,
#                                       user_data="Input_Float")
#                     dpg.add_menu_item(tag="Menu_AddNode_InputButton",
#                                       label="Input button",
#                                       callback=callback_add_node,
#                                       user_data="Input_Button")
#                     dpg.add_menu_item(tag="Menu_AddNode_OutputFloat",
#                                       label="Output_Float",
#                                       callback=callback_add_node,
#                                       user_data="Output_Float")
#
#                 with dpg.menu(label="Math nodes"):
#                     dpg.add_menu_item(tag="Menu_AddNode_Addition",
#                                       label="Addition",
#                                       callback=callback_add_node,
#                                       user_data="Addition")
#                     dpg.add_menu_item(tag="Menu_AddNode_Subtraction",
#                                       label="Subtraction",
#                                       callback=callback_add_node,
#                                       user_data="Subtraction")
#                     dpg.add_menu_item(tag="Menu_AddNode_Multiplication",
#                                       label="Multiplication",
#                                       callback=callback_add_node,
#                                       user_data="Multiplication")
#                     dpg.add_menu_item(tag="Menu_AddNode_Division",
#                                       label="Division",
#                                       callback=callback_add_node,
#                                       user_data="Division")
#                     dpg.add_menu_item(tag="Menu_AddNode_And",
#                                       label="And",
#                                       callback=callback_add_node,
#                                       user_data="And"
#                                       )
#
#             with dpg.group(horizontal=True):
#                 dpg.add_text("Status:")
#                 dpg.add_text(tag="InfoBar")
#
#             # Add node editor to the window
#             with dpg.node_editor(tag="NodeEditor",
#                                  # Function call for updating all nodes if a new link is created
#                                  callback=func_chain_update,
#                                  # Function call for updating if a link is destroyed
#                                  delink_callback=func_link_destroyed):
#                 pass
#
#             with dpg.handler_registry():
#                 dpg.add_mouse_click_handler(callback=save_last_node_position)
#
#             with dpg.handler_registry():
#                 dpg.add_key_release_handler(key=dpg.mvKey_Delete, callback=callback_delete_item)
#         # End note editor
#
#
# # Saving the position of the last selected node
# def save_last_node_position():
#     global LastNodePosition
#     if not dpg.get_selected_nodes("NodeEditor"):
#         pass
#     else:
#         LastNodePosition = dpg.get_item_pos(dpg.get_selected_nodes("NodeEditor")[0])
#
#
# def callback_add_node(sender, app_data, user_data):
#     function_dict = {
#         "Input_Float": node_input_float.add_node_input_float,
#         "Input_Button": node_input_button.add_node_input_button,
#         "Output_Float": node_output_float.add_node_output_float,
#         "Addition": node_addition.AddNodeAddition,
#         "Subtraction": node_subtraction.add_node_subtraction,
#         "Multiplication": node_multiplication.add_node_multiplication,
#         "Division": node_division.add_node_division,
#         "And": base_and.AndNode
#     }
#     function_dict[user_data](LastNodePosition)
