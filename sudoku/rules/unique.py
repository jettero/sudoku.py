#!/usr/bin/env python
# coding: utf-8
"""
Go through all cells, if there's a .value, then remove that center mark from
each cell in the col, row and box.
"""

from sudoku.rules import hookimpl
from sudoku.const import ELEMENT_VALUES as EV
from sudoku.tools import elements_in_box_col_row

class RestartTop(Exception):
    pass

@hookimpl
def init(puzzle, opts=set()):
    for e in puzzle:
        if not e.value:
            e.set_center_marks(*EV)

@hookimpl
def main(puzzle, opts=set()):
    last_pass_dc = -1
    did_count = 0

    while not puzzle.broken and last_pass_dc != did_count:
        last_pass_dc = did_count
        try:
            for e in puzzle:
                if e.value:
                    continue
                v_in_row_col_box = set(x.value for x in elements_in_box_col_row(puzzle, e) if x.value)
                before = e.center
                e.remove_center_marks(*v_in_row_col_box)
                after = e.center
                if after != before:
                    did_count += 1
                    if not after:
                        puzzle.broken = True
                        puzzle.describe_inference(f"this puzzle is broken. {e} can't be any value.", __name__)
                    if len(after) == 1:
                        v, = after
                        e.value = v
                        puzzle.describe_inference(f"{e} must be {v} by uniqueness", __name__)
                        raise RestartTop() # restart the top loop with python's clumsy longjump
        except RestartTop:
            continue

    return did_count
