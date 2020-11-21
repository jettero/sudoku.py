#!/usr/bin/env python
# coding: utf-8

from sudoku import ROW_NUMBERS


def test_diag_oopsie(diag_puzzle):
    diag_puzzle[1, 3] = 1
    diag_puzzle[3, 1] = 1
    bad = diag_puzzle.check()

    assert "row 1 contains 2 '1's" in bad
    assert "col 1 contains 2 '1's" in bad
    assert "box 1 contains 3 '1's" in bad
    assert len(bad) == 3
