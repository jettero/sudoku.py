#!/usr/bin/env python
# coding: utf-8

from sudoku.tools import one_and_the_others_iter, pos_iter, pairs_iter


def test_one_and_the_others_iter():
    blah = tuple(one_and_the_others_iter((1, 2, 3)))
    assert blah == ((1, (2, 3)), (2, (1, 3)), (3, (1, 2)))


def test_pos_iter():
    blah = tuple(pos_iter())
    assert len(blah) == 81
    assert blah[0] == (1, 1)
    assert blah[-1] == (9, 9)

def test_pairs_iter():
    all_pairs = list( pairs_iter() )
    assert len(all_pairs) == 36
    for i in range(1,10,1):
        for j in range(1,10,1):
            if i < j:
                assert (i,j) in all_pairs
