from typing import List, Iterator, Optional

from pattern.pattern import NEPattern


def generate_rec_patterns(words: List[str], length: int) -> List[NEPattern]:

    def generate_patterns(length: int) -> Iterator[NEPattern]:
        # TODO: optimal algorithm
        for i in range(length):
            pass
        pass

    result = []
    for i in range(length, 1, -1):
        patterns = generate_patterns(i)
        for pattern in patterns:
            if all([pattern.match(word) for word in words]):
                result.append(pattern)
        if len(result):
            break
    return result


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
