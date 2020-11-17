#!/usr/bin/env python
# coding: utf-8

import pytest

@pytest.fixture(scope='function')
def box4(five_six_puzzle):
    yield five_six_puzzle.boxes[4]

# elements_in_attr()
def test_elements_of_box_4_in_col2(box4):
    res = box4.elements_in_attr(2, attr='col')

    assert len(res) == 3
    assert set(x.box for x in res) == {4,}
    assert set(x.col for x in res) == {2,}
    assert set(x.row for x in res) == {4,5,6}

# element_has_val()
def test_elements_in_box4_having_5(box4):
    res = box4.has(5, inc_val=False, inc_marks=False)
    assert len(res) == 0

    res = box4.has(5, inc_val=False, inc_marks=True)
    assert len(res) == 2

    res = box4.has(5, inc_val=True, inc_marks=False)
    assert len(res) == 0

    res = box4.has(5, inc_val=True, inc_marks=True)
    assert len(res) == 2

# attrs_containing_val()
def test_columns_in_box4_with_5(box4):
    res = box4.attrs_containing_val(5, attr='col')
    assert res == {2,}

# val_restricted_to_single_attr()
def test_columns_in_box4_with_5(box4):
    res = box4.single_attr_containing_val(5, attr='col')
    assert res == 2
