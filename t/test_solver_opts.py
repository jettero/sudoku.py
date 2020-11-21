#!/usr/bin/env python
# coding: utf-8

from sudoku.solver import process_opts

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
