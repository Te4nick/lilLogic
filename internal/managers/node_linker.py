from internal.nodeedit.base_node_link import NodeLink
from internal.utils import dpg2class


class NodeLinker:

    @staticmethod
    def link(from_attr: int | str, to_attr: int | str, parent: int | str):
        NodeLink(from_attr, to_attr, parent)

    @staticmethod
    def unlink(node_link: int | str):
        dpg2class(node_link).__del__()

