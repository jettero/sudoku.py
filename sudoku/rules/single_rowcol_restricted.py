#!/usr/bin/env python
# coding: utf-8

from sudoku.rules import hookimpl
from sudoku.const import ELEMENT_VALUES as EV
from sudoku.tools import describe_elements

@hookimpl
def main(puzzle, opts):
    did_count = 0
    already_removed = puzzle.context(main, already_removed=set)['already_removed']

    for v in EV:
        for box in puzzle.boxes:
            x = box.single_attr_containing_val(v, attr='row', inc_val=False, inc_marks=True)
            if x:
                t = box.has(v, inc_marks=True)
                s = set(x for x in puzzle.rows[x].has(v, inc_marks=True) - t if x.loc not in already_removed)
                if s:
                    puzzle.describe_inference(f'{v} is restricted from {describe_elements(s)} by {describe_elements(t)}')
                    for e in s:
                        already_removed.add(e.loc)
                        did_count += 1
                        e.remove_pencil_mark(v)
                        e.remove_center_mark(v)

    return did_count
