from uuid import uuid4
from typing import Callable
import dearpygui.dearpygui as dpg
# from src.base.chain_update import func_chain_update


class Node:
    node_type: str = "BaseNode"

    def __init__(self, user_data: list[int]):
        self.id = uuid4()
        self.tag = str(self.id) + self.node_type

        self.inputs: dict[str, int | str] = {}
        self.outputs: dict[str, int | str] = {}

        self.build()
        self.__build_node(user_data)

    def __build_node(self, user_data):
        with dpg.node(
                tag=str(self.id) + "!Node" + self.node_type,
                parent="NodeEditor",
                label=self.node_type,
                pos=user_data
        ):
            for input_label, input_index in self.inputs.items():
                self.__build_input(input_label, input_index)

            for output_label, output_index in self.outputs.items():
                self.__build_output(output_label, output_index)

    def __build_input(self, label, index):
        with dpg.node_attribute(tag=self.tag + f"_Input{index}"):
            self.inputs[label] = dpg.add_input_int(
                tag=self.tag + f"_Input{index}_value",
                label=label,
                width=100,
                default_value=0,
                callback=self.calculate  # TODO: implement callback
            )

    def __build_output(self, label, index):
        with dpg.node_attribute(
                tag=self.tag + "_Output",
                attribute_type=dpg.mvNode_Attr_Output
        ):

            self.outputs[label] = dpg.add_input_int(
                tag=self.tag + "_Output_value",
                label=label,
                width=100,
                default_value=0,
                readonly=True)

    def calculate(self):
        pass

    def build(self):
        pass

    def add_input(self, label: str):
        self.inputs[label] = len(self.inputs) + 1

    def add_output(self, label: str):
        self.outputs[label] = len(self.outputs) + 1
