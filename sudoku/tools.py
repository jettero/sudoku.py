#!/usr/bin/env python
# coding: utf-8

import re
from collections import namedtuple
import tabulate

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
                self._g = list()
        return self._g

    @property
    def groupdict(self):
        if self._gd is None:
            if self._m:
                gd = self._m.groupdict()
                gdc = namedtuple('GDC', gd.keys())
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

# NOTE: you can't actually use a TableFormat with multiline data
# in any legitimate fashion — the if block looks like this:
#
#    if (
#        not isinstance(tablefmt, TableFormat)
#        and tablefmt in multiline_formats
#        and _is_multiline(plain_text)
#    ):
#        tablefmt = multiline_formats.get(tablefmt, tablefmt)
#        is_multiline = True
#    else:
#        is_multiline = False
#
# ... if we want to define our own tableformat and have it still
# act multiline, we straight up have to modify tabulate. *sigh*
#
# We'll just monkeypatch that shit in then. Whatever.

class SudokuTableFormat(tabulate.TableFormat):
    @property
    def padding(self):
        self.pos = [0,0]
        return super().padding

    @property
    def linebetweenrows(self):
        self.pos[1] += 1
        if self.pos[1] in (4,7):
            return super().linebelowheader
        return super().linebetweenrows

    def datarow(self, padded_cells, colwidths, colaligns):
        # This is what "grid" would do if datarow was actually a callable:
        #   begin, sep, end = super().datarow
        #   return (begin + sep.join(padded_cells) + end).rstrip()

        begin, d_sep, end = super().datarow
        _, h_sep, _ = super().headerrow
        return (begin + h_sep.join([
            d_sep.join(padded_cells[0:3]),
            d_sep.join(padded_cells[3:6]),
            d_sep.join(padded_cells[6:9]) ]) + end).rstrip()


# NOTE: this is the "grid" tablefmt in tabulate, except that we change the headerrow.sep to be
# '║' (aka '\u2551')...
sudoku_tablefmt_obj = SudokuTableFormat(
        lineabove=tabulate.Line(begin="+", hline="-", sep="+", end="+"),
        linebelowheader=tabulate.Line(begin="+", hline="=", sep="+", end="+"),
        linebetweenrows=tabulate.Line(begin="+", hline="-", sep="+", end="+"),
        linebelow=tabulate.Line(begin="+", hline="-", sep="+", end="+"),
        headerrow=tabulate.DataRow(begin="|", sep="║", end="|"),
        datarow=tabulate.DataRow(begin="|", sep="|", end="|"),
        padding=1,
        with_header_hide=None,
    )

tabulate._table_formats['sudoku'] = sudoku_tablefmt_obj
tabulate.multiline_formats['sudoku'] = 'sudoku'

sudoku_table_format = 'sudoku' # the value actually used in sudoku.Grid
