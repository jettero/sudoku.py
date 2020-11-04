#!/usr/bin/env python
# coding: utf-8

import re

from sudoku import COLUMN_NUMBERS, ROW_NUMBERS

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


class PYTR:
    """Assert that a given string meets some expectations."""

    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)

    def __eq__(self, actual):
        return bool(self._regex.search(actual))

    def __repr__(self):
        return self._regex.pattern


def test_rows_iter(empty_grid):
    r = 1
    for row in empty_grid.rows:
        assert PYTR(".*?".join(f"b{BN[r][c]}c{c}r{r}" for c in COLUMN_NUMBERS)) == repr(
            row
        )
        r += 1


def test_cols_iter(empty_grid):
    c = 1
    for col in empty_grid.cols:
        assert PYTR(".*?".join(f"b{BN[r][c]}c{c}r{r}" for r in ROW_NUMBERS)) == repr(
            col
        )
        c += 1


def test_boxes_iter(empty_grid):
    b = 1
    for box in empty_grid.boxes:
        assert PYTR(".*?".join((f"b{b}",) * 9)) == repr(box)
        b += 1
