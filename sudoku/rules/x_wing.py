#!/usr/bin/env python
# coding: utf-8

"""
Find x-wings (and related) and remove marks relating to their influences.

… and then generalize to find other similar things.

I.e., start with this notion:

    n = 2
    for i in 1 .. 9:
        E = { e ∈ P | i in e.center }  # e is an element in the puzzle
                                       # given that i is a member of
                                       # the center marks of e)

        A = { e.row | e ∈ E }  # the set of row numbers available in the
                               # elements in E

        ∀ a ⊆ A, |a| = n:  # a is each 2-pick combination in A
            Ea = { e ∈ E | e.row ∈ a }  # elements with rows in a
            b = { e.col | e ∈ Ea }  # columns

            if |b| = n:  # if there's 2 of them
                Eb = { e ∈ E | e.col ∈ b }  # Eb is the elements with
                                            # columns in b

                # The X-wing we just found implies nothing else in these
                # columns can have the mark 'i' — side note: set difference is
                # not written with a dash, like an algebraic difference, but
                # instead chooses a backslash, which has special meaning in
                # python comments that function as docs.

                Eδ = Ea - Eb  # meaning Eb \\ Ea = { e ∈ Eb | e ∉ Ea }
                ∀ e ∈ Eδ:  # so for each
                    e.remove_center_marks(i)  # remove the mark 'i'

And then generalize so that A is { e.col | e ∈ E } (rather than by rows) and b
becomes { e.row | e ∈ Ea }. I.e., we call the first attribute aa='row' and the
second attribute ab='col' and then swap so aa='col' and ab='row'.

Then we can generalize again and say ∀ n ∈ {2,3,4} — which now finds all the
"Jellyfish" for sizes 3 and 4.

We can then generalize one more time: ∀ aa,ab ∈ { 'row', 'col', 'box' }, aa≠ab.
In other words, all the row-col, col-row, and box-col, row-box permutations.
This finds not just X-wings and Jellyfish, but also something else I'm calling
G-wings (for generalized x-wings); though, there may already be a better name
of which I'm not currently aware.
"""

from itertools import combinations, permutations
from sudoku.rules import hookimpl
from sudoku.const import SEV
from sudoku.tools import oxford_format_ints, describe_elements, LongJump, pluralize

SIZES = (2, 3, 4)
ATTRS = ("row", "col", "box")

def nameify(n, *a):
    if n == 2 and "box" not in a:
        return "X-wing"
    if "box" not in a:
        return "Jellyfish"
    return f"G-wing({n}, {'-'.join(sorted(a))})"

@hookimpl
def main(puzzle, opts=set()):
    did_something = 0

    nv = set(x for x in puzzle if not x.value)
    while True:
        try:
            for n in SIZES:
                for i in SEV:
                    E = set(x for x in nv if i in x.center)
                    for aa, ab in permutations(ATTRS, 2):
                        A = set(getattr(x, aa) for x in E)
                        for a in combinations(A, n):
                            Ea = set(x for x in E if getattr(x, aa) in a)
                            b = set(getattr(x, ab) for x in Ea)

                            if len(b) == n:
                                Eb = set(x for x in E if getattr(x, ab) in b)
                                if Eδ := Eb - Ea:
                                    puzzle.describe_inference(
                                        f"{nameify(n,aa,ab)}: {i} can only be in {pluralize(ab)} {oxford_format_ints(*b)} in {pluralize(aa)} {oxford_format_ints(*a)}"
                                        f" => remove {i} from {describe_elements(Eδ)}",
                                        __name__,
                                    )
                                    for e in Eδ:
                                        e.remove_center_marks(i)
                                    raise LongJump()
        except LongJump:
            did_something += 1
            continue
        break

    return did_something
