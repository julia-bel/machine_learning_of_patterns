from __future__ import annotations
from typing import Optional, List, Tuple, Any, Set

from regex.const import EPSILON
from .abstract_automaton import Automaton, Node


class DFA(Automaton):
    def match(self, word: str) -> bool:
        word = list(word[::-1])
        stack = {self.start}
        while stack and word:
            char = word.pop()
            node = stack.pop()
            if char in node.out:
                stack = node.out[char].copy()
            else:
                return False
        return not word and stack and stack.pop() in self.final


class NFA(Automaton):
    def __eps_closure(self, stack: Optional[Set[Node]] = None) -> Set[Node]:
        stack = [self.start] if stack is None else list(stack)
        closure = set(stack)
        while stack:
            node = stack.pop()
            if EPSILON in node.out:
                for child in node.out[EPSILON]:
                    if child not in closure:
                        closure.add(child)
                        stack.append(child)
        return closure

    def __rename_dfa(self, start: Set[Node], final: List[Set[Node]], new_nodes: List[Tuple[Any]]) -> DFA:

        def get_new_node(multinode: Set[Node]) -> Optional[Node]:
            for prev_nodes, new_node in new_nodes:
                if prev_nodes == multinode:
                    return new_node

        final = set([get_new_node(node) for node in final])
        start = get_new_node(start)
        stack = [start]
        used = set(stack)
        while stack:
            cur_node = stack.pop()
            for value, children in cur_node.out.copy().items():
                new_node = get_new_node(children)
                cur_node.delete_edge(value)
                cur_node.add_edge(value, new_node)
                if new_node not in used:
                    used.add(new_node)
                    stack.append(new_node)
        inner = used.difference(final)
        inner.discard(start)
        dfa = DFA(start, *final)
        dfa.add(*inner)
        return dfa

    def to_dfa(self) -> DFA:
        start = self.__eps_closure()
        final, new_nodes = [], []
        stack, used = [start], [start]
        while stack:
            cur_node = stack.pop()
            for node in cur_node:
                if node in self.final:
                    final.append(cur_node)
                    break
            map_closure = {}
            for node in cur_node:
                for value, children in node.out.items():
                    if value == EPSILON:
                        continue
                    if value not in map_closure:
                        map_closure[value] = self.__eps_closure(children)
                    else:
                        map_closure[value] = map_closure[value].union(self.__eps_closure(children))
            for value, closure in map_closure.items():
                if closure not in used:
                    used.append(closure)
                    stack.append(closure)
            new_nodes.append((cur_node, Node(map_closure)))
        assert len(new_nodes) == len(used), f'{len(new_nodes), len(used)}'
        return self.__rename_dfa(start, final, new_nodes)

    def match(self, word: str) -> bool:
        cost = {}
        closure = self.__eps_closure()
        word = list(word[::-1])
        while word and closure:
            char = word.pop()
            new_closure = set()
            for node in closure:
                if char in node.out:
                    if node.height:
                        if node in cost:
                            if cost[node] > 0:
                                cost[node] -= 1
                            else:
                                continue
                        else:
                            cost[node] = node.height - 1
                    new_closure = new_closure.union(self.__eps_closure(node.out[char]))
            closure = new_closure
        for node in closure:
            if node in self.final:
                return True
        return False
