from __future__ import annotations
from typing import Optional
from tqdm import tqdm

from pattern.pattern import NEPattern, NEVariable


def unite(pattern: NEPattern, word: str) -> NEPattern:
    assert len(pattern) == len(word), "incorrect arguments"

    def find_var(i: int, w: str, p: str | NEVariable) -> Optional[NEVariable]:
        for j, (prev_w, prev_p) in enumerate(zip(word[:i], pattern.value[:i])):
            if prev_w == w and prev_p == p:
                return result[j]

    result = []
    for i, (w, p) in enumerate(zip(word, pattern.value)):
        if w == p:
            result.append(w)
        else:
            prev_var = find_var(i, w, p)
            result.append(prev_var if prev_var else NEVariable())
    return NEPattern(result)


def LWA(words: tqdm) -> NEPattern:
    pattern = None
    for word in words:
        if pattern is None or len(pattern) > len(word):
            pattern = NEPattern(list(word))
        elif len(pattern) == len(word):
            pattern = unite(pattern, word)
        words.set_postfix({"pattern": pattern})
    return pattern
