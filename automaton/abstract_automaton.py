from __future__ import annotations
from typing import Optional, Dict
from abc import ABC, abstractmethod
from graphviz import Digraph
from typing import Iterator

from utils.utils import key_generator


class Node:
    def __init__(self,
                 out: Optional[Dict] = None,
                 height: Optional[int] = None,
                 hash_generator: Iterator[str] = key_generator()):
        self.out = out if out else {}
        self.height = height
        self.hash = next(hash_generator)

    def add_height(self, height: int):
        self.height = self.height + height if self.height else height

    def add_edge(self, value: str, node: Node):
        if value in self.out:
            self.out[value].add(node)
        else:
            self.out[value] = {node}

    def delete_edge(self, value: str, node: Optional[Node] = None):
        if value in self.out:
            if node:
                self.out[value].remove(node)
            if node is None or not self.out[value]:
                self.out.pop(value)

    def __hash__(self) -> int:
        return int(self.hash)


class Automaton(ABC):
    def __init__(self, start: Optional[Node] = None, *final):
        self.start = start if start else Node()
        self.final = set(final) if final else {Node()}
        self.inner = set()

    @abstractmethod
    def match(self, word: str) -> bool:
        pass

    def add(self, *nodes):
        self.inner.update(nodes)

    def plot(self, name_generator: Optional[Iterator[str]] = None) -> Digraph:
        graph = Digraph()
        if name_generator is None:
            name_generator = key_generator()
        stack = [self.start]
        used = {self.start: next(name_generator)}
        while stack:
            node = stack.pop()
            name = used[node]
            graph.node(used[node], shape="doublecircle" if node in self.final else "circle")
            for value, children in node.out.items():
                for child in children:
                    if child in used:
                        graph.edge(name, used[child], value)
                    else:
                        child_name = next(name_generator)
                        graph.edge(name, child_name, value)
                        used[child] = child_name
                        stack.append(child)
        return graph
