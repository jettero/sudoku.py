#!/usr/bin/env python
# coding: utf-8

from sudoku.grid import ELEMENT_VALUES as EV, describe_elements
from .spec import hookimpl

def has_value(box, value):
    for e in box:
        if e.value == value:
            return e

def has_no_value(box):
    return set(e for e in box if not e.value)

def restrictions_cause_further_restrictions(puzzle, box, value):
    """ if value is restricted to a single row in box 1, then box 2 and box 3 can't have value in that row """

    has_v_box  = set(e for e in box if value in e.hidden)
    has_v_rows = set(e.row for e in has_v_box)
    has_v_cols = set(e.col for e in has_v_box)

    if len(has_v_rows) == 1:
        r, = has_v_rows
        reason = f"{value} is restricted to row {r} in {box.short}"
        yield (reason, set(puzzle.rows[r]) - set(box))

    if len(has_v_cols) == 1:
        c, = has_v_cols
        reason = f"{value} is restricted to col {c} in {box.short}"
        yield (reason, set(puzzle.cols[c]) - set(box))

@hookimpl
def hidden(puzzle):
    did_count = 0
    changed = set()

    for v in EV:
        has_v = set()
        for x in puzzle.rows + puzzle.cols:
            if has_value(x, v):
                has_v = has_v.union(x)

        for box in puzzle.boxes:
            if has_value(box, v):
                continue
            could_have_v = set(x for x in has_no_value(box) - has_v if v not in x.hidden)
            changed = changed.union(could_have_v)
            for e in could_have_v:
                e.add_hidden_mark(v)

        for box in puzzle.boxes:
            for reason, generator in restrictions_cause_further_restrictions(puzzle, box, v):
                shouldnt_have_v = set(x for x in generator if v in x.hidden)
                if shouldnt_have_v:
                    puzzle.describe_inference(f"{reason} => {v} can't be in {describe_elements(shouldnt_have_v)}")
                    changed = changed.symmetric_difference(shouldnt_have_v)
                    for e in shouldnt_have_v:
                        e.remove_hidden_mark(v)

    did_count = len(changed)
    return did_count
