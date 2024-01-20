from abc import ABC, abstractmethod
from typing import Any
from .link import Link


class LinkableABC(ABC):

    @abstractmethod
    def add_link(self, item: int | str, link: Link, outgoing: bool):
        pass

    @abstractmethod
    def delete_link(self, item: int | str, outgoing: bool):
        pass

    @abstractmethod
    def send_value(self):
        pass

    @abstractmethod
    def receive_value(self, value: Any):
        pass
