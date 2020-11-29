#!/usr/bin/env python
# coding: utf-8

from sudoku import Puzzle

def test_puzzle_context_string():
    s = 'supz'
    p = Puzzle()
    a = p.context(s, pfft=set)['pfft']
    b = p.context(s, pfft=set)['pfft']
    assert a is b
    assert isinstance(a, set)

def test_puzzle_context_function():
    s = 'supz'
    p = Puzzle()
    a = p.context(test_puzzle_context_function, pfft=set)['pfft']
    b = p.context(test_puzzle_context_function, pfft=set)['pfft']
    assert a is b
    assert isinstance(a, set)

def test_puzzle_context_some_dict():
    s = dict(supz='supz')
    p = Puzzle()
    a = p.context(s, pfft=set)['pfft']
    b = p.context(s, pfft=set)['pfft']
    assert a is b
    assert isinstance(a, set)
