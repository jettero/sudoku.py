#!/usr/bin/env python
# coding: utf-8

import pytest
from sudoku import BOX_MATRIX
from sudoku.tools import brc_iter, rc2b

def test_brc_iter():
    bs = set()
    rs = set()
    cs = set()
    ps = set()

    for b,r,c in brc_iter():
        bs.add(b)
        rs.add(r)
        cs.add(c)
        ps.add( (r,c) )

    assert bs == set(range(1,10))
    assert rs == set(range(1,10))
    assert cs == set(range(1,10))
    assert len(ps) == 81

def test_rc2b():
    for b,r,c in brc_iter():
        assert rc2b(r,c) == b

def test_manual_matrix():
    x = tuple(tuple(rc2b(r,c) for c in range(1,10)) for r in range(1,10))
    assert x == BOX_MATRIX

def test_rc2b_via_element(empty_puzzle):
    for b,r,c in brc_iter():
        assert empty_puzzle[r,c].box == b
