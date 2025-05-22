from board.trie import Trie


def test_trie_happy_path():
    trie = Trie()

    wordlist = ["aback", "abacus", "boy", "dog", "gold", "golden"]
    for word in wordlist:
        trie.add(word)

    for test_case, expected_is_word, expected_is_substring in [
        ("boy", True, True),
        ("cat", False, False),
        ("gol", False, True),
        ("gold", True, True),
        ("golde", False, True),
        ("golden", True, True),
    ]:
        result = trie.contains(test_case)
        assert result.is_word == expected_is_word
        assert result.is_substring == expected_is_substring
        assert trie.is_word(test_case) == expected_is_word
        assert trie.is_substring(test_case) == expected_is_substring


def test_trie_contains_using_last_node():
    trie = Trie()

    wordlist = ["gold", "golds", "golden", "goldfish", "goldenrod"]
    for word in wordlist:
        trie.add(word)

    result = trie.contains("gold")
    d_node = result.last_node

    result = trie.contains("en", last_node=d_node)
    assert result.is_word == True

    result = trie.contains("e", last_node=d_node)
    assert result.is_substring == True
    assert result.is_word == False
    e_node = result.last_node

    result = trie.contains("n", last_node=e_node)
    assert result.is_word == True

    result = trie.contains("ns", last_node=e_node)
    assert result.is_word == False
    assert result.is_substring == False

