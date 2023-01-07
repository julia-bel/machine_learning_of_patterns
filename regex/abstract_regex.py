from __future__ import annotations
from typing import Any, Iterator, Optional
from abc import ABC, abstractmethod
from graphviz import Digraph

from automaton.automaton import NFA


class Regex(ABC):
    def __init__(self, value: Any):
        assert value, "empty regular expression"
        self.value = value

    def __len__(self) -> int:
        return len(self.value)

    def match(self, word: str) -> bool:
        word_len = len(word)
        for final in self.starts_with(word):
            if final == word_len:
                return True
        return False

    @abstractmethod
    def __str__(self) -> str:
        pass

    @abstractmethod
    def starts_with(self, text: str) -> Iterator[int]:
        pass

    @abstractmethod
    def to_nfa(self, last_nfa: Optional[NFA] = None) -> NFA:
        pass

    @abstractmethod
    def plot(self,
             parent: Optional[str] = None,
             graph: Digraph = Digraph(),
             name_generator: Optional[Iterator[str]] = None) -> Digraph:
        pass


class NodeRegex(Regex):
    def __init__(self, value: Any):
        super(NodeRegex, self).__init__(value)
        self.unpack()

    @abstractmethod
    def unpack(self):
        pass
