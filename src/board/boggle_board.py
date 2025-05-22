import json
import random

from board.shared import frequency
from board.trie import get_default_trie, ALPHABET

WORD_LEN_THRESHOLD = 3



def get_neighbours(idx):
    row = int(idx / 4)
    col = idx % 4
    neighbours = []
    for r in range(max(row - 1, 0), (min(row + 1, 3) + 1)):
        for c in range(max(col - 1, 0), (min(col + 1, 3) + 1)):
            if (r, c) != (row, col):
                neighbours.append(r * 4 + c)
    return neighbours


def score(word):
    word_len = len(word)
    if word_len < 3:
        return 0
    if word_len >= 3 and word_len <= 4:
        return 1
    if word_len == 5:
        return 2
    if word_len == 6:
        return 3
    if word_len == 7:
        return 5
    if word_len > 7:
        return 11


class BoggleBoard:
    def __init__(self, letters, trie=None):
        self.letters = letters.lower()
        if trie is None:
            trie = get_default_trie()

        self.trie = trie
        self._words = None
        assert len(self.letters) == 16

    def traverse(self, i, last_visited_trie_node=None, visited=None):
        """
        There are two trees we are traversing, the boggleboard and the trie
        i = index of the letter box of the board
        last_visited_trie_node =  if we are traversing midway through a word, passing in the
                                  last-visited trie node we have traversed saves traversing the trie again
        visited = letter boxes we have already visited
        """
        visited = visited or []
        letter_at_current_node = self.letters[i]

        result = self.trie.contains(letter_at_current_node, last_visited_trie_node)

        wordlist = []
        if result.is_word:
            word = "".join([self.letters[v] for v in visited + [i]])
            wordlist.append(word)

        if not result.is_substring:
            return wordlist
        else:
            for n in get_neighbours(i):
                if n in visited:
                    continue
                words = self.traverse(n, result.last_node, visited=visited + [i])
                wordlist.extend(words)
            return wordlist

    def _solve(self):
        """
        M I S U
        N D E R
        S T A N
        D I N G
        """
        words = []
        for i, l in enumerate(self.letters):
            new_words = self.traverse(i)
            new_words = [word for word in new_words if len(word) >= WORD_LEN_THRESHOLD]
            words.extend(new_words)
        self._words = list(set(words))

    @property
    def words(self):
        if self._words is None:
            self._solve()
        return self._words

    @classmethod
    def from_random_distribution(cls, trie=None):
        letters = random.choices(ALPHABET, weights=frequency, k=16)
        return cls("".join(letters), trie)

    @classmethod
    def from_uniform_distribution(cls, trie=None):
        letters = random.choices(ALPHABET, k=16)
        return cls("".join(letters), trie)

    def print(self):
        output = ""
        for i, l in enumerate(self.letters):
            output = output + " " + l.upper()
            if i > 0 and (i + 1) % 4 == 0:
                output = output + "\n"

        print(output)

    def maximum_possible_score(self):
        return sum(score(word) for word in self.words)

    def json(self):
        return json.dumps(
            {
                "letters": self.letters,
                "words": self.words,
                "max_score": self.maximum_possible_score()
            }
        )
