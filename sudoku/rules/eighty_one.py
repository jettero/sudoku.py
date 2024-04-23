#!/usr/bin/env python
# coding: utf-8
"""
Go through all cells, if there's a .value, then remove that center mark from
each cell in the col, row and box.  If a cells in the BCR already have a value,
then we skip -- or set the broken condition if it's the same value as the given
element.
"""

from sudoku.rules import hookimpl
from sudoku.const import ELEMENT_VALUES as EV
from sudoku.tools import elements_in_box_col_row

SEV = set(EV)

class RestartTop(Exception):
    pass

@hookimpl
def main(puzzle, opts=set()):
    did_count = 0

    while not puzzle.broken:
        try:
            for E in puzzle:
                if E.value:
                    for e in elements_in_box_col_row(puzzle, E):
                        if e.value:
                            continue
                        if before := e.center:
                            if E.value in before:
                                e.remove_center_marks(E.value)
                                did_count += 1
                                after = e.center
                                if len(after) == 1:
                                    v, = after
                                    e.value = v
                                    puzzle.describe_inference(f"{e} must be {v} by uniqueness", __name__)
                                    raise RestartTop() # restart the top loop with python's clumsy longjump
                                elif len(after) < 1:
                                    puzzle.broken = True
                                    puzzle.describe_inference(f"this puzzle is broken, we need {e} is restricted to ∅", __name__)
                                    return did_count # we're done here, the puzzle is nonsense now
                        else:
                            e.set_center_marks(*( v for v in EV if v != E.value ))
                            did_count += 1
            return did_count
        except RestartTop:
            continue
