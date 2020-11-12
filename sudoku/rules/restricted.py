#!/usr/bin/env python
# coding: utf-8

from sudoku.grid import ELEMENT_VALUES as EV, describe_elements
from .spec import hookimpl

def value_restricted(puzzle):
    changed = set()

    for v in EV:
        rows  = set(x for x in EV if puzzle.rows[x].has(v))
        cols  = set(x for x in EV if puzzle.cols[x].has(v))
        boxes = set(x for x in EV if puzzle.boxes[x].has(v))

        for e in puzzle:
            if e.value:
                continue
            shouldnt_have = e.row in rows or e.col in cols or e.box in boxes
            if v in e.hidden and shouldnt_have:
                e.remove_hidden_mark(v)
                changed.add(e)
            elif v not in e.hidden and not shouldnt_have:
                e.add_hidden_mark(v)
                changed.add(e)

    return changed

def single_row_of_a_box(puzzle, vr_changed, mode='row'):
    changed = set()

    for v in EV:
        for box in puzzle.boxes:
            rno = set(getattr(x,mode) for x in box if v in x.hidden)
            if len(rno) == 1:
                rno, = rno
                shouldnt_have_v = set(getattr(puzzle, f'{mode}s')[rno]) - set(box)
                actually_has_v_though = set(x for x in shouldnt_have_v if v in x.hidden)
                if actually_has_v_though:
                    puzzle.describe_inference(f"{v} is restricted to row {rno} in {box.short} => {v} can't be in {describe_elements(shouldnt_have_v)}")
                    for e in actually_has_v_though:
                        e.remove_hidden_mark(v)
                        changed.add(e)

    return vr_changed.symmetric_difference(changed)


@hookimpl
def hidden(puzzle):
    changed = value_restricted(puzzle)
    changed = single_row_of_a_box(puzzle, changed)
    changed = single_row_of_a_box(puzzle, changed, mode='col')
    return len(changed)
