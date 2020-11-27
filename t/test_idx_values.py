#!/usr/bin/env python
# coding: utf-8

import pytest
from sudoku.filt import acceptable_element_value, acceptable_index_value

def test_index_value():
    for i in range(1,9+1):
        assert acceptable_index_value(i) == i

    assert acceptable_index_value(None, none_ok=True) == None

    with pytest.raises(IndexError):
        assert acceptable_index_value(None)

    with pytest.raises(IndexError):
        assert acceptable_index_value(0)

    with pytest.raises(IndexError):
        assert acceptable_index_value(10)

def test_element_value():
    for i in range(1,9+1):
        assert acceptable_element_value(i) == i

    assert acceptable_element_value(None, none_ok=True) == None

    with pytest.raises(ValueError):
        assert acceptable_element_value(None)

    with pytest.raises(ValueError):
        assert acceptable_element_value(0)

    with pytest.raises(ValueError):
        assert acceptable_element_value(10)
