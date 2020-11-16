#!/usr/bin/env python
# coding: utf-8

import pytest

from sudoku import Puzzle
from sudoku import get_puzzles
from sudoku import ROW_NUMBERS

@pytest.fixture(scope='function')
def puzzles():
    yield tuple(get_puzzles())

@pytest.fixture(scope='function')
def p0(puzzles):
    yield puzzles[0]

@pytest.fixture(scope='function')
def empty_puzzle():
    yield Puzzle()

@pytest.fixture(scope='function')
def diag_puzzle():
    p = Puzzle()
    for x in ROW_NUMBERS:
        p[x,x] = x
    yield p
