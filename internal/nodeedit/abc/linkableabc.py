from abc import ABC, abstractmethod
from typing import Any
from .link import Link


class LinkableABC(ABC):
    @abstractmethod
    def add_to_link(self, item: int | str, link: Link):
        pass

    @abstractmethod
    def delete_to_link(self, item: int | str):
        pass

    @abstractmethod
    def add_from_link(self, item: int | str, link: Link):
        pass

    @abstractmethod
    def delete_from_link(self, item: int | str):
        pass

    @abstractmethod
    def set_value(self, value: Any):
        pass

    @abstractmethod
    def get_value(self) -> Any:
        pass

    @abstractmethod
    def send_value(self):
        pass

    @abstractmethod
    def receive_value(self, value: Any):
        pass
