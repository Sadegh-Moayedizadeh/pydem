from __future__ import annotations

from abc import ABC, abstractproperty, abstractmethod
from typing import Dict


class BaseShape(ABC):
    @abstractproperty
    def center_x(self) -> float:
        pass

    @abstractproperty
    def center_y(self) -> float:
        pass

    @abstractmethod
    def area(self) -> float:
        pass

    @abstractmethod
    def __deepcopy__(self, memo: Dict[int, object]) -> BaseShape:
        pass
