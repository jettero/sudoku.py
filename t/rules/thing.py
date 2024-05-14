#!/usr/bin/env python
# coding: utf-8

from sudoku.rules import hookimpl

RETURN_BULLSHIT = PUZZLE_SUBTLE_BREAK = PUZZLE_BREAK = RULE_BREAK = False

STEPS = 0

@hookimpl
def main(puzzle, opts=set()):
    global STEPS
    if PUZZLE_BREAK:
        puzzle.broken = True
    if PUZZLE_SUBTLE_BREAK:
        puzzle[1,1] = 9
        puzzle[1,2] = 9
    if RULE_BREAK:
        raise Exception("intentionally broken")
    if RETURN_BULLSHIT:
        return # anything that's not an int will do to trigger HookValueError in solver
    STEPS = STEPS - 1
    return 1 if STEPS >= 0 else 0
