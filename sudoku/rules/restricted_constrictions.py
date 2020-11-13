#!/usr/bin/env python
# coding: utf-8

from sudoku.puzzle import ELEMENT_VALUES as EV
from sudoku.rules import hookimpl
from sudoku.tools import one_and_the_others_iter

def chain(x):
    for y in x:
        yield from y

@hookimpl
def main(puzzle, opts):
    did_count = 0
    context = puzzle.context(main, already_p=set, already_up=set)
    already_p = context['already_p']
    already_u = context['already_up']

    for v in EV:
        for three_boxes in puzzle.box_rows:
            for box, others in one_and_the_others_iter(three_boxes):
                rno = set(e.row for e in chain(others) if e.value == v or v in e.marks)
                if len(rno) == 2:
                    only_row, = set(e.row for e in box) - rno
                    possible = set(e for e in box if e.row == only_row)
                    unpossible = set(e for e in box if e.row != only_row)

                    for e in possible:
                        e.add_pencil_mark(ddp
                        if e not in already_p:
                            did_count += 1

    return did_count
