from internal.nodeedit import Node, NodeLink
from internal.utils import dpg2class


class SaveMan:
    def __init__(self) -> None:
        self.__nodes: list[Node] = []
        self.__node_links: list[NodeLink] = []

    @staticmethod
    def dump_nodes(node_ids: list[int | str]) -> dict:
        node_dict: dict = {}
        for i in range(len(node_ids)):
            node: Node = dpg2class(node_ids[i])
            node_dict[i] = node.serialize()
        return node_dict
