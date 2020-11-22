#!/usr/bin/env python
# coding: utf-8


from sudoku.rules import hookimpl
from sudoku.const import ELEMENT_VALUES as EV

SEV = set(EV)


@hookimpl
def main(puzzle, opts=set()):
    did_count = 0

    for box in puzzle.rows + puzzle.cols + puzzle.boxes:
        no_v = set(e for e in box if not e.value)
        if len(no_v) == 1:
            kv = set(e.value for e in box if e.value)
            v, *ov = SEV - kv
            (e,) = no_v
            if ov:  # pragma: no cover
                puzzle.describe_inference(
                    f"this puzzle is broken, we need {e} to be {v} + {ov}", __name__
                )
                return
            puzzle.describe_inference(f"{e} must be {v} by uniqueness", __name__)
            e.value = v

    return did_count
