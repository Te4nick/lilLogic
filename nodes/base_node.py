from uuid import uuid4
from typing import Any
import dearpygui.dearpygui as dpg


# from src.base.chain_update import func_chain_update


class Node:
    node_type: str = "BaseNode"

    def __init__(self, user_data: dict[str, Any] = None):
        if user_data is None:
            user_data = {}
        self.tag = str(uuid4()) + "_" + self.node_type
        self.alias = self.tag + "_Node"

        self.inputs: dict[str, int | str] = {}
        self.outputs: dict[str, int | str] = {}

        self.__node_outputs: dict[str, int | str] = {}

        self.__links: dict[int | str: list[int | str]] = {}

        self.build()
        self.__build_node(user_data)

    def __build_node(self, user_data):
        user_data["class"] = self
        self.node = dpg.node(
            tag=self.tag + "_Node",
            user_data=user_data,
            parent="NodeEditor",
            label=self.node_type,
            pos=user_data["pos"] if "pos" in user_data.keys() else [0, 0]
        )

        with self.node:

            input_count = 0
            for input_label, input_index in self.inputs.items():
                input_count += 1
                self.__build_input(
                    input_label,
                    input_index,
                    readonly=(input_count != input_index)
                )

            output_count = 0
            for output_label, output_index in self.outputs.items():
                output_count += 1
                self.__build_output(
                    output_label,
                    output_index,
                    readonly=(output_count != output_index)
                )

        print("AND ID:", self.node)

    def __build_input(self, label, index, readonly: bool = False):
        with dpg.node_attribute(tag=self.tag + f"_Input{index}"):
            self.inputs[label] = 0
            dpg.add_input_int(
                tag=self.tag + f"_Input{index}_Value",
                label=label,
                width=100,
                default_value=0,
                callback=self.__on_input_changed(label),
                readonly=readonly
            )

    def __build_output(self, label, index, readonly: bool = True):
        with dpg.node_attribute(
                tag=self.tag + f"_Output{index}",
                attribute_type=dpg.mvNode_Attr_Output
        ):
            self.outputs[label] = 0
            self.__links[label] = []
            self.__node_outputs[label] = dpg.add_input_int(
                tag=self.tag + f"_Output{index}_Value",
                label=label,
                width=100,
                default_value=0,
                callback=self.__on_output_changed(label),
                readonly=readonly
            )

    def __on_input_changed(self, label):
        def input_changed(sender: Any = None, app_data: Any = None, user_data: Any = None):
            self.inputs[label] = dpg.get_value(sender)
            self.calculate()

        return input_changed

    def __on_output_changed(self, label):

        def output_changed(sender: Any = None, app_data: Any = None, user_data: Any = None):
            self.set_output_value(label, dpg.get_value(sender))
            # self.calculate()
        return output_changed

    # def __alias2id(self, alias):
    #     pass

    def calculate(self):
        pass

    def build(self):
        pass

    def add_input(self, label: str, readonly: bool = False) -> None:
        self.inputs[label] = len(self.inputs) + 1 + readonly

    def add_output(self, label: str, readonly: bool = True) -> None:
        self.outputs[label] = len(self.outputs) + 1 + readonly

    def add_output_link(self, output_value_id: int | str, attr_value_id: int | str) -> None:
        self.__links[dpg.get_item_label(output_value_id)].append(attr_value_id)
        dpg.set_value(attr_value_id, dpg.get_value(output_value_id))
        pass

    def set_output_value(self, label: str, value: int) -> None:
        dpg.set_value(self.__node_outputs[label], value)
        for link in self.__links[label]:
            dpg.set_value(link, value)

    def delete_output_link(self, output_value_id: int | str, attr_value_id: int | str) -> None:
        self.__links[dpg.get_item_label(output_value_id)].remove(attr_value_id)
        dpg.set_value(attr_value_id, 0)
        pass
