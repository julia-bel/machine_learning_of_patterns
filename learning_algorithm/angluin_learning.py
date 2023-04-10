from __future__ import annotations
from typing import List, Iterator, Optional
from itertools import product

from pattern.pattern import NEPattern, NEVariable


def match_all(pattern: NEPattern, words: List[str | List[str]]) -> bool:
    return all([pattern.match(word) for word in words])


def get_alphabet(words: List[str | List[str]]) -> List[str]:
    return sorted(list({char for word in words for char in word}))


def optimal_generate_rec_patterns(words: List[str | List[str]], length: int) -> List[NEPattern]:
    def substitute_all(pattern: NEPattern, sub: NEPattern) -> Iterator[NEPattern]:
        vars = set()
        for i, value in enumerate(pattern.value):
            if isinstance(value, NEVariable) and value not in vars:
                new_pattern = []
                for v in pattern.value:
                    if v == value:
                        new_pattern += sub.value
                    else:
                        new_pattern.append(v)
                yield NEPattern(new_pattern)
                vars.add(value)

    def generate_bisubs(
            vars: List[NEVariable],
            const: bool = True) -> Iterator[NEPattern]:
        if const:
            for prod in product(alphabet, repeat=2):
                yield NEPattern(list(prod))
        for char in alphabet:
            for var in vars:
                yield NEPattern([char, var])
                yield NEPattern([var, char])
        for prod in product(vars, repeat=2):
            yield NEPattern(list(prod))
        yield NEPattern([NEVariable(), NEVariable()])

    def generate_bipatterns(const: bool = False) -> Iterator[NEPattern]:
        if const:
            for prod in product(alphabet, repeat=2):
                yield NEPattern(list(prod))
        vars = [NEVariable(), NEVariable()]
        for char in alphabet:
            yield NEPattern([char, vars[0]])
            yield NEPattern([vars[0], char])
        yield NEPattern(vars[:1] * 2)
        yield NEPattern(vars)

    """
        1) Check all patterns of length 2.
        2) Select all that recognize all the words.
        3) Generate possible substitutions of length 2 for some variable of the next test sample 
           and check only their results for word recognition.
    """

    alphabet = get_alphabet(words)
    bipatterns = generate_bipatterns()
    rec_patterns = [pattern for pattern in bipatterns if match_all(pattern, words)]
    used = []
    max_length = 2
    while len(rec_patterns):
        pattern = rec_patterns.pop()
        bisubs = generate_bisubs([v for v in pattern.value if isinstance(v, NEVariable)])
        for sub in bisubs:
            for new_pattern in substitute_all(pattern, sub):
                if len(new_pattern) > length or new_pattern in rec_patterns or new_pattern in used:
                    continue
                if match_all(new_pattern, words):
                    max_length = max(len(new_pattern), max_length)
                    rec_patterns.append(new_pattern)
        used.append(pattern)
    return [p for p in used if len(p) == max_length]


def generate_rec_patterns(words: List[str | List[str]], length: int) -> List[NEPattern]:
    def generate_patterns(length: int) -> Iterator[NEPattern]:
        subs = set()
        vars = [NEVariable() for _ in range(length)]
        for sub in product(alphabet + vars, repeat=length):
            pattern = NEPattern(list(sub))
            sub = tuple(pattern.shape())
            if sub not in subs:
                subs.add(sub)
                yield pattern

    result = []
    alphabet = get_alphabet(words)
    for i in range(length, 1, -1):
        patterns = generate_patterns(i)
        for pattern in patterns:
            if match_all(pattern, words):
                result.append(pattern)
        if len(result):
            break
    return result


def find_min_pattern(patterns: List[NEPattern]) -> Optional[NEPattern]:
    for p1 in patterns:
        if all([not p1.include(p2) for p2 in patterns if p1 != p2]):
            return p1


def angluin_algorithm(words: List[str | List[str]], optimize: bool = False) -> Optional[NEPattern]:
    min_length = min([len(word) for word in words])
    patterns = optimal_generate_rec_patterns(words, min_length) \
        if optimize else generate_rec_patterns(words, min_length)
    return find_min_pattern(patterns)
