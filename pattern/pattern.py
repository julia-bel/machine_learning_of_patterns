from __future__ import annotations
from typing import List, Iterator, Optional

from pattern.abstract_pattern import Variable, Pattern


class NEVariable(Variable):
    def __init__(self, value: Optional[str] = None):
        super().__init__(value)

    def substitute(self, value: str | List[str]):
        assert len(value), "length of the value must be > 0"
        self.value = value.split() if type(value) is str else value


class NEPattern(Pattern):
    def __init__(self, value: List[str | Variable]):
        super().__init__(value)

    def shape(self) -> List[str]:
        result = []
        vars = {}
        i = 1
        for value in self.value:
            if type(value) is NEVariable:
                prev_i = vars.get(value)
                if prev_i is None:
                    vars[value] = f"x{i}"
                    result.append(vars[value])
                    i += 1
                else:
                    result.append(prev_i)
            else:
                result.append(value)
        return result

    def slice_len(self, start: int = 0, end: int = -1) -> int:
        length = 0
        for value in self.value[start:end]:
            l = len(value)
            length += l if l > 0 else 1
        return length

    def is_alphabet_compatible(self, word: str | List[str], value_start: int = 0) -> bool:
        word_tail = list(word)
        value_tail = self.value[value_start:]
        if len(word_tail) < self.slice_len(value_start):
            return False
        for value in value_tail:
            if len(word_tail) == 0:
                break
            if type(value) is str:
                if value in word_tail:
                    word_tail.remove(value)
                else:
                    return False
            elif not value.is_free():
                for char in value.value:
                    if char in word_tail:
                        word_tail.remove(char)
                    else:
                        return False
        return True

    def match(self, word: str | List[str]) -> bool:
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

        word = list(word)
        stack = []
        i = 0
        while i < len(self.value):
            value = self.value[i]
            start = stack[-1][0] if stack else 0
            if type(value) is str:
                if word[start] == value:
                    stack.append([start + 1, None])
                else:
                    i = iter_positions(i - 1)
            elif value.is_free():
                positions = get_free_positions(i, start)
                try:
                    stack.append([next(positions), positions])
                except StopIteration:
                    i = iter_positions(i - 1)
            else:
                if word[start:start + len(value)] == value.value:
                    stack.append([start + len(value), None])
                else:
                    i = iter_positions(i - 1)
            if i < 0:
                self.free()
                return False
            i += 1
        self.free()
        return stack[-1][0] == len(word)

    def include(self, pattern: NEPattern) -> bool:
        return self.match(pattern.shape())
