#!/usr/bin/env python
# coding: utf-8

from sudoku.rules import hookimpl
from sudoku.const import ELEMENT_VALUES as EV
from sudoku.tools import describe_elements

def v_can_be_in_e(v, e, rows_with_v, cols_with_v):
    if e.value:
        return False
    if e.row in rows_with_v:
        return False
    if e.col in cols_with_v:
        return False
    if e.center and v not in e.center:
        return False
    return True

class Abstraction:
    def __init__(self, grouping, r1, r2, only_singletons=False):
        self.grouping = grouping
        self.r1 = r1
        self.r2 = r2
        self.only_singletons = only_singletons

    def elements_in_r1(self, elements):
        return set(getattr(e, self.r1) for e in elements)

    def elements_in_r2(self, elements):
        return set(getattr(e, self.r2) for e in elements)

    def groupings(self, puzzle):
        return getattr(puzzle, self.grouping)

ABSTRACTIONS = (
    Abstraction('boxes', 'row', 'col'),

    # this is really confusing and certainly not a mark a human would make:
    # Abstraction('rows',  'box', 'col'),
    # Abstraction('cols',  'row', 'box'),

    # a human swould notice this though:
    Abstraction('rows',  'box', 'col', only_singletons=True),
    Abstraction('cols',  'row', 'box', only_singletons=True),
)

@hookimpl
def main(puzzle, opts):
    did_count = 0
    context = puzzle.context(main, already_singleton=set, already_pencil=set)
    already_s = context['already_singleton']
    already_p = context['already_pencil']

    for abstraction in ABSTRACTIONS:
        for v in EV:
            e_with_v = puzzle.has(v)
            rows_with_v = abstraction.elements_in_r1(e_with_v)
            cols_with_v = abstraction.elements_in_r2(e_with_v)
            for box in abstraction.groupings(puzzle):
                if box.has(v):
                    continue
                s = set(e for e in box if v_can_be_in_e(v, e, rows_with_v, cols_with_v))
                if len(s) == 1:
                    for e in s:
                        k = (v, e.loc)
                        if k not in already_s:
                            puzzle.describe_inference(f'singleton {v} must be in {e.short} in {box.short}', __name__)
                            e.value = v
                            for box in (puzzle.boxes[e.box], puzzle.rows[e.row], puzzle.cols[e.col]):
                                for e in box:
                                    e.remove_marks(v)
                            did_count += 1
                            already_s.add(k)
                elif len(s) == 2 and not abstraction.only_singletons:
                    for e in s:
                        k = (v, e.loc)
                        if k not in already_p:
                            puzzle.describe_inference(f'{v} can only be in {describe_elements(s)} in {box.short}', __name__)
                            e.add_pencil_mark(v)
                            did_count += 1
                            already_p.add(k)

    return did_count
