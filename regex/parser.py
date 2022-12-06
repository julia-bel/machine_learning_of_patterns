from typing import List

from regex.const import L_PAR, R_PAR, KLEENE_STAR, ALTERNATIVE
from regex.regex import BaseRegex, StarRegex, Regex, BracketRegex, AlternativeRegex


class RegexParser:

    def __init__(self, value: str, height: List[int]):
        self.value = list(value[::-1])
        self.height = height[::-1]
        self.parenthesis_count = 0

    def peek_char(self) -> str:
        return self.value[-1] if self.value else ""

    def next_char(self) -> str:
        return self.value.pop() if self.value else ""

    def next_height(self) -> int:
        return self.height.pop() if self.height else ""

    def parse(self) -> Regex:

        def add2parsed(regex: str):
            if regex:
                parsed.append(BaseRegex(regex))

        parsed = []
        curr_regex = ""
        alternative = 0
        while len(self.value):
            char = self.next_char()
            if char == L_PAR:
                self.parenthesis_count += 1
                add2parsed(curr_regex)
                curr_regex = ""
                parsed.append(self.parse())
            elif char == R_PAR:
                self.parenthesis_count -= 1
                assert self.parenthesis_count > -1, "invalid parenthesis"
                add2parsed(curr_regex)
                if alternative:
                    assert len(parsed) > alternative, "invalid alternative expression"
                    if len(parsed) != alternative + 1:
                        parsed = parsed[:alternative] + [BracketRegex(parsed[alternative:])]
                    return AlternativeRegex(parsed)
                return BracketRegex(parsed)
            elif char == ALTERNATIVE:
                add2parsed(curr_regex)
                curr_regex = ""
                assert len(parsed) > alternative, "invalid alternative expression"
                if len(parsed) != alternative + 1:
                    parsed = parsed[:alternative] + [BracketRegex(parsed[alternative:])]
                alternative += 1
            elif char == KLEENE_STAR:
                if curr_regex:
                    add2parsed(curr_regex[:-1])
                    parsed.append(StarRegex(BaseRegex(curr_regex[-1]), self.next_height()))
                    curr_regex = ""
                else:
                    assert len(parsed), "invalid operation"
                    parsed[-1] = StarRegex(parsed[-1], self.next_height())
            else:
                curr_regex += char
        assert self.parenthesis_count == 0, "invalid parenthesis"
        add2parsed(curr_regex)
        if alternative:
            assert len(parsed) > alternative, "invalid alternative expression"
            if len(parsed) != alternative + 1:
                parsed = parsed[:alternative] + [BracketRegex(parsed[alternative:])]
            return AlternativeRegex(parsed)
        return parsed[0] if len(parsed) == 1 else BracketRegex(parsed)
