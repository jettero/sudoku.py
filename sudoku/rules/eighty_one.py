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

        can_be = SEV - set(x.value for b in box_col_row(puzzle, e) for x in b if x.value)

        if not can_be:
            puzzle.broken = True
            puzzle.describe_inference(f"this puzzle is broken, we need {e} is restricted to ∅", __name__)
            e.clear_center_marks()

        elif len(can_be) == 1:
            (e.value,) = can_be
            puzzle.describe_inference(f"{e} must be {can_be} by uniqueness", __name__)
            did_count = 1

        elif e.center != can_be:
            e.set_center_marks(*can_be)
            # puzzle.describe_inference(f"{e} must be {can_be} by uniqueness", __name__)
            did_count = 1

    return did_count
