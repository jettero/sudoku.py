#!/usr/bin/env python
# coding: utf-8

import pytest
import logging
from sudoku.solver import process_opts, solve, Karen
from sudoku.tools import ListTrueWhenEmpty

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

def test_list_true_when_empty():
    l0 = ListTrueWhenEmpty()
    l1 = ListTrueWhenEmpty([1])
    l2 = ListTrueWhenEmpty([2])

    assert bool(l0) is True
    assert bool(l1) is False
    assert bool(l2) is False

    assert l0
    assert not l1
    assert not l2

def test_p_is_not_broken(any_p):
    assert any_p.check()

def test_solver_doesnt_ruin_any_puzzle(any_q):
    c = any_q.check()
    assert (any_q, c) == (any_q, list())
    assert c

def test_solvers_load_the_same_local_modules():
    assert set(Karen().local_modules) == set(Karen().local_modules)

def LPN(*a, **kw): # list plugin names
    return set(x[0] for x in Karen(*a, **kw).list_name_plugin() if x[1] is not None)

def test_solvers_reject_filters_work():
    lpn_0 = LPN()
    lpn_a = LPN(accept_filter='nop')
    lpn_r = LPN(reject_filter='nop')

    assert lpn_0 != lpn_a
    assert lpn_0 != lpn_r
    assert lpn_a != lpn_r
    assert len(lpn_a) == 1
    assert 't.rules.nop' in lpn_a
    assert 't.rules.nop' not in lpn_r

def test_sometimes_solvers_break(p0):
    import t.rules.nop as tnop

    solver = Karen(accept_filter='nop')

    s = solver.solve(p0)
    assert len(s.history) == 0
    assert s.broken is False

    tnop.RULE_BREAK = True
    s = solver.solve(p0)
    assert len(s.history['.*intentionally broken.*']) == 1
    assert s.broken is False
    tnop.RULE_BREAK = False

    tnop.STEPS = 1 # to test the if puzzle.broken: break
    tnop.PUZZLE_BREAK = True
    s = solver.solve(p0)
    assert len(s.history) == 0
    assert s.broken is True
    tnop.PUZZLE_BREAK = False

    tnop.PUZZLE_SUBTLE_BREAK = True
    s = solver.solve(p0)
    assert len(s.history['.*puzzle broke during t.rules.nop.*']) == 1
    assert s.broken is True
    tnop.PUZZLE_SUBTLE_BREAK = False

    tnop.RETURN_BULLSHIT = True
    s = solver.solve(p0)
    assert len(s.history['.*failed to return an int.*']) == 1
    assert s.broken is False
    tnop.RETURN_BULLSHIT = False

    tnop.STEPS = 1
    s = solver.solve(p0)
    assert len(s.history) == 0
    assert s.broken is False

def test_sometimes_solvers_work(p_solved, p_empty):
    assert p_solved.solved == True
    assert p_empty.solved == False
