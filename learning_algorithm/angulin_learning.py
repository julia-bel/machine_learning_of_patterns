from __future__ import annotations
from typing import List, Iterator, Optional, Tuple, Any
from itertools import product

from pattern.pattern import NEPattern, NEVariable


def optimal_generate_rec_patterns():
    '''
    1) Проверяем все образцы длины 2
    2) Выбираем все, которые распознают все слова выборки
    3) Порождаем возможные подстановки длины 2 на какую-нибудь переменную очередного тестового образца
    и проверяем только их результаты на распознавание слов выборки
    '''
    pass


def generate_rec_patterns(words: List[str], length: int) -> List[NEPattern]:

    def get_alphabet() -> List[str]:
        chars = set()
        for word in words:
            for char in word:
                chars.add(char)
        return sorted(list(chars))

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
    alphabet = get_alphabet()
    for i in range(length, 1, -1):
        patterns = generate_patterns(i)
        for pattern in patterns:
            if all([pattern.match(word) for word in words]):
                result.append(pattern)
        if len(result):
            break
    return result if len(result) else [NEPattern([NEVariable(f"x{i}") for i in range(length)])]


def find_min_pattern(patterns: List[NEPattern]) -> Optional[NEPattern]:
    for p1 in patterns:
        if all([p2.include(p1) for p2 in patterns if p1 != p2]):
            return p1


def angulin_algorithm(words: List[str]) -> Optional[NEPattern]:
    min_length = min([len(word) for word in words])
    patterns = generate_rec_patterns(words, min_length)
    max_length = max([len(pattern) for pattern in patterns])
    max_patterns = [pattern for pattern in patterns if len(pattern) == max_length]
    return find_min_pattern(max_patterns)
