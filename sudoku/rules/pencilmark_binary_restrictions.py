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
                first,second = sorted(x.short for x in hv)
                puzzle.describe_inference(f'{v} must be either in {first} or {second}')
                for e in hv:
                    if v not in e.pencil:
                        did_count += 1
                        e.add_pencil_mark(v)

    return did_count

