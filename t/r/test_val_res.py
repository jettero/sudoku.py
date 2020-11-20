#!/usr/bin/env python
# coding: utf-8

import logging

from sudoku.tools import pos_iter
from sudoku.rules.value_restrictions import main as vr_main

log = logging.getLogger(__name__)

def has_pencil_mark(v, p):
    for e in p:
        if 3 in e.pencil:
            yield e

def test_value_restrictions(p0):
    pm = p0.has(3, inc_val=False)
    assert len(pm) == 0

    vr_main(p0,{})
    pm = tuple(has_pencil_mark(3, p0))
    assert len(pm) == 4

def test_value_restrictions(p1):
    pm = p1.has(3, inc_val=False)
    assert len(pm) == 0

    pm = tuple(has_pencil_mark(3, p1))
    assert len(pm) == 0

    while vr_main(p1,{}):
        pass

    log.debug(p1)

    pm = p1.has(3, inc_val=False, inc_marks=True)
    assert len(pm) == 6

    pm = tuple(has_pencil_mark(3, p1))
    assert len(pm) == 6

