from regex.generator import RegexGenerator
from regex.parser import RegexParser

if __name__ == "__main__":
    regex_length = 20
    star_num = 5
    star_nesting = 5
    alphabet_size = 26
    reg_gen = RegexGenerator(regex_length, star_num, star_nesting, alphabet_size)
    for _ in range(10):
        regex_str = reg_gen.generate_regex()
        print(regex_str)
        parser = RegexParser(regex_str, [100] * star_num)
        regex = parser.parse()
        nfa = regex.to_nfa()
        dfa = nfa.to_dfa()
        data = {
            "regex": regex,
            "nfa": nfa,
            "dfa": dfa
        }
        word = "asaaabb"
        for k, v in data.items():
            v.plot().render(f"visualization/{k}.gv", format="png").replace('\\', '/')
            print(f"{k}: {v.match(word)}")
