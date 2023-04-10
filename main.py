from argparse import ArgumentParser
from typing import List, Dict, Optional
from tqdm import tqdm

from learning_algorithm.angluin_learning import angluin_algorithm
from learning_algorithm.lange_wiehagen_learning import LWA
from pattern.pattern import NEPattern


def split_by_len(words: List[str]) -> Dict[int, List[str]]:
    result = {}
    for word in words:
        word_len = len(word)
        if word_len in result:
            result[word_len].append(word)
        else:
            result[word_len] = [word]
    return result


def learn(words: List[str], optimize: bool = False) -> Optional[NEPattern]:
    def add_pattern(pattern: NEPattern):
        nonlocal patterns
        new_patterns = [pattern]
        while len(patterns) and not patterns[-1].include(pattern):
            pattern = angluin_algorithm(
                [patterns.pop().shape("x"), pattern.shape("y")],
                optimize=optimize)
            new_patterns.append(pattern)
        patterns += new_patterns[::-1]

    map_words = split_by_len(words)
    patterns = []
    for length in sorted(map_words):
        words = tqdm(map_words[length])
        words.set_description(f"Length={length}")
        add_pattern(LWA(words))
    return patterns[0]


if __name__ == "__main__":
    parser = ArgumentParser(description="Patterns learning")
    parser.add_argument(
        "-d", "--dataset_path",
        default="datasets/dataset.csv",
        help="Path to the file with words for learning.",
    )
    parser.add_argument(
        "-o", "--optimize", action="store_true",
        help="Whether to use optimization of Angluin's algorithm.",
    )
    args = parser.parse_args()

    with open(args.dataset_path, mode="r", encoding="utf-8") as file:
        dataset = [data for data in file.read().split("\n") if data]

    print(f"Result: {learn(dataset, optimize=args.optimize)}")
