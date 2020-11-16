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

@pytest.fixture(scope='function')
def five_six_puzzle():
    p = Puzzle()
    p[5,5] = 5
    p[4,2].add_pencil_mark(5,6)
    p[6,2].add_pencil_mark(5,6)
    p[4,8].add_center_mark(5,6)
    p[6,8].add_center_mark(5,6)
    yield p

