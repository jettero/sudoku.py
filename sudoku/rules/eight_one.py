#!/usr/bin/env python
# coding: utf-8

from sudoku.rules import hookimpl
from sudoku.const import ELEMENT_VALUES as EV
from sudoku.tools import box_col_row

SEV = set(EV)


@hookimpl
def main(puzzle, opts=set()):
    did_count = 0

    for e in puzzle:
        if e.value:
            continue
        can_be = SEV
        for box in box_col_row(puzzle, e):
            can_be -= set(_e.value for _e in box if _e.value)
        if len(can_be) == 1:
            e.value, = can_be
        else:
            e.set_center_marks(*can_be)

    return did_count
