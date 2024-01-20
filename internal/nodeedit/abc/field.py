from abc import ABC, abstractmethod
from typing import Any


class FieldABC(ABC):

    @abstractmethod
    def get_value(self) -> Any:
        pass

    @abstractmethod
    def set_value(self, value: Any):
        pass

    @abstractmethod
    def build(self):
        pass
