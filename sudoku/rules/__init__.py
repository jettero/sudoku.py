#!/usr/bin/env python
# coding: utf-8
# pylint: disable=undefined-variable,unused-argument

import pluggy

hookspec = pluggy.HookspecMarker("sudoku")
hookimpl = pluggy.HookimplMarker("sudoku")

@hookspec
def init(puzzle, opts=set()):  # pragma: no cover
    pass # no return values are checked or anything

@hookspec
def main(puzzle, opts=set()):  # pragma: no cover
    # Do whatever the ruleset should do and then return the count of things
    # that were done
    #
    # 0. We use pencil markings in human-esque rules to mark the places where
    #    'x' can be.
    # 1. We use center marks to show only 'x' can go in this cell
    # 2. We set the value of a cell when we figured it out
    #
    # But we try to mimick only things a human could actually figure out. We
    # may cheat slightly (e.g. we have hidden marks that compute literally
    # every restriction on a cell); but we at least try to only mimick rules a
    # human could use.
    #
    # We return did_count, specifically so we know when to stop working —
    # definitely not for any statistical or tracking reasons. (It'd be
    # problematic to try to use did_counts for profiling because what is
    # 'something' exactly? What counts as work?)

    return did_count


del hookspec
del pluggy
