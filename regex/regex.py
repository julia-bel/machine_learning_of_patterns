from __future__ import annotations

from collections import OrderedDict
from typing import List, Iterator, Optional

from graphviz import Digraph

from automaton.abstract_automaton import Node
from automaton.automaton import NFA
from regex.abstract_regex import Regex, NodeRegex
from regex.const import EPSILON
from utils.utils import key_generator


class BaseRegex(Regex):
    def starts_with(self, text: str) -> Iterator[int]:
        if text.startswith(self.value):
            yield len(self.value)

    def to_nfa(self, last_nfa: Optional[NFA] = None) -> NFA:
        if last_nfa is None:
            nfa = NFA()
            for final in nfa.final:
                nfa.start.add_edge(self.value, final)
        else:
            nfa = NFA(last_nfa.start)
            nfa.add(*last_nfa.inner, *last_nfa.final)
            for node in last_nfa.final:
                for final in nfa.final:
                    node.add_edge(self.value, final)
        return nfa

    def plot(self,
             parent: Optional[str] = None,
             graph: Digraph = Digraph(),
             name_generator: Optional[Iterator[str]] = None) -> Digraph:
        if name_generator is None:
            name_generator = key_generator()
        name = next(name_generator)
        graph.node(name, self.__class__.__name__)
        if parent is not None:
            graph.edge(parent, name)
        value = next(name_generator)
        graph.node(value, self.value)
        graph.edge(name, value)
        return graph


class BracketRegex(NodeRegex):
    def __init__(self, value: List[Regex]):
        super().__init__(value)
        self.unpack()

    def unpack(self):
        while len(self.value) == 1 and type(self.value[0]) is type(self):
            self.value = self.value[0].value

    def starts_with(self, text: str) -> Iterator[int]:
        stack = [(0, text, 0)]
        while stack:
            regex_i, word, k = stack.pop()
            for i in self.value[regex_i].starts_with(word):
                if regex_i + 1 == len(self.value):
                    yield k + i
                else:
                    stack.append((regex_i + 1, word[i:], k + i))

    def to_nfa(self, last_nfa: Optional[NFA] = None) -> NFA:
        nfa = last_nfa
        for regex in self.value:
            nfa = regex.to_nfa(nfa)
        return nfa

    def plot(self,
             parent: Optional[str] = None,
             graph: Digraph = Digraph(),
             name_generator: Optional[Iterator[str]] = None) -> Digraph:
        if name_generator is None:
            name_generator = key_generator()
        name = next(name_generator)
        graph.node(name, self.__class__.__name__)
        if parent is not None:
            graph.edge(parent, name)
        for v in self.value:
            v.plot(name, graph, name_generator)
        return graph


class AlternativeRegex(NodeRegex):
    def __init__(self, value: List[Regex]):
        super().__init__(value)

    def unpack(self):
        pass

    def starts_with(self, text: str) -> Iterator[int]:
        for regex in self.value:
            for i in regex.starts_with(text):
                yield i

    def to_nfa(self, last_nfa: Optional[NFA] = None) -> NFA:
        nfas = [regex.to_nfa() for regex in self.value]
        start = Node() if last_nfa is None else last_nfa.final.pop()
        final = Node()
        for nfa_branch in nfas:
            start.add_edge(EPSILON, nfa_branch.start)
            for branch_final in nfa_branch.final:
                branch_final.add_edge(EPSILON, final)
        if last_nfa is None:
            nfa = NFA(start, final)
        else:
            nfa = NFA(last_nfa.start, final)
            nfa.add(start, *last_nfa.inner)
        for nfa_branch in nfas:
            nfa.add(nfa_branch.start, *nfa_branch.inner, *nfa_branch.final)
        return nfa

    def plot(self,
             parent: Optional[str] = None,
             graph: Digraph = Digraph(),
             name_generator: Optional[Iterator[str]] = None) -> Digraph:
        if name_generator is None:
            name_generator = key_generator()
        name = next(name_generator)
        graph.node(name, self.__class__.__name__)
        if parent is not None:
            graph.edge(parent, name)
        for v in self.value:
            v.plot(name, graph, name_generator)
        return graph


class StarRegex(NodeRegex):
    def __init__(self, value: Regex, height: int):
        self.height = height
        NodeRegex.__init__(self, value)

    def unpack(self):
        while type(self.value) is type(self):
            self.height += self.value.height
            self.value = self.value.value

    def starts_with(self, text: str) -> Iterator[int]:
        used = set()
        stack = OrderedDict([(0, self.height)])
        while stack:
            i, h = stack.popitem()
            yield i
            used.add(i)
            if h > 0:
                for j in self.value.starts_with(text[i:]):
                    j += i
                    if j not in used:
                        prev = stack.get(j)
                        stack[j] = h - 1 if prev is None else min(prev, h - 1)

    def to_nfa(self, last_nfa: Optional[NFA] = None) -> NFA:
        inner_nfa = self.value.to_nfa()
        inner_nfa.start.add_height(self.height)
        start = Node() if last_nfa is None else last_nfa.final.pop()
        final = Node()
        start.add_edge(EPSILON, inner_nfa.start)
        start.add_edge(EPSILON, final)
        for inner_final in inner_nfa.final:
            inner_final.add_edge(EPSILON, inner_nfa.start)
            inner_final.add_edge(EPSILON, final)
        if last_nfa is None:
            nfa = NFA(start, final)
        else:
            nfa = NFA(last_nfa.start, final)
            nfa.add(start, *last_nfa.inner)
        nfa.add(inner_nfa.start, *inner_nfa.inner, *inner_nfa.final)
        return nfa

    def plot(self,
             parent: Optional[str] = None,
             graph: Digraph = Digraph(),
             name_generator: Optional[Iterator[str]] = None) -> Digraph:
        if name_generator is None:
            name_generator = key_generator()
        name = next(name_generator)
        graph.node(name, self.__class__.__name__ + f" [{self.height}]")
        if parent is not None:
            graph.edge(parent, name)
        self.value.plot(name, graph, name_generator)
        return graph
