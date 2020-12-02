#!/usr/bin/env python
# coding: utf-8

from sudoku.rules import hookimpl
from sudoku.tools import describe_elements, pairs_iter

@hookimpl
def main(puzzle, opts=set()):
    did_count = 0
    already = puzzle.context(main, already_paired=set)["already_paired"]

    # we pretend we're just working on finding hidden pairs in rows
    # but then we flip rows/cols and row/col on the second mainloop

    def cols_without_v(v, cmode='col'):
        ret = set(range(1,10))
        for col in getattr(puzzle, f'{cmode}s'):
            if col.has(v):
                ret.remove(col.idx)
        return ret

    def cols_that_cant_be_v(row,v, cmode='col'):
        ret = set()
        for e in row:
            if e.value:
                ret.add(getattr(e, cmode))
            elif e.center and v not in e.center:
                ret.add(getattr(e, cmode))
        return ret

    for rmode, cmode in ( ('row', 'col'), ('col', 'row') ):
        for v1, v2 in pairs_iter():
            for row in getattr(puzzle, f'{rmode}s'):
                if row.has(v1) or row.has(v2):
                    continue

                c1 = cols_without_v(v1, cmode) - cols_that_cant_be_v(row,v1,cmode)
                c2 = cols_without_v(v2, cmode) - cols_that_cant_be_v(row,v2,cmode)

                boxes = tuple(puzzle.boxes[b] for b in set(x.box for x in row))
                for box in boxes:
                    if box.has(v1):
                        c1 -= set(getattr(x, cmode) for x in box)
                    if box.has(v2):
                        c2 -= set(getattr(x, cmode) for x in box)

                if len(c1) == 2 and c1 == c2:
                    i1,i2 = c1
                    hp = row[i1], row[i2]
                    k = tuple(x.loc for x in hp)
                    if k not in already:
                        for e in hp:
                            e.add_center_marks(v1,v2)
                        puzzle.describe_inference(
                            f"{v1}-{v2} hidden pair in {row.short} in {describe_elements(hp)}",
                            __name__,
                        )
                        did_count += 1
                        already.add(k)

    return did_count
