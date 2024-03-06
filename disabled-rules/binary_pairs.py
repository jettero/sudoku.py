#!/usr/bin/env python
# coding: utf-8

from sudoku.rules import hookimpl
from sudoku.tools import describe_elements, pairs_iter


@hookimpl
def main(puzzle, opts=set()):
    did_count = 0
    already = puzzle.context(main, already_paired=set)["already_paired"]

    def all_boxes_have_marks(v1, v2, hvu):
        """ check to make sure if hvu is a row or a col
            that we've actually checked all the boxes in the row or col
            for v1 and v2; otherwise we could falsely assume the absence of
            markings in one of the positions is because the digit can't be
            there, when it's really only because we never considered whether it
            could for that box.
        """

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
            raise Exception("this doesn't seem possible")  # pragma: no cover
        bbox = puzzle.boxes[bno]
        bbh1 = memoized_fetch(v1, bbox, inc_val=True)
        bbh2 = memoized_fetch(v2, bbox, inc_val=True)
        if bbh1 and bbh2:
            return True

    memo = dict()

    def memoized_fetch(v, box, inc_pencil=True, inc_center=False, inc_val=False):
        k = (v, box, inc_pencil, inc_center, inc_val)
        try:
            return memo[k]
        except KeyError:
            memo[k] = hv = box.has(v, inc_pencil=inc_pencil, inc_center=inc_center, inc_val=inc_val)
        return hv

    for v1, v2 in pairs_iter():
        for box in puzzle.boxes + puzzle.rows + puzzle.cols:
            hv1 = memoized_fetch(v1, box)
            hv2 = memoized_fetch(v2, box)
            hvu = hv1.union(hv2)
            if len(hv1) == 2 and hv1 == hv2:
                if all_boxes_have_marks(v1, v2, hvu):
                    lvu = tuple(sorted(set(x.loc for x in hvu)))
                    k = (v1, v2, lvu)
                    if k not in already:
                        puzzle.describe_inference(
                            f"{v1}-{v2} pair in {box.short} in {describe_elements(hvu)}",
                            __name__,
                        )
                        already.add(k)
                        for e in hvu:
                            e.clear_pencil_marks()
                            e.add_center_mark(v1, v2)
                        memo.clear()

    return did_count
