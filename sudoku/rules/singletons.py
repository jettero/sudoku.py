#!/usr/bin/env python
# coding: utf-8

from sudoku.grid import ELEMENT_VALUES as EV
from sudoku.rules import hookimpl

@hookimpl
def human(puzzle):
    did_count = 0

    for e in puzzle:
        if e.value:
            continue
        if len(e.hidden) == 1:
            v, = e.hidden
            puzzle.describe_inference(f'{e.short} can only be {v}')
            e.value = v
            did_count += 1

    for v in EV:
        for word,boxes in (('row', puzzle.rows), ('col', puzzle.cols), ('box', puzzle.boxes)):
            for box in boxes:
                s = set(x for x in box if x.value == v or v in x.hidden)
                if len(s) == 1:
                    e, = s
                    if e.value:
                        continue
                    a = getattr(e, word)
                    puzzle.describe_inference(f'{e.short} is the only place {v} can be in {word} {a}')
                    e.value = v
                    did_count += 1

    return did_count
