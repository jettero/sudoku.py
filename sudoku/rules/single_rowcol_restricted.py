#!/usr/bin/env python
# coding: utf-8

from sudoku.rules import hookimpl
from sudoku.const import ELEMENT_VALUES as EV
from sudoku.tools import describe_elements, one_and_the_others_iter


@hookimpl
def main(puzzle, opts=set()):
    did_count = 0
    context = puzzle.context(main, blessed=set, blocked=set)
    blessed = context["blessed"]
    blocked = context["blocked"]

    for v in EV:
        for attr in ("row", "col"):
            for boxset in getattr(puzzle, f"box_{attr}s"):
                for box, (o1, o2) in one_and_the_others_iter(boxset):
                    if box.has(v):
                        continue
                    o1 = o1.single_attr_containing_val(
                        v, attr=attr, inc_marks=True, inc_val=True
                    )
                    o2 = o2.single_attr_containing_val(
                        v, attr=attr, inc_marks=True, inc_val=True
                    )

                    if o1 and o2:
                        # if v is restricted to one row in both other boxes we
                        # can compute a single blessed row where v has to be in
                        # the remaining box
                        blessed_no, *broken = set(getattr(x, attr) for x in box) - {
                            o1,
                            o2,
                        }
                        if broken: # pragma: no cover
                            broken = f'{blessed_no}, {", ".join(broken)}'
                            puzzle.describe_inference(
                                f"this puzzle is broken, we have multiple blessed rows for {v} in {box.short}: {broken}",
                                __name__,
                            )
                            return
                        has_no_v = set(e for e in box if not e.value)
                        can_be_v = set(
                            e for e in has_no_v if getattr(e, attr) == blessed_no
                        )
                        cannot_be_v = has_no_v - can_be_v
                        for e in can_be_v:
                            if not e.center:
                                e.add_pencil_mark(v)
                                k = (blessed_no, box.short, e.loc, "can")
                                if k not in blessed:
                                    blessed.add(k)
                                    did_count += 1
                        for e in cannot_be_v:
                            e.remove_marks(v)
                            k = (blessed_no, box.short, e.loc, "cant")
                            if k not in blessed:
                                blessed.add(k)
                                did_count += 1

                    # we can also remove any pencil marks in rows restricted
                    # out by either o1 or o2 even if nothing else happened
                    # above
                    for no in (o1, o2):
                        cant_be = set(
                            x for x in box if getattr(x, attr) == no and v in x.marks
                        )
                        if cant_be:
                            puzzle.describe_inference(
                                f"{v} can't be in {attr} {no} in {box.short}", __name__
                            )
                            for e in cant_be:
                                e.remove_marks(v)
                                k = (attr, no, box.short, e.loc)
                                if k not in blocked:
                                    blocked.add(k)
                                    did_count += 1

    return did_count
