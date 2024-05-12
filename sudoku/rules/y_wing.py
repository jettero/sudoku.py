from itertools import combinations

"""
Find y-wings and enforce them.

TODO: I'd say this spots _some_ y-wings, but certainly _not_ all y-wings.
"""

from itertools import combinations
from sudoku.rules import hookimpl
from sudoku.tools import format_ints


def can_see(A, B):
    if A is B:
        return False  # I can't see myself, that's just crazy talk
    return A.row == B.row or A.col == B.col or A.box == B.box


def y_wing_finder(puzzle, C=(2, 2)):
    applicable = set(x for x in puzzle if not x.value and C[0] <= len(x.center) <= C[1])
    for combo in (set(x) for x in combinations(applicable, 3)):
        for head in combo:
            lhs, rhs = combo - {
                head,
            }
            if can_see(head, lhs) and can_see(head, rhs) and not can_see(rhs, lhs):
                if common := head.center & lhs.center & rhs.center:
                    uncommon = (rhs.center - common) | (lhs.center - common)
                    if len(common) == 1 and len(uncommon) == 2:
                        for tail in (x for x in applicable if can_see(lhs, x) and can_see(rhs, x)):
                            if (tail.center & uncommon) == uncommon:
                                yield (head, (lhs, rhs), *common, *sorted(uncommon), tail)


@hookimpl
def main(puzzle, opts=set()):
    did_something = 0
    start = -1
    while did_something > start:
        start = did_something
        for head, (lhs, rhs), ruled_out, v1, v2, tail in y_wing_finder(puzzle):
            puzzle.describe_inference(
                f"Y-Wing: As {tail} vacillates between {v1} and {v2}, it implies {head} cannot be {ruled_out} via {lhs} and {rhs}",
                __name__,
            )
            head.remove_center_marks(ruled_out)
            did_something += 1
    return did_something
