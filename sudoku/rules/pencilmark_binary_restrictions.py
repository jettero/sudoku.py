#!/usr/bin/env python
# coding: utf-8

from sudoku.grid import ELEMENT_VALUES as EV
from sudoku.rules import hookimpl

@hookimpl
def human(puzzle):
    did_count = 0

    for box in puzzle.boxes:
        for v in EV:
            hv = set(x for x in box if v in x.hidden)
            if len(hv) == 2:
                for e in hv:
                  e.add_pencil_mark(v)

    return did_count

