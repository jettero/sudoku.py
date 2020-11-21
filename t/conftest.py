#!/usr/bin/env python
# coding: utf-8

import os
import logging
import pytest

from sudoku import Puzzle, get_puzzles, ROW_NUMBERS, solve

log = logging.getLogger(__name__)

tdir = os.path.dirname(__file__)
rdir = os.path.dirname(tdir)
adir = os.path.join(tdir, "asset")

already_spammed = set()


def spam(name, puzzle):
    if name not in already_spammed:
        log.debug("%s:\n%s", name, puzzle)
        already_spammed.add(name)


@pytest.fixture(scope="function")
def puzzles():
    yield tuple(get_puzzles())


@pytest.fixture(scope="function")
def p0(puzzles):
    yield puzzles[0]


@pytest.fixture(scope="function")
def p1(puzzles):
    yield puzzles[1]


@pytest.fixture(scope="function")
def empty_puzzle():
    yield Puzzle()


@pytest.fixture(scope="function")
def diag_puzzle():
    p = Puzzle()
    for x in ROW_NUMBERS:
        p[x, x] = x
    yield p


def get_single_puzzle(short):
    for dir in (adir, tdir, rdir):
        file = os.path.join(dir, f"{short}.txt")
        if os.path.isfile(file):
            (p,) = get_puzzles(file)
            spam(short, p)
            return p


@pytest.fixture(scope="function")
def p_1t9m4():
    p = get_single_puzzle("p_1t9m4")
    yield p


@pytest.fixture(scope="function")
def p_45():
    p = get_single_puzzle("p_45")
    yield p


@pytest.fixture(scope="function")
def p_45m(p_45):
    p = p_45.clone()

    p[2, 1].add_center_mark(4, 5)
    p[2, 3].add_center_mark(4, 5)

    p[4, 1].add_pencil_mark(5)
    p[4, 3].add_pencil_mark(5)

    p[6, 8].add_pencil_mark(4)
    p[6, 9].add_pencil_mark(4)

    p[7, 5].add_pencil_mark(4)
    p[8, 5].add_pencil_mark(4)
    p[9, 5].add_pencil_mark(4)

    p[7, 7].add_pencil_mark(5)

    spam("p_45m", p)

    yield p
