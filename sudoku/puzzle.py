#!/usr/bin/env python
# coding: utf-8

import logging
from tabulate import tabulate
from .tools import sudoku_table_format, sudoku_hist_table_format
from .otuple import Otuple
from .const import BOX_NUMBERS, ROW_NUMBERS, COLUMN_NUMBERS, ELEMENT_VALUES
from .box import Box, Row, Col
from .filt import element_has_val
from .history import History

log = logging.getLogger(__name__)

class Puzzle:
    broken = False
    pid = 0

    def __init__(self, pid=None):
        self.rows = rows = Otuple(Row(idx=r) for r in ROW_NUMBERS)
        self.cols = Otuple(Col(*(r[c] for r in rows), idx=c) for c in COLUMN_NUMBERS)

        if pid is None:
            self.pid = self.__class__.pid
            self.__class__.pid += 1
        else:
            self.pid = pid
        self.short = f'Puzzle({self.pid})'

        def box_elements(b):
            b -= 1
            c = (3 * b) % 9
            C = tuple(range(c, c + 3))
            r = (b // 3) * 3
            R = tuple(range(r, r + 3))
            for r in R:
                for c in C:
                    yield rows[r + 1][c + 1]

        self.boxes = Otuple(Box(*box_elements(b), idx=b) for b in BOX_NUMBERS)
        self._history = History()
        self._context = dict()

    def context(self, thing, **kw):
        """
        Give some puzzle local storage.

            def nombre():
                X = puzzle.context(main, X=set)["X"]

        This says, there should be some persistant storage called "X" that's
        quasi-local to the nombre() function.

        You could do sorta the same thing with something like this:

            if not hasattr(puzzle, 'C'):
                puzzle.C = dict()

            k = (id(main), "X")
            if k not in puzzle.C:
                puzzle.C[k] = set()
            X = puzzle.C[k]
        """
        try:
            hash(thing)
        except TypeError:
            thing = id(thing)
        if thing in self._context:
            return self._context[thing]
        if thing not in self._context:
            for k, v in kw.items():
                if v in (set, dict, tuple, list):
                    kw[k] = v()
            self._context[thing] = dict(**kw)
        return self._context[thing]

    def clone(self, transpose=False, copy_all=False, with_marks=False):
        ret = self.__class__(pid=self.pid)
        for r in ROW_NUMBERS:
            for c in COLUMN_NUMBERS:
                e = self[c,r] if transpose else self[r, c]
                if e.given:
                    ret[r, c].given = e.value
                elif copy_all and e.value:
                    ret[r,c].value = e.value
                if with_marks or copy_all:
                    ret[r,c].add_pencil_marks(*e.pencil)
                    ret[r,c].add_center_marks(*e.center)
        return ret

    def reset(self):
        for e in self:
            e.reset()
        self._history.clear()

    def describe_inference(self, desc, src):
        log.debug("[%s].di( %s by %s )", self.short, desc, src)
        self._history.append(desc, src)

    @property
    def history(self):
        return self._history.freeze()

    def __iter__(self):
        for row in self.rows:
            for e in row:
                yield e

    def __getitem__(self, idx):
        if isinstance(idx, (list, tuple)) and len(idx) == 2:
            return self.rows[idx[0]][idx[1]]
        try:
            idx = int(idx)
        except (ValueError, TypeError):
            pass
        if isinstance(idx, str):
            ret = set()
            for row in self.rows:
                ret = ret.union(row[idx])
            return ret
        return self.rows[idx]

    def __setitem__(self, idx, val):
        if isinstance(idx, (list, tuple)) and len(idx) == 2:
            self.rows[idx[0]][idx[1]] = val
            return
        raise IndexError(f"grids require tuple indexes to set elements (given: {idx})")

    def __repr__(self):
        return self.short

    def __str__(self):
        dat = [[x.as_cell for x in row] for row in self.rows]
        if self.history:
            return tabulate([[tabulate(dat, tablefmt=sudoku_table_format, stralign=None), '\n'.join(self.history)]], tablefmt=sudoku_hist_table_format, rowalign='bottom')
        return tabulate(dat, tablefmt=sudoku_table_format, stralign=None)

    def has(self, val, inc_val=True, inc_pencil=False, inc_center=False):
        return set(
            x
            for x in self
            if element_has_val(x, val, inc_val=inc_val, inc_pencil=inc_pencil, inc_center=inc_center)
        )

    @property
    def box_rows(self):
        yield (self.boxes[1], self.boxes[2], self.boxes[3])
        yield (self.boxes[4], self.boxes[5], self.boxes[6])
        yield (self.boxes[7], self.boxes[8], self.boxes[9])

    @property
    def box_cols(self):
        yield (self.boxes[1], self.boxes[4], self.boxes[7])
        yield (self.boxes[2], self.boxes[5], self.boxes[8])
        yield (self.boxes[3], self.boxes[6], self.boxes[9])

    @property
    def groupings(self):
        yield self.rows
        yield self.cols
        yield self.boxes

    def count_values(self):
        ret = dict()
        for grouping in self.groupings:
            for group in grouping:
                ret[group.short] = d = {d: 0 for d in ELEMENT_VALUES}
                for x in group:
                    if x.value:
                        d[x.value] += 1
        return ret

    def check(self):
        class WeirdList(list):
            def __bool__(self):
                return len(self) == 0
        res = WeirdList()
        cv = self.count_values()
        for gname, grouping in sorted(cv.items()):
            for v, c in sorted(grouping.items()):
                if c > 1:
                    res.append(f"{gname} contains {c} '{v}'s")
        if not res:
            self.broken = True
        return res
