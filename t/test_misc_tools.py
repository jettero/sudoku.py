#!/usr/bin/env python
# coding: utf-8


from sudoku.tools import format_digits_in_row_cols

def test_format_center_digits():
    s = ''
    for i in range(1,10):
        s += f'{i}'
        f = format_digits_in_row_cols(s)
        assert 2 <= len(f) <= 3
        for item in f:
            assert len(item) <= 4
