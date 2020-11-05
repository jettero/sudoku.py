#!/usr/bin/env python
# coding: utf-8

from sudoku.grid import ELEMENT_VALUES as EV
from sudoku.rules import hookimpl

@hookimpl
def human(puzzle):
    did_count = 0

    for e in puzzle:
        if not e.value and len(e.hidden) == 1:
            pm, = e.hidden
            e.value = pm
            did_count += 1

    return did_count
