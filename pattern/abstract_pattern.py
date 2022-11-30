from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class Variable(ABC):
    def __init__(self, name: str):
        self.name = name
        self.value = None

    def is_free(self) -> bool:
        return self.value is None

    @abstractmethod
    def substitute(self, value: str):
        pass


class Pattern(ABC):
    def __init__(self, value: List[str | Variable]):
        assert value, "empty pattern"
        self.value = value

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def match(self, word: str) -> bool:
        pass
