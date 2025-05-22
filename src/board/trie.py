from collections import namedtuple

TrieSearchResult = namedtuple(
    "TrieSearchResult", ["is_word", "is_substring", "last_node"]
)

ALPHABET = "abcdefghijklmnopqrstuvwxyz"
_SOWPODS_TRIE = None


def get_sowpods_trie():
    return Trie.from_text_file("src/board/sowpods.txt")


def get_default_trie():
    global _SOWPODS_TRIE
    if _SOWPODS_TRIE is None:
        _SOWPODS_TRIE = get_sowpods_trie()
    return _SOWPODS_TRIE


class Node:
    def __init__(self):
        self.children = [None] * 26
        self.isleaf = False

    def print(self, pst=None):
        pst = pst or ""
        children = [(i, c) for i, c in enumerate(self.children) if c is not None]
        if self.isleaf:
            print(pst)
        for i, c in children:
            newstring = pst + ALPHABET[i]
            c.print(newstring)


class Trie:
    def __init__(self):
        self.head = Node()

    def add(self, word):
        children = self.head.children
        for letter in word:
            i = ALPHABET.index(letter)

            if children[i]:
                last_node = children[i]
                children = children[i].children
                continue
            else:
                children[i] = Node()
                last_node = children[i]
                children = children[i].children

        last_node.isleaf = True

    def is_word(self, word):
        result = self.contains(word)
        return result.is_word

    def contains(self, token, last_node=None):
        last_node = last_node or self.head
        children = last_node.children
        for letter in token:
            i = ALPHABET.index(letter)
            if children[i]:
                last_node = children[i]
                children = children[i].children
            else:
                return TrieSearchResult(
                    is_word=False, is_substring=False, last_node=last_node
                )

        return TrieSearchResult(
            is_substring=True, is_word=last_node.isleaf, last_node=last_node
        )

    def is_substring(self, substr):
        result = self.contains(substr)
        return result.is_substring

    def print(self):
        self.head.print()

    @classmethod
    def from_text_file(cls, filename):
        instance = cls()
        with open(filename, "r") as f:
            for l in f:
                word = l.strip()
                instance.add(word)
        return instance


if __name__ == "__main__":
    wordlist = ["aback", "abacus", "boy", "dog", "gold", "golden"]
    trie = Trie()
    for word in wordlist:
        trie.add(word)
    trie.print()
    for test_case, expected in [
        ("boy", True),
        ("cat", False),
        ("gol", False),
        ("gold", True),
        ("golden", True),
    ]:
        print(trie.is_word(test_case), expected)

    for test_case, expected in [("gol", True), ("bra", False)]:
        print(trie.is_word(test_case), expected)

    last_node = None
    for letter in "golden":
        print(letter)
        result = trie.contains(letter, last_node)
        print(result)
        if not result.is_substring:
            print("wrong")
        last_node = result.last_node
    print("---------")
    last_node = None
    for letter in "botch":
        print(letter)
        result = trie.contains(letter, last_node)
        print(result)
        last_node = result.last_node
