from typing import Iterator


def key_generator() -> Iterator[str]:
    i = 0
    while True:
        yield str(i)
        i += 1


def is_empty_generator(g: Iterator) -> bool:
    for _ in g:
        return True
    return False


