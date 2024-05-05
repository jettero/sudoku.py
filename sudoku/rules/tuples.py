#!/usr/bin/env python
# coding: utf-8
"""
XXX: Description here
"""

import os
from itertools import combinations
from sudoku.rules import hookimpl
from sudoku.const import SEV
from sudoku.tools import describe_elements

TUPLE_SIZEZ_AND_NAMES = (  # (sz, name), ...
    (1, "can only be"),
    (2, "pair"),
    #   (3, "tripple"),
    #   (4, "quad"),
)


@hookimpl
def main(puzzle, opts=set()):
    if os.environ.get("SKIP_TUPLES"):
        return 0

    did_count = 0

    # If 5 and 8 appear in only in c2 and c3 of column 1, then they can't also
    # contain other numbers -- remove anything but 5 and 8 from those two.
    # This works for any N numbers in any N elements in any row/col/box.
    for N, nname in TUPLE_SIZEZ_AND_NAMES:
        for container in puzzle.containers:
            for vp in combinations(SEV - set(e.value for e in container if e.value), N):
                vp = {*vp}
                e = {x for x in container if x.center & vp}

                if len(e) == N:
                    dc = did_count
                    for item in e:
                        if N == 1 and not item.value:
                            (item.value,) = vp
                            did_count += 1
                        elif item.center != vp:
                            item.set_center_marks(*vp)
                            did_count += 1
                    if did_count > dc:
                        puzzle.describe_inference(
                            f"{''.join(str(x) for x in sorted(vp))} {nname} in {describe_elements(e)} in {container.short}",
                            __name__,
                        )

    return did_count
