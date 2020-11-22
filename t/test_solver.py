#!/usr/bin/env python
# coding: utf-8

import logging
from sudoku.solver import process_opts, solve

log = logging.getLogger(__name__)

def test_process_opts():
    opts0 = process_opts(None)
    opts1 = process_opts(['human', 'dog', 'test'])
    opts2 = process_opts('this is my human dog test hybrid')
    opts3 = process_opts('human')
    opts4 = process_opts('dog')

    assert opts0 == set()
    assert opts1 == {'human', 'test'}
    assert opts2 == {'human', 'test'}
    assert opts3 == {'human',}
    assert opts4 == set()

def test_solver_doesnt_ruin_any_puzzle(any_p):
    q = solve(any_p)
    c = q.check()
    ok = bool(c)
    if not c:
        log.info('original puzzle that failed:\n%s\n\nour "solution":\n%s\nsolution history:', any_p, q)
        for item in q.history:
            log.info('  %s', item)
        log.info('problems:')
        for item in c:
            log.error("  %s", item)
    assert ok
