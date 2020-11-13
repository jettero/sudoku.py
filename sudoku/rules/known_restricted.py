#!/usr/bin/env python
# coding: utf-8

from sudoku.puzzle import ELEMENT_VALUES as EV, describe_elements
from sudoku.rules import hookimpl


@hookimpl
def main(puzzle, opts):
    did_count = 0
    already = puzzle.context(main, already=set)['already']

    for v in EV:
        e_with_v = set(e for e in puzzle if e.value == v)
        rows_with_v = set(e.row for e in e_with_v)
        cols_with_v = set(e.col for e in e_with_v)
        for box in puzzle.boxes:
            if box.has(v):
                continue
            s = set(e for e in box if not e.value and e.row not in rows_with_v and e.col not in cols_with_v)
            if len(s) == 2:
                for e in s:
                    if e.loc not in already:
                        already.add(e.loc)
                        e.add_pencil_mark(v)
                        did_count += 1
                        puzzle.describe_inference(f'{v} can only be in {describe_elements(s)} in box {box.short} because of known positions of {v}')

    return did_count
