#!/usr/bin/env python
# coding: utf-8

def count_puzzles(file='Puzzles.txt'):
    c = 0
    with open(file, 'r') as fh:
        for line in fh:
            if line.startswith('-'):
                c += 1
    return c

def test_all_puzzles_loaded(puzzles):
    assert len(puzzles) == count_puzzles()
