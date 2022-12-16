from __future__ import annotations
from typing import List, Iterator, Optional, Tuple, Any
from itertools import product

from pattern.pattern import NEPattern, NEVariable


def match_all(pattern: NEPattern, words: List[str]) -> bool:
    return all([pattern.match(word) for word in words])


def get_alphabet(words: List[str]) -> List[str]:
    chars = set()
    for word in words:
        for char in word:
            chars.add(char)
    return sorted(list(chars))


def optimal_generate_rec_patterns(words: List[str], length: int) -> List[NEPattern]:
    def substitute_all(pattern: NEPattern, sub: NEPattern) -> Iterator[NEPattern]:
        vars = set()
        for i, value in enumerate(pattern.value):
            if type(value) is NEVariable and value not in vars:
                new_pattern = []
                for v in pattern.value:
                    if v == value:
                        new_pattern += sub.value
                    else:
                        new_pattern.append(v)
                yield NEPattern(new_pattern)
                vars.add(value)

    def generate_bisubs(
            vars: List[NEPattern],
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
        yield NEPattern([NEVariable("x1"), NEVariable("x2")])

    def generate_bipatterns(const: bool = False) -> Iterator[NEPattern]:
        if const:
            for prod in product(alphabet, repeat=2):
                yield NEPattern(list(prod))
        vars = [NEVariable("x1"), NEVariable("x2")]
        for char in alphabet:
            yield NEPattern([char, vars[0]])
            yield NEPattern([vars[0], char])
        yield NEPattern(vars[:1] * 2)
        yield NEPattern(vars)

    '''
        1) Check all patterns of length 2.
        2) Select all that recognize all the words.
        3) Generate possible substitutions of length 2 for some variable of the next test sample 
           and check only their results for word recognition.
    '''

    alphabet = get_alphabet(words)
    bipatterns = generate_bipatterns()
    rec_patterns = []
    for pattern in bipatterns:
        if match_all(pattern, words):
            rec_patterns.append(pattern)

    used = []
    max_length = 2
    while len(rec_patterns):
        pattern = rec_patterns.pop()
        bisubs = generate_bisubs([v for v in pattern.value if type(v) is NEVariable])
        for sub in bisubs:
            for new_pattern in substitute_all(pattern, sub):
                if len(new_pattern) > length or new_pattern in rec_patterns or new_pattern in used:
                    continue
                if match_all(new_pattern, words):
                    max_length = max(len(new_pattern), max_length)
                    rec_patterns.append(new_pattern)
        used.append(pattern)
    return [p for p in used if len(p) == max_length]


def generate_rec_patterns(words: List[str], length: int) -> List[NEPattern]:
    def generate_patterns(length: int) -> Iterator[NEPattern]:
        def get_var_substitution(pattern: Any) -> Tuple:
            result = []
            vars = {}
            i = 1
            for value in pattern:
                if type(value) is NEVariable:
                    prev_i = vars[str(value)]
                    if prev_i is None:
                        vars[str(value)] = i
                        result.append(i)
                        i += 1
                    else:
                        result.append(prev_i)
                else:
                    result.append(0)
            return tuple(result)

        var_subs = set()
        vars = [NEVariable(f"x{i}") for i in range(length - 1)]
        for pattern in product(alphabet + vars, repeat=len(alphabet) + len(vars)):
            sub = get_var_substitution(pattern)
            if sub not in var_subs:
                var_subs.add(sub)
                yield NEPattern(list(pattern))

    result = []
    alphabet = get_alphabet(words)
    for i in range(length, 1, -1):
        patterns = generate_patterns(i)
        for pattern in patterns:
            if match_all(pattern, words):
                result.append(pattern)
        if len(result):
            break
    return result if len(result) else [NEPattern([NEVariable(f"x{i}") for i in range(length)])]


def find_min_pattern(patterns: List[NEPattern]) -> Optional[NEPattern]:
    for p1 in patterns:
        if all([p2.include(p1) for p2 in patterns if p1 != p2]):
            return p1


def angulin_algorithm(words: List[str], optimize: bool = False) -> Optional[NEPattern]:
    min_length = min([len(word) for word in words])
    patterns = optimal_generate_rec_patterns(words, min_length) \
        if optimize else generate_rec_patterns(words, min_length)
    max_length = max([len(pattern) for pattern in patterns])
    max_patterns = [pattern for pattern in patterns if len(pattern) == max_length]
    return find_min_pattern(max_patterns)
