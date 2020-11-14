#!/usr/bin/env python
# coding: utf-8

from sudoku.rules import hookimpl
from sudoku.const import ELEMENT_VALUES as EV
from sudoku.tools import describe_elements


@hookimpl
def main(puzzle, opts):
    did_count = 0
    context = puzzle.context(main, already_singleton=set, already_pencil=set)
    already_s = context['already_singleton']
    already_p = context['already_pencil']

    for v in EV:
        e_with_v = puzzle.has(v)
        rows_with_v = set(e.row for e in e_with_v)
        cols_with_v = set(e.col for e in e_with_v)
        for box in puzzle.boxes:
            if box.has(v):
                continue
            s = set(e for e in box if not e.value and e.row not in rows_with_v and e.col not in cols_with_v)
            if len(s) == 1:
                for e in s:
                    if e.loc not in already_s:
                        puzzle.describe_inference(f'singleton {v} must be in {e.short} in box {box.short}')
                        e.value = v
                        did_count += 1
                        already_s.add(e.loc)
            elif len(s) == 2:
                for e in s:
                    if e.loc not in already_p:
                        already_p.add(e.loc)
                        e.add_pencil_mark(v)
                        did_count += 1
                        puzzle.describe_inference(f'{v} can only be in {describe_elements(s)} in box {box.short}')

    return did_count
