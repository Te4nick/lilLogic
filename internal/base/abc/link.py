from abc import ABC, abstractmethod
from typing import Any


class Link(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def __del__(self):
        pass

    @abstractmethod
    def send(self, value: Any):
        pass


class Linkable(ABC):
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
    def receive_value(self, value: Any):
        pass
