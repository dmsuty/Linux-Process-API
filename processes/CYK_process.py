import random

class ContextFreeGrammar:
    def __init__(
        self,
        nonterms: str,
        terms: str,
        productions: list,
        start: str,
        normalized: bool = False,
    ):
        self.__nonterms = list(nonterms)
        self.__terms = list(terms)
        self.__productions = dict()
        for nonterm, product in productions:
            self.add(nonterm, product)
        self.__start = start
        self.__normalized = normalized

    def is_normalized(self) -> bool:
        return self.__normalized

    def chomsky_form(self):
        # remove non-generative
        # remove unattainable
        # remove mixed products A->aBcDe
        # remove long products A->BCD...
        # remove eps symbols A->eps
        # process eps not s |- eps only s->eps
        # unary products A->B
        if self.is_normalized():
            return
        # TODO

    def add(self, nonterm: str, product: str):
        if nonterm not in self.__productions:
            self.__productions[nonterm] = []
        self.__productions[nonterm].append(product)

    @staticmethod
    def __2d_list(size1: int, size2: int, default=None):
        return [[default] * size2 for i in range(size1)]

    def CYK_find(self, word: str) -> bool:
        self.chomsky_form()
        if word == "":
            return "" in self.__productions[self.__start]
        find = dict()
        for nonterm in self.__nonterms:
            find[nonterm] = ContextFreeGrammar.\
                                        __2d_list(len(word), len(word), False)
        for sublength in range(len(word)):
            for left in range(len(word)):
                for nonterm in self.__nonterms:
                    if sublength == 0:
                        if word[left] in self.__productions[nonterm]:
                            find[nonterm][left][left] = True
                        continue
                    right = left + sublength
                    if right >= len(word):
                        break
                    for production in self.__productions[nonterm]:
                        if len(production) == 2:
                            for middle in range(left, right):
                                nonterm1 = production[0]
                                nonterm2 = production[1]
                                if find[nonterm1][left][middle]\
                                        and find[nonterm2][middle + 1][right]:
                                    find[nonterm][left][right] = True
                                    break
                            if find[nonterm][left][right]:
                                break
        return find[self.__start][0][len(word) - 1]

bbs = ContextFreeGrammar(
    "SATLR",
    "()",
    [
        ("S", ""),
        ("S", "AA"),
        ("S", "LT"),
        ("A", "AA"),
        ("A", "LT"),
        ("T", "SR"),
        ("T", ")"),
        ("L", "("),
        ("R", ")"),
    ],
    "S",
    True,
)

def create_random_string(len: int) -> str:
    return ''.join(random.choice(['(', ')']) for _ in range(len))

cnt = 0
tries = 100
leng = 1_000
for i in range(tries):
    s = create_random_string(leng)
    print(bbs.CYK_find(s))
