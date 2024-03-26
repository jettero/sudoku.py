#!/usr/bin/env python
# coding: utf-8

import re
from collections import namedtuple
from .monkeypatch_tabulate import sudoku_table_format  # pylint: disable=unused-import
from .const import R19, EV


def rc2b(r, c):
    # I wonder if we could do this more elegantly with math
    # probably not worth figuring out… hrm.
    if r in (1, 2, 3):
        if c in (1, 2, 3):
            return 1
        if c in (4, 5, 6):
            return 2
        if c in (7, 8, 9):
            return 3
    if r in (4, 5, 6):
        if c in (1, 2, 3):
            return 4
        if c in (4, 5, 6):
            return 5
        if c in (7, 8, 9):
            return 6
    if r in (7, 8, 9):
        if c in (1, 2, 3):
            return 7
        if c in (4, 5, 6):
            return 8
        if c in (7, 8, 9):
            return 9


def describe_elements(elements):
    return ", ".join(sorted(e.short for e in elements))


class PYTR:
    def __init__(self, pattern, flags=0):
        self._regex = re.compile(pattern, flags)
        self._m = self._g = self._gd = None

    def match(self, target):
        self._m = self._regex.match(target)
        self._g = self._gd = None
        return bool(self._m)

    def search(self, target):
        self._m = self._regex.search(target)
        self._g = self._gd = None
        return bool(self._m)

    @property
    def groups(self):
        if self._g is None:
            if self._m:
                self._g = self._m.groups()
            else:
                self._g = tuple()
        return self._g

    @property
    def groupdict(self):
        if self._gd is None:
            if self._m:
                gd = self._m.groupdict()
                gdc = namedtuple("GDC", gd.keys())
                gdc.__getitem__ = gd.__getitem__
                gdc.get = gd.get
                self._gd = gdc(**gd)
            else:
                self._gd = dict()
        return self._gd

    def __getitem__(self, key):
        if isinstance(key, int):
            return self.groups[key]
        if isinstance(key, str):
            return self.groupdict[key]
        raise TypeError(f'not sure how to lookup key="{key}"')

    def __eq__(self, actual):
        return bool(self._regex.search(actual))

    def __repr__(self):
        return self._regex.pattern


def one_and_the_others_iter(s):
    """
    In [35]: list(one_and_the_others_iter([1,2,3]))
    Out[35]: [(1, [2, 3]), (2, [1, 3]), (3, [1, 2])]
    """
    for i, x in enumerate(s):
        yield (x, s[:i] + s[i + 1 :])


def pos_iter():
    for r in R19:
        for c in R19:
            yield (r, c)


def brc_iter():
    for b in range(9):
        c = (3 * b) % 9
        C = tuple(range(c, c + 3))
        r = (b // 3) * 3
        R = tuple(range(r, r + 3))
        for r in R:
            for c in C:
                yield (b + 1, r + 1, c + 1)


def pairs_iter():
    already = set()
    for v1 in EV:
        for v2 in EV:
            if v1 == v2:
                continue
            op = tuple(sorted((v1, v2)))
            if op not in already:
                already.add(op)
                yield op


def box_col_row(p, e):
    yield p.boxes[e.box]
    yield p.rows[e.row]
    yield p.cols[e.col]
