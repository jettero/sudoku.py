#!/usr/bin/env python
# coding: utf-8

from sudoku.rules import hookimpl

@hookimpl
def main(puzzle, opts=set()):
    return 0
