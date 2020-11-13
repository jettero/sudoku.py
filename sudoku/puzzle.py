#!/usr/bin/env python
# coding: utf-8

from tabulate import tabulate
from .tools import sudoku_table_format
from .otuple import Otuple
from .const import BOX_NUMBERS, ROW_NUMBERS, COLUMN_NUMBERS
from .box import Box, Row, Col

def box_elements(b):
    b -= 1
    c = (3 * b) % 9
    C = tuple(range(c, c + 3))
    r = (b // 3) * 3
    R = tuple(range(r, r + 3))
    for r in R:
        for c in C:
            yield self.rows[r + 1][c + 1]

class Puzzle:
    def __init__(self):
        self.rows = Otuple(Row(idx=r) for r in ROW_NUMBERS)
        self.cols = Otuple(
            Col(*(r[c] for r in self.rows), idx=c) for c in COLUMN_NUMBERS
        )

        self.boxes = Otuple(Box(*box_elements(b), idx=b) for b in BOX_NUMBERS)
        self._history = list()
        self._context = dict()

    def context(self, thing, **kw):
        try:
            if thing in self._context:
                return self._context[thing]
        except TypeError:
            thing = id(thing)
        if thing not in self._context:
            for k, v in kw.items():
                if v in (set, dict, tuple, list):
                    kw[k] = v()
            self._context[thing] = dict(**kw)
        return self._context[thing]

    def clone(self):
        ret = self.__class__()
        for r in ROW_NUMBERS:
            for c in COLUMN_NUMBERS:
                e = self[r, c]
                if e.given:
                    ret[r, c].given = e.value
        return ret

    def reset(self):
        for e in self:
            e.reset()
        self._history = list()

    def describe_inference(self, desc):
        desc = desc.strip() + "\n"
        if desc not in self._history:
            self._history.append(desc)

    @property
    def history(self):
        return "".join(self._history)

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
        dat = [[x.as_cell for x in row] for row in self.rows]
        return tabulate(dat, tablefmt=sudoku_table_format, stralign=None)

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
