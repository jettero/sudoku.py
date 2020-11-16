#!/usr/bin/env python
# coding: utf-8

import re

from sudoku import COLUMN_NUMBERS, ROW_NUMBERS
from sudoku.tools import PYTR

BN = (
    None,
    (None, 1, 1, 1, 2, 2, 2, 3, 3, 3),
    (None, 1, 1, 1, 2, 2, 2, 3, 3, 3),
    (None, 1, 1, 1, 2, 2, 2, 3, 3, 3),
    (None, 4, 4, 4, 5, 5, 5, 6, 6, 6),
    (None, 4, 4, 4, 5, 5, 5, 6, 6, 6),
    (None, 4, 4, 4, 5, 5, 5, 6, 6, 6),
    (None, 7, 7, 7, 8, 8, 8, 9, 9, 9),
    (None, 7, 7, 7, 8, 8, 8, 9, 9, 9),
    (None, 7, 7, 7, 8, 8, 8, 9, 9, 9),
)


def test_rows_iter(empty_puzzle):
    """ if we stringify a row we get something like:
        Row[E(b1c1r2) E(b1c2r2) E(b1c3r2) E(b2c4r2) E(b2c5r2) E(b2c6r2)<5> E(b3c7r2)<4> E(b3c8r2) E(b3c9r2)]
        We can then PYTR to ensure the that correct boxes (b2-3), columns (c1-9) and rows (r2) are in the row.
    """
    r = 1
    for row in empty_puzzle.rows:
        assert PYTR(".*?".join(f"b{BN[r][c]}c{c}r{r}" for c in COLUMN_NUMBERS)) == repr(
            row
        )
        r += 1


def test_cols_iter(empty_puzzle):
    """ if we stringify a column, get something like:
        Col[E(b1c2r1)<1> E(b1c2r2) E(b1c2r3) E(b4c2r4) E(b4c2r5) E(b4c2r6)<7> E(b7c2r7)<5> E(b7c2r8) E(b7c2r9)]
        We can then PYTR to ensure it's built correctly.
    """
    c = 1
    for col in empty_puzzle.cols:
        assert PYTR(".*?".join(f"b{BN[r][c]}c{c}r{r}" for r in ROW_NUMBERS)) == repr(
            col
        )
        c += 1


def test_boxes_iter(empty_puzzle):
    b = 1
    for box in empty_puzzle.boxes:
        assert PYTR(".*?".join((f"b{b}",) * 9)) == repr(box)
        b += 1

def test_has_things(empty_puzzle):
    empty_puzzle[5,5] = 5
    empty_puzzle[4,2].add_pencil_mark(5,6)
    empty_puzzle[6,2].add_pencil_mark(5,6)
    empty_puzzle[4,8].add_center_mark(5,6)
    empty_puzzle[6,8].add_center_mark(5,6)

    res = empty_puzzle.has(5, inc_val=False, inc_marks=False)
    assert len(res) == 0

    res = empty_puzzle.has(5, inc_val=False, inc_marks=True)
    assert len(res) == 4

    res = empty_puzzle.has(5, inc_val=True, inc_marks=False)
    assert len(res) == 1

    res = empty_puzzle.has(5, inc_val=True, inc_marks=True)
    assert len(res) == 5


