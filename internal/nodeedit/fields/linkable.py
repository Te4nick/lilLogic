from ..abc.linkableabc import LinkableABC, Link
from typing import Any, Callable

from internal.utils import logger


class Linkable(LinkableABC):

    __slots__ = ["value", "_callback", "__links_to", "__links_from"]

    def __init__(self, tag: str, callback: Callable):
        self.tag = tag
        self.value = 0
        self._callback = callback
        self.__links_to: dict[str:Link] = {}
        self.__links_from: dict[str:Link] = {}

    def __del__(self):
        for link in list(self.__links_to.values()):
            link.__del__()
        for link in list(self.__links_from.values()):
            link.__del__()
        # del self.__links_to
        # del self.__links_from
        logger.debug(f"{self.tag}.__del__() __links_to: {self.__links_to}")
        logger.debug(f"{self.tag}.__del__() __links_from: {self.__links_from}")

    def _on_receive_value(self):
        pass

    def add_link(self, item: int | str, link: Link, outgoing: bool):
        if outgoing:
            self.__links_to[item] = link
            link.send(self.value)
            logger.debug(f"{self.tag}: adding outgoing link to id: {item}")
            logger.debug(f"{self.tag}: __links_to: {self.__links_to}")
        else:
            self.__links_from[item] = link
            logger.debug(f"{self.tag}: adding incoming link from id: {item}")
            logger.debug(f"{self.tag}: __links_from: {self.__links_from}")

    def delete_link(self, item: int | str, outgoing: bool):
        if outgoing:
            self.__links_to.pop(item, None)
            logger.debug(f"{self.tag}: deleting outgoing link to id: {item}")
            logger.debug(f"{self.tag}: __links_to: {self.__links_to}")
        else:
            self.__links_from.pop(item, None)
            logger.debug(f"{self.tag}: deleting incoming link from id: {item}")
            logger.debug(f"{self.tag}: __links_from: {self.__links_from}")

    def send_value(self):
        for link in self.__links_to.values():
            link.send(self.value)

    def receive_value(self, value: Any):
        logger.debug(f"{self.tag}: receiving value: {value}; self.value: {self.value}")
        if value != self.value:
            self.value = value
            self.send_value()
            self._callback()
            self._on_receive_value()
