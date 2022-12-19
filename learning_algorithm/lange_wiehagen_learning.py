from __future__ import annotations
from typing import Optional, List

from pattern.pattern import NEPattern, NEVariable


def unite(pattern: NEPattern, word: str) -> NEPattern:
    assert len(NEPattern) == len(word), "incorrect components"

    def find_var(i: int, w: str, p: str | NEVariable) -> Optional[NEVariable]:
        for j, prev_w, prev_p in enumerate(zip(word[:i], pattern.value[:i])):
            if prev_w == w and prev_p == p:
                return result[j]

    result = []
    n = 0
    for i, w, p in enumerate(zip(word, pattern.value)):
        if w == str(p):
            result.append(w)
        else:
            prev_var = find_var(i, w, p)
            if prev_var is not None:
                result.append(prev_var)
            else:
                new_var = NEVariable(f"x{n}")
                new_var.substitute(w)
                result.append(new_var)
                n += 1
    return NEPattern(result)


def LWA(words: List[str]) -> NEPattern:
    pattern = words[0]
    for word in words[1:]:
        if len(pattern) > len(word):
            pattern = word
        elif len(pattern) == len(word):
            pattern = unite(pattern, word)
    return pattern if type(pattern) is NEPattern else NEPattern([pattern])

