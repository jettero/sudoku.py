#!/usr/bin/env python
# coding: utf-8

import re
import os
import inspect
from collections import namedtuple
from itertools import combinations
from .monkeypatch_tabulate import sudoku_table_format, sudoku_hist_table_format  # pylint: disable=unused-import
from .const import R19, EV

class LongJump(Exception):
    pass

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


def pairs_iter(n=2):
    yield from combinations(EV, n)

def box_col_row(p, e):
    """generate the box, col, and row for an element"""
    yield p.boxes[e.box]
    yield p.rows[e.row]
    yield p.cols[e.col]


def elements_in_box_col_row(p, e):
    """generate all elements from the box, col, and row of a given element
    (but excluded the given element and cul duplicates)
    """
    ret = set()
    for b in box_col_row(p, e):
        for _e in b:
            if _e is e:
                continue
            ret.add(_e)
    yield from ret


def split_tuple(input_tuple, chunk_size=3):
    return tuple(input_tuple[i : i + chunk_size] for i in range(0, len(input_tuple), chunk_size))


def format_digits_in_row_cols(digits):
    """
    meant for formatting center marks in the center of the cell when displaying the puzzle for humans

    digits must be iterable, and must be the digits...

    "".join(str(x) for x in digits) # <--- this has to work

    returns a tuple of tuples
    """

    d = tuple(str(x) for x in sorted(digits))
    l = len(digits)

    if l == 1:
        #   1
        return (tuple(), (" ", " ", *d))

    if l == 2:
        #  12
        return (tuple(), (" ", *d))

    if l < 5:
        # 123
        # 1234
        return (
            tuple(),
            d,
        )  # empty tuple, so single line is more centered

    if l in (5, 6, 9):
        # 123
        # 45
        #
        # 123
        # 456
        #
        # 123
        # 456
        # 789
        return split_tuple(d, chunk_size=3)

    # 1234
    # 567
    #
    # 1234
    # 5678
    return split_tuple(d, chunk_size=4)

def format_ints(*i):
    return ''.join(str(x) for x in sorted(i))

def oxford_format_ints(*i):
    i = [ str(x) for x in i ]
    i = list(sorted(set(i)))
    if len(i) <= 2:
       return ' and '.join(i)
    i[-1] = f'and {i[-1]}'
    return ', '.join(i)

def format_exception_in_english(e, back=1):
     tb = e.__traceback__
     if tb is None:    # this isn't likely to come up, so I don't want to bother testing it
         return str(e) # pragma: no cover
     while tb.tb_next is not None and back > 0:
         tb = tb.tb_next
         back -= 1

     frame = tb.tb_frame
     lineno = tb.tb_lineno
     filename = frame.f_code.co_filename
     function_name = frame.f_code.co_name

     if module := inspect.getmodule(frame):
         module_name = module.__name__
     else:
         # I doubt we'll reach this point very often, so I don't want to bother testing it
         module_name = os.path.basename(filename)[:-3] # pragma: no cover

     return f"{e} in {module_name} line {lineno}"

def can_see(A, B):
    if A is B:
        return False  # I can't see myself, that's just crazy talk
    return A.row == B.row or A.col == B.col or A.box == B.box

def pluralize(x):
    if x.endswith('x'):
        return f'{x}es'
    return f'{x}s'

