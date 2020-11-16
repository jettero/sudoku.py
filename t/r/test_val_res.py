#!/usr/bin/env python
# coding: utf-8

from sudoku.tools import pos_iter
from sudoku.rules.value_restrictions import main as vr_main

def has_3_pencil_mark(p):
    for e in p:
        if 3 in e.pencil:
            yield e

def test_value_restrictions(p0):
    pm = p0.has(3, inc_val=False)
    assert len(pm) == 0

    vr_main(p0,{})
    pm = tuple(has_3_pencil_mark(p0))
    assert len(pm) == 4
