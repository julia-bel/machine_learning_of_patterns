from __future__ import annotations

from abc import ABC, abstractmethod
from typing import List


class Variable(ABC):
    def __init__(self, name: str):
        self.name = name
        self.value = None

    def is_free(self) -> bool:
        return self.value is None

    def __str__(self) -> str:
        return self.value if self.value else ''

    @abstractmethod
    def substitute(self, value: str):
        pass


class Pattern(ABC):
    def __init__(self, value: List[str | Variable]):
        assert value, "empty pattern"
        self.value = value

    def __len__(self) -> int:
        return len(self.value)

    def __str__(self) -> str:
        return ''.join([v if type(v) is str else v.name for v in self.value])

    @abstractmethod
    def match(self, word: str) -> bool:
        pass

    def include(self, pattern: Pattern) -> bool:
        pass
