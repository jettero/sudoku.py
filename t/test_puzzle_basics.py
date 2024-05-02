#!/usr/bin/env python
# coding: utf-8

import re
import pytest
from sudoku import COLUMN_NUMBERS, ROW_NUMBERS, Puzzle
from sudoku.tools import PYTR
from sudoku.element import CELL_WIDTH
from sudoku.box import Box

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
        assert PYTR(".*?".join(f"b{BN[r][c]}r{r}c{c}" for c in COLUMN_NUMBERS)) == repr(
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
        assert PYTR(".*?".join(f"b{BN[r][c]}r{r}c{c}" for r in ROW_NUMBERS)) == repr(
            col
        )
        c += 1


def test_boxes_iter(empty_puzzle):
    b = 1
    for box in empty_puzzle.boxes:
        assert PYTR(".*?".join((f"b{b}",) * 9)) == repr(box)
        b += 1


def test_puzzle_has_things(p_45m):
    res = p_45m.has(5, inc_val=False, inc_pencil=False)
    assert len(res) == 0

    res = p_45m.has(5, inc_val=False, inc_pencil=True)
    assert len(res) == 3

    res = p_45m.has(5, inc_val=False, inc_center=True)
    assert len(res) == 2

    res = p_45m.has(5, inc_val=True, inc_pencil=False)
    assert len(res) == 6

    res = p_45m.has(5, inc_val=True, inc_pencil=True)
    assert len(res) == 9

    res = p_45m.has(5, inc_val=True, inc_center=True)
    assert len(res) == 8


def test_rows_have_things(p_45m):
    res = p_45m.rows[4].has(5, inc_val=False, inc_pencil=False)
    assert len(res) == 0

    res = p_45m.rows[4].has(5, inc_val=False, inc_pencil=True)
    assert len(res) == 2

    res = p_45m.rows[4].has(5, inc_val=True, inc_pencil=False)
    assert len(res) == 0

    res = p_45m.rows[4].has(5, inc_val=True, inc_pencil=True)
    assert len(res) == 2

    res = p_45m.rows[5].has(5, inc_val=False, inc_pencil=True)
    assert len(res) == 0

    res = p_45m.rows[5].has(5, inc_val=True, inc_pencil=False)
    assert len(res) == 1

    res = p_45m.rows[5].has(5, inc_val=True, inc_pencil=True)
    assert len(res) == 1

    for row in p_45m.rows:
        if row.has(5, inc_val=True, inc_pencil=False):
            assert row.has(5, inc_val=False, inc_pencil=True) == set()

        if row.has(5, inc_val=False, inc_pencil=True):
            assert row.has(5, inc_val=True, inc_pencil=False) == set()


def test_silly_idx(empty_puzzle):
    with pytest.raises(IndexError):
        empty_puzzle.rows[0]
    with pytest.raises(IndexError):
        empty_puzzle[1] = 4

def test_reset(empty_puzzle):
    empty_puzzle[1,1].given = 5
    empty_puzzle[1,2].value = 4
    empty_puzzle[2,1].add_pencil_marks(6,7)
    empty_puzzle[2,2].add_center_marks(8,9)

    assert empty_puzzle[1,1].value == 5
    assert empty_puzzle[1,2].value == 4

    assert empty_puzzle[2,1].pencil == {6,7}
    assert empty_puzzle[2,2].center == {8,9}

    empty_puzzle.reset()

    assert empty_puzzle[1,1].value == 5
    assert empty_puzzle[1,2].value is None

    assert empty_puzzle[2,1].pencil == set()
    assert empty_puzzle[2,2].center == set()

def test_pencil_setter(empty_puzzle):
    empty_puzzle[2,1].add_pencil_marks(6,7)
    assert empty_puzzle[2,1].pencil == {6,7}
    empty_puzzle[2,1].set_pencil_marks(1,2)
    assert empty_puzzle[2,1].pencil == {1,2}

def test_center_setter(empty_puzzle):
    empty_puzzle[2,1].add_center_marks(6,7)
    assert empty_puzzle[2,1].center == {6,7}
    empty_puzzle[2,1].set_center_marks(1,2)
    assert empty_puzzle[2,1].center == {1,2}

def test_rows(empty_puzzle):
    p = Puzzle()
    r1 = p[1]
    r7 = p[7]
    assert p[1].short == 'row 1'
    assert p[7].short == 'row 7'

def test_repr(empty_puzzle, p1, p2, p3):
    for p in (empty_puzzle, p1, p2, p3):
        for line in str(p).splitlines():
            assert len(line) == CELL_WIDTH*9 + 2*9 + (9-1) + 2
            # length of line is cell_width + two spaces + dividers between + two borders

def test_box_rows(p1):
    br = list(p1.box_rows)
    assert len(br) == 3 # three rows
    assert len(br[0]) == 3 # three boxes per row
    assert isinstance(br[0][0], Box)

def test_box_cols(p1):
    bc = list(p1.box_cols)
    assert len(bc) == 3 # three columns
    assert len(bc[0]) == 3 # thee boxes per column
    assert isinstance(bc[0][0], Box)

def test_pids(p7):
    q7 = p7.clone()

    assert p7.pid == 7
    assert q7.pid == p7.pid

    assert p7.short == "Puzzle(7)"
    assert q7.short == "Puzzle(7)"
