#!/usr/bin/env python
# coding: utf-8
# pylint: disable=method-hidden,unused-argument,attribute-defined-outside-init,protected-access

import tabulate

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
    def padding(self): # pragma: no cover
        self.pos = [0, 0]
        return super().padding

    @property
    def linebetweenrows(self): # pragma: no cover
        self.pos[1] += 1
        if self.pos[1] in (4, 7):
            return super().linebelowheader
        return super().linebetweenrows

    def datarow(self, padded_cells, colwidths, colaligns): # pragma: no cover
        # This is what "grid" would do if datarow was actually a callable:
        #   begin, sep, end = super().datarow
        #   return (begin + sep.join(padded_cells) + end).rstrip()

        begin, d_sep, end = super().datarow
        _, h_sep, _ = super().headerrow
        return (
            begin
            + h_sep.join(
                [
                    d_sep.join(padded_cells[0:3]),
                    d_sep.join(padded_cells[3:6]),
                    d_sep.join(padded_cells[6:9]),
                ]
            )
            + end
        ).rstrip()


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

tabulate._table_formats["sudoku"] = sudoku_tablefmt_obj
tabulate.multiline_formats["sudoku"] = "sudoku"

sudoku_table_format = "sudoku"  # the value actually used in sudoku.Puzzle
