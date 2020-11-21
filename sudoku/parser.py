#!/usr/bin/env python
# coding: utf-8
# pylint: disable=no-self-use

from lark import Lark, Transformer
from .puzzle import Puzzle


def get_puzzles(file="Puzzles.txt"):
    """ get_puzzles(file='Puzzles.txt') does essentially this:

            with open(file, 'r') as fh:
                dat = fh.read()
            yield from PuzzleParser().parse(dat)

        but it tries to read one puzzle at a time and yield them without
        reading the whole file at once.
    """

    pp = PuzzleParser()
    cur_lines = ""

    def my_yield(x):  # pragma: no cover
        if isinstance(x, Puzzle):
            yield x
        else:
            yield from x

    with open(file, "r") as fh:
        for line in fh:
            if "-" in line and "-" in cur_lines:
                yield from my_yield(pp.parse(cur_lines))
                cur_lines = line
                continue
            cur_lines += line
    if cur_lines:
        yield from my_yield(pp.parse(cur_lines))


class PuzzleTransformer(Transformer):
    def given(self, v):
        return int(v[0])

    def cell_item(self, v):
        return v[0]

    def open(self, _):
        return None

    def cell_row(self, v):
        return v

    def puzzle_line(self, v):
        return v[0] + v[1] + v[2]

    def box_line(self, v):
        return v

    def puzzle(self, v):
        puzzle = Puzzle()
        dat = v[3] + v[4] + v[5]
        for i in range(9):
            for j in range(9):
                if dat[i][j] is not None:
                    # this would work:
                    # puzzle[ (i+1, j+1) ] = dat[i][j]
                    #
                    # but would fail to mark the cell as a given
                    puzzle[(i + 1, j + 1)].given = dat[i][j]
        return puzzle

    def puzzle_list(self, v):  # pragma: no cover
        return v


def PuzzleParser():
    l = Lark(
        """
        ?start: puzzle_list
        ?puzzle_list: puzzle*
        puzzle: header header header box_line box_line box_line
        box_line: puzzle_line puzzle_line puzzle_line
        puzzle_line: cell_row cell_row cell_row
        cell_row: cell_item cell_item cell_item
        cell_item: given | open
        header: /-+/
        given: GDIGIT
        open: OPENCHAR
        GDIGIT: /[1-9]/
        OPENCHAR: "."
        %import common.WS
        %ignore WS
    """,
        parser="lalr",
        transformer=PuzzleTransformer(),
    )

    return l
