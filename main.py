from regex.parser import RegexParser


if __name__ == "__main__":
    parser = RegexParser("s(a*b)b*f*", [3, 1, 7])
    regex = parser.parse()
    nfa = regex.to_nfa()
    dfa = nfa.to_dfa()

    data = {
        "regex": regex,
        "nfa": nfa,
        "dfa": dfa
    }

    word = "saaabbf"
    for k, v in data.items():
        v.plot().render(f"visualization/{k}.gv", format="png").replace('\\', '/')
        print(f"{k}: {v.match(word)}")
