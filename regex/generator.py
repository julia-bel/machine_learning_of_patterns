import random
import string
from typing import Optional, List

"""
GRAMMAR:
    <regex> ::= <conc-regex> <alt> <regex> | <conc-regex>
    <conc-regex> ::= <simple-regex> | <simple-regex><conc-regex>
    <simple-regex> ::= <lbr><regex><rbr><unary>? | letter <unary>?
    <alt> ::= "|"
    <lbr> ::= "("
    <rbr> ::= ")"
    <unary> ::= "*"
"""


class RegexGenerator:
    seed = 0
    cur_regex_length = 0
    cur_star_num = 0
    cur_nesting = 0
    cur_regex = ""

    def __init__(
            self, regex_length: int,
            star_num: int, star_nesting: int,
            alphabet_size: int, alphabet: Optional[List[str]] = None):
        assert regex_length >= 1, "regex length must be > 0"
        self.regex_length = regex_length
        self.star_nesting = 0 if star_nesting < 0 else star_nesting
        self.star_num = 0 if star_num < 0 else star_num
        if alphabet is None:
            if alphabet_size < 1:
                alphabet_size = 1
            self.alphabet = list(string.ascii_lowercase)[:alphabet_size] + \
                            list(string.ascii_uppercase)[:alphabet_size]
        else:
            self.alphabet = alphabet

    def change_seed(self, step: int = 1):
        self.seed += step
        random.seed(self.seed)

    def generate_regex(self) -> str:
        # self.change_seed()
        self.cur_nesting = 0
        self.cur_regex = ""
        self.cur_regex_length = self.regex_length
        self.cur_star_num = self.star_num
        self._generate_regex()
        return self.cur_regex

    # <regex> ::= <n-alt-regex> <alt> <regex> | <conc-regex>
    def _generate_regex(self):
        if self.cur_regex_length < 1:
            return
        if random.randint(0, 1):
            if self.cur_regex_length > 1:
                self.generate_conc_regex()
            if self.cur_regex_length < 1:
                return
            if self.cur_regex_length != 1:
                self.cur_regex += "|"
                self._generate_regex()
        else:
            self.generate_conc_regex()

    # <conc-regex> ::= <simple-regex> | <simple-regex><conc-regex>
    def generate_conc_regex(self):
        if random.randint(0, 1):
            self.generate_simple_regex()
            if self.cur_regex_length < 1:
                return
            self.generate_conc_regex()
        else:
            self.generate_simple_regex()

    # <simple-regex> ::= <lbr><regex><rbr><unary>? | letter <unary>?
    def generate_simple_regex(self, br_prob: int = 7):
        if random.randint(0, 10) > br_prob:
            self.cur_regex += self.random_char()
            if self.cur_star_num:
                star_chance = self.cur_regex_length // self.cur_star_num
                if star_chance < 2:
                    star_chance = 2
                v = random.randint(0, star_chance - 1)
            else:
                v = 1
            if not v and self.cur_star_num > 0 and self.cur_nesting < self.star_nesting:
                self.cur_regex += "*"
                self.cur_star_num -= 1
            self.cur_regex_length -= 1
        else:
            if self.cur_star_num:
                star_chance = self.cur_regex_length // self.cur_star_num
                if self.cur_regex_length > self.cur_star_num:
                    star_chance += self.cur_star_num // self.star_nesting
                else:
                    star_chance += self.cur_regex_length // self.star_nesting
                if star_chance < 2:
                    star_chance += 2
                v = random.randint(0, star_chance - 1)
            else:
                v = 1
            if not v and self.cur_star_num > 0 and self.cur_nesting < self.star_nesting:
                self.cur_star_num -= 1
                self.cur_nesting += 1
            else:
                v = 1
            self.cur_regex += "("
            self._generate_regex()
            self.cur_regex += ")"
            if not v:
                self.cur_regex += "*"
                self.cur_nesting -= 1

    def random_char(self):
        return self.alphabet[random.randint(0, len(self.alphabet) - 1)]
