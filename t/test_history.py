#!/usr/bin/env python
# coding: utf-8

from sudoku.history import History, FrozenHistory

def test_history():
    h = History()

    h.append('supz', 'mang1')
    h.append('supz', 'mang2')
    h.append('stoopid', 'thing')

    assert h['supz'] == 'mang2'
    assert h['stoopid'] == 'thing'

    f = h.freeze()

    assert isinstance(f, FrozenHistory)
    assert tuple(f) == ('[mang2] supz', '[thing] stoopid')
    assert f['stoopid'] == ('[thing] stoopid',)

    assert str(f) == '[mang2] supz\n[thing] stoopid\n'
