from dataclasses import dataclass
import random

from board.boggle_board import BoggleBoard
from board.trie import get_default_trie


def combine(parent_a, parent_b):
    if parent_a.trie != parent_b.trie:
        raise ValueError("cannot combine two boards with different tries")
    new_sequence = list(parent_b.letters)
    for _ in range(2):
        start = random.randint(0, 15)
        for i in range(start,  start + 4):
            new_sequence[i % 16] = parent_a.letters[i % 16]
            
    return BoggleBoard(''.join(new_sequence), parent_a.trie)


def boggle_genetic_algo(num_individuals=20, num_generations=30, trie=None):
    if trie is None:
        trie = get_default_trie()
    individuals = [
        BoggleBoard.from_random_distribution(trie=trie) for _ in range(num_individuals)
    ]


    best_so_far = individuals[0]
    best_score_so_far = 0
    for _ in range(num_generations):
        fitness = [
            individual.maximum_possible_score() for individual in individuals
        ]

        for individual, score in zip(individuals, fitness):
            if score > best_score_so_far:
                best_so_far = individual
                best_score_so_far = score

        # print("best score so far:", best_score_so_far)
        # best_so_far.print()
        new_generation = []
        for _ in range(num_individuals):
            parent_a, parent_b = random.choices(individuals, weights=fitness, k=2)

            child = combine(parent_a, parent_b)
            new_generation.append(child)
        individuals = new_generation

    return best_so_far
