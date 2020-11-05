#!/usr/bin/env python
# coding: utf-8

from sudoku.grid import ELEMENT_VALUES as EV
from .spec import hookimpl

def has_value(box, value):
    for e in box:
        if e.value == value:
            return e

def has_no_value(box):
    return set(e for e in box if not e.value)

def elements_of_puzzle_with_single_rowcol_hidden_marks(puzzle, box, value):
    has_v_box  = set(e for e in box if value in e.hidden)
    has_v_rows = set(e.row for e in has_v_box)
    has_v_cols = set(e.col for e in has_v_box)

    if len(has_v_rows) == 1:
        has_v_rows, = has_v_rows
        yield from set(puzzle.rows[has_v_rows]) - set(box)

    if len(has_v_cols) == 1:
        has_v_cols, = has_v_cols
        yield from set(puzzle.cols[has_v_cols]) - set(box)

@hookimpl
def hidden(puzzle):
    did_count = 0
    something = set()

    for v in EV:
        has_v = set()
        for x in puzzle.rows + puzzle.cols:
            if has_value(x, v):
                has_v = has_v.union(x)

        for box in puzzle.boxes:
            if has_value(box, v):
                continue
            could_have_v = set(x for x in has_no_value(box) - has_v if v not in x.hidden)
            something = something.union(could_have_v)
            for e in could_have_v:
                e.add_hidden_mark(v)

        for box in puzzle.boxes:
            shouldnt_have_v = set(elements_of_puzzle_with_single_rowcol_hidden_marks(puzzle, box, v))
            something -= shouldnt_have_v
            for e in shouldnt_have_v:
                e.remove_hidden_mark(v)

    did_count = len(something)
    return did_count
