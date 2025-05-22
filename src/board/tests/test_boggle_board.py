import json

from board.boggle_board import BoggleBoard, get_neighbours
from board.trie import Trie



def test_get_neighbours():
    for i, expected_neighbours in [
        (3, [2, 6, 7]),
        (9, [4, 5, 6, 8, 10, 12, 13, 14])
    ]:
        neighbours = get_neighbours(i)
        neighbours.sort()
        assert neighbours == expected_neighbours


def test_boggle_board_happy_path():
    wordlist = [
        "mind", "bind", "sine", "stares", "dating", "gating", "guides"
    ]
    trie = Trie()
    for word in wordlist:
        trie.add(word)
 
    # M I S U
    # N D E R
    # S T A N
    # D I N G
    
    board = BoggleBoard(letters="MISUNDERSTANDING", trie=trie)

    expected_words= [
        "mind", "stares", "dating"
    ]
    assert set(board.words) == set(expected_words)
    assert board.maximum_possible_score() == 7

    json_output = board.json()
    actual_json = json.loads(json_output)
    assert actual_json["letters"] == "misunderstanding"
    assert set(actual_json["words"]) == set(expected_words)
    assert actual_json["max_score"] == 7


def test_boggle_board_from_random():
    board = BoggleBoard.from_random_distribution()


def test_boggle_board_from_uniform():
    board = BoggleBoard.from_uniform_distribution()