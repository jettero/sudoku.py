#!/usr/bin/env python
# coding: utf-8

from sudoku.rules import hookimpl
from sudoku.tools import describe_elements, pairs_iter
from sudoku.const import EV


@hookimpl
def main(puzzle, opts=set()):
    did_count = 0
    already = puzzle.context(main, already_paired=set)["already_paired"]

    def seems_legit(v1, v2, hvu):
        hvu_boxes = set(e.box for e in hvu)
        if len(hvu_boxes) == 1:
            return True
        r1, r2 = (e.row for e in hvu)
        c1, c2 = (e.col for e in hvu)
        if c1 == c2:
            (bno,) = set(x.box for x in puzzle.cols[c1]) - hvu_boxes
        elif r1 == r2:
            (bno,) = set(x.box for x in puzzle.rows[r1]) - hvu_boxes
        else:
            raise Exception("this doesn't seem possible")
        bbox = puzzle.boxes[bno]
        bbh1 = bbox.has(v1, inc_marks=True, inc_val=True)
        bbh2 = bbox.has(v2, inc_marks=True, inc_val=True)
        if bbh1 and bbh2:
            return True

    memo = dict()
    def memoized_fetch(v,box):
        k = (v,box)
        try:
            return memo[k]
        except KeyError:
            memo[k] = hv = box.has(v, inc_marks=True, inc_val=False)
        return hv

    for v1, v2 in pairs_iter():
        for box in puzzle.boxes + puzzle.rows + puzzle.cols:
            hv1 = memoized_fetch(v1,box)
            hv2 = memoized_fetch(v2,box)
            hvu = hv1.union(hv2)
            if len(hv1) == 2 and len(hv2) == 2 and len(hvu) == 2:
                if seems_legit(v1, v2, hvu):
                    lvu = tuple(sorted(set(x.loc for x in hvu)))
                    k = (v1, v2, lvu)
                    if k not in already:
                        puzzle.describe_inference(
                            f"{v1}-{v2} pair in {box.short} in {describe_elements(hvu)}",
                            __name__,
                        )
                        already.add(k)
                        for e in hvu:
                            e.remove_pencil_mark(*EV)
                            e.add_center_mark(v1, v2)

    return did_count
