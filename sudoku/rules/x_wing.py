#!/usr/bin/env python
# coding: utf-8

"""
Find x-wings (and related) and remove marks relating to their influences.

... and then generalize to find other similar things.
"""

from itertools import combinations, permutations
from sudoku.rules import hookimpl
from sudoku.const import SEV
from sudoku.tools import oxford_format_ints, describe_elements, LongJump, pluralize

def nameify(n,*a):
    if n == 2 and 'box' not in a:
        return "X-Wing"
    return f"G-Wing({n}, {'-'.join(sorted(a))})"

@hookimpl
def main(puzzle, opts=set()):
    did_something = 0

    nv = set(x for x in puzzle if not x.value)
    while True:
        try:
            for n in (2,3,4):
                for i in SEV:
                    E = set(x for x in nv if i in x.center)
                    for aa,ab in permutations(('row','col','box'), 2):
                        A = set(getattr(x, aa) for x in E)
                        for a in combinations(A, n):
                            Ea = set(x for x in E if getattr(x, aa) in a)
                            b = set(getattr(x,ab) for x in Ea)

                            if len(b) == n:
                                Eb = set(x for x in E if getattr(x, ab) in b)
                                if no := Eb - Ea:
                                    puzzle.describe_inference(f"{nameify(n,aa,ab)}: {i} can only be in {pluralize(ab)} {oxford_format_ints(*b)} in {pluralize(aa)} {oxford_format_ints(*a)}"
                                                              f" => remove {i} from {describe_elements(no)}", __name__)
                                    for e in no:
                                        e.remove_center_marks(i)
                                    raise LongJump()
        except LongJump:
            did_something += 1
            continue
        break

    return did_something
