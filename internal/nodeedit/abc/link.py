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
