#!/usr/bin/env python
# coding: utf-8

from sudoku.rules import hookimpl
from sudoku.tools import describe_elements, pairs_iter
from sudoku.const import EV

@hookimpl
def main(puzzle, opts):
    did_count = 0
    already = puzzle.context(main, already_paired=set)['already_paired']

    for v1,v2 in pairs_iter():
        for box in puzzle.boxes + puzzle.rows + puzzle.cols:
            hv1 = box.has(v1, inc_marks=True, inc_val=False)
            hv2 = box.has(v2, inc_marks=True, inc_val=False)
            hvu = hv1.union(hv2)
            if len(hv1) == 2 and len(hv2) == 2 and len(hvu) == 2:
                lvu = tuple(sorted(set( x.loc for x in hvu )))
                k = (v1,v2,lvu)
                if k not in already:
                    puzzle.describe_inference(f'{v1}-{v2} pair in {box.short} in {describe_elements(hvu)}', __name__)
                    already.add(k)
                    for e in hvu:
                        e.remove_pencil_mark(*EV)
                        e.add_center_mark(v1,v2)

    return did_count
