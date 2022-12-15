from __future__ import annotations

from typing import List, Iterator

from pattern.abstract_pattern import Variable, Pattern


class NEVariable(Variable):
    def __init__(self, name: str):
        super().__init__(name)

    def substitute(self, value: str):
        assert len(value), "length of the value must be > 0"
        self.value = value

    def __len__(self) -> int:
        return len(self.value) if self.value else 0

    def __str__(self) -> str:
        return "" if self.is_free() else self.value


class NEPattern(Pattern):
    def __init__(self, value: List[str | Variable]):
        super().__init__(value)

    def slice_len(self, start: int = 0) -> int:
        length = 0
        for value in self.value[start:]:
            l = len(value)
            length += l if l > 0 else 1
        return length

    def is_alphabet_compatible(self, word: str, value_start: int = 0) -> bool:
        word_tail = list(word)
        value_tail = self.value[value_start:]
        if len(word_tail) < self.slice_len(value_start):
            return False
        for value in value_tail:
            if not word_tail:
                break
            if type(value) is str or not value.is_free():
                for char in str(value):
                    if char in word_tail:
                        word_tail.remove(char)
                    else:
                        return False
        return True

    def match(self, word: str) -> bool:
        if not self.is_alphabet_compatible(word):
            return False

        def get_free_positions(var_i: int, start: int = 0) -> Iterator[int]:
            var = self.value[var_i]
            for i in range(start + 1, len(word) + 1):
                if not self.is_alphabet_compatible(word[i:], var_i + 1):
                    break
                var.substitute(word[start:i])
                yield i

        def iter_positions(i: int) -> int:
            nonlocal stack
            while stack and stack[-1][1] is None:
                i -= 1
                stack.pop()
            if stack:
                try:
                    stack[-1][0] = next(stack[-1][1])
                    return i
                except StopIteration:
                    stack.pop()
                    return iter_positions(i - 1)
            return -1

        stack = []
        i = 0
        while i < len(self.value):
            value = self.value[i]
            start = stack[-1][0] if stack else 0
            if type(value) is str or not value.is_free():
                if word[start:].startswith(str(value)):
                    stack.append([start + len(value), None])
                else:
                    i = iter_positions(i - 1)
            else:
                positions = get_free_positions(i, start)
                try:
                    stack.append([next(positions), positions])
                except StopIteration:
                    i = iter_positions(i - 1)
            if i < 0:
                return False
            i += 1
        return True

    def include(self, pattern: NEPattern) -> bool:
        assert len(self) == len(pattern), "invalid inclusion"
        return self.match(str(pattern))
