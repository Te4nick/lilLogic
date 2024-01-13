from icecream import ic

from ..abc.linkableabc import LinkableABC, Link
from typing import Any, Callable


class Linkable(LinkableABC):

    __slots__ = ["value", "_callback", "__links_to", "__links_from"]

    def __init__(self, callback: Callable):
        self.value = 0
        self._callback = callback
        self.__links_to: dict[str: Link] = {}
        self.__links_from: dict[str: Link] = {}

    def __del__(self):
        for link in list(self.__links_to.values()):
            link.__del__()
        for link in list(self.__links_from.values()):
            link.__del__()
        del self.__links_to
        del self.__links_from

    def _on_set_value(self):
        pass

    def build(self):
        pass

    def add_to_link(self, item: int | str, link: Link):
        self.__links_to[item] = link
        link.send(self.value)

    def delete_to_link(self, item: int | str):
        self.__links_to.pop(item)

    def add_from_link(self, item: int | str, link: Link):
        self.__links_from[item] = link

    def delete_from_link(self, item: int | str):
        self.__links_from.pop(item)

    def get_value(self) -> Any:
        return self.value

    def set_value(self, value: Any):
        self.value = value
        self.send_value()
        self._on_set_value()

    def send_value(self):
        for link in self.__links_to.values():
            link.send(self.value)

    def receive_value(self, value: Any):
        ic()
        ic(value)
        if value != self.value:
            self.set_value(value)
            self._callback()
