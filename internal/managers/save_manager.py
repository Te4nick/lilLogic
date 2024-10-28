from dataclasses import dataclass

from internal.nodeedit import Node, NodeLink
from internal.utils import dpg2class


@dataclass
class SaveData:
    nodes: list[dict]  # NodeData
    links: list[dict]  # NodeLinkData


class SaveMan:
    def __init__(self) -> None:
        self.__nodes: list[Node] = []
        self.__node_links: list[NodeLink] = []

    @staticmethod
    def dump_save(node_ids: list[int | str], link_ids: list[int | str]) -> dict:
        nodes: list[dict] = []
        links: list[dict] = []
        for i in range(len(node_ids)):
            node: Node = dpg2class(node_ids[i])
            nodes.append(node.serialize())
        for i in range(len(link_ids)):
            link: NodeLink = dpg2class(link_ids[i])
            links.append(link.serialize())
        return SaveData(
            nodes=nodes,
            links=links,
        ).__dict__
