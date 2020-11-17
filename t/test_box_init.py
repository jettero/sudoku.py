#!/usr/bin/env python
# coding: utf-8

import pytest
from sudoku.box import Box


def test_init():
    b = Box()
    assert len(tuple(b)) == 9

    c = Box(*b)
    assert len(tuple(c)) == 9

    with pytest.raises(ValueError):
        Box(*(list(b)[2:]))
