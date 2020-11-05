#!/usr/bin/env python
# coding: utf-8

from .grid import Grid
from lark import Lark, Transformer

class PuzzleTransformer(Transformer):
    def given(self, v):
        return int(v[0])

    def cell_item(self, v):
        return v[0]

    def open(self, v):
        return None

    def cell_row(self, v):
        return v

    def puzzle_line(self, v):
        return v[0] + v[1] + v[2]

    def box_line(self, v):
        return v

    def puzzle(self, v):
        grid = Grid()
        dat = v[3] + v[4] + v[5]
        for i in range(9):
            for j in range(9):
                if dat[i][j] is not None:
                    # this would work:
                    # grid[ (i+1, j+1) ] = dat[i][j]
                    #
                    # but would fail to mark the cell as a given
                    grid[ (i+1, j+1) ].given = dat[i][j]
        return grid

    def puzzle_list(self, v):
        return v

def PuzzleParser():
    l = Lark('''
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
    ''',

    parser='lalr',
    transformer=PuzzleTransformer()

    )

    return l
