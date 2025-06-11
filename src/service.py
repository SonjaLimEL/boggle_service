import importlib
import asyncio
from typing import Union
from celery.result import AsyncResult
import celery.states

from board.boggle_board import BoggleBoard
from board.trie import get_default_trie
from board.optimizer import boggle_genetic_algo
from shared import BoardGenerationOptions
from settings import Settings


class CeleryTaskException(Exception):
    pass


class CeleryTaskUnreadyException(Exception):
    pass


class CeleryNotEnabled(Exception):
    pass


def in_process_optimized_board_generation():
    return boggle_genetic_algo()

optimized_board_generation_fn = in_process_optimized_board_generation
my_module = None

if Settings.USE_CELERY:
    my_module = importlib.import_module('worker')
    def celery_optimized_board_generation():
        task = my_module.get_optimized_board.delay()
        return task.id

    optimized_board_generation_fn = celery_optimized_board_generation


def get_board(generation_method=None, letters=None) -> Union[BoggleBoard, int]:
    if letters is not None:
        return BoggleBoard(letters)

    if generation_method is None:
        generation_method = BoardGenerationOptions.RANDOM

    if generation_method == BoardGenerationOptions.RANDOM:
        return BoggleBoard.from_random_distribution()
    elif generation_method == BoardGenerationOptions.OPTIMIZED:
        return optimized_board_generation_fn()
    elif generation_method == BoardGenerationOptions.UNIFORM:
        return BoggleBoard.from_uniform_distribution()
    else:
        raise ValueError("Unknown method of creating board: {generation_method}") 


def get_board_from_redis(task_id):
    if not Settings.USE_CELERY:
        raise CeleryNotEnabled
    res = my_module.get_optimized_board.AsyncResult(task_id)

    if res.state in celery.states.EXCEPTION_STATES:
        raise CeleryTaskException("task state: {res.state}")
    if res.state in celery.states.READY_STATES:
        return res.get()
    elif res.state in celery.states.UNREADY_STATES:
        raise CeleryTaskUnreadyException()


