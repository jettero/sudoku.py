#!/usr/bin/env python
# coding: utf-8

import pytest
from sudoku.box import Box

@pytest.fixture(scope="function")
def box4(p_45m):
    yield p_45m.boxes[4]


def test_init():
    b = Box()
    assert len(tuple(b)) == 9

    c = Box(*b)
    assert len(tuple(c)) == 9

    with pytest.raises(ValueError):
        Box(*(list(b)[2:]))

def test_marks(box4):
    # b = Box()
    #
    # we can't just make a new box, the elements won't have their .row, .col,
    # .box set. has() returns a set, which is keyed on (.row,.col,.box)

    assert len(box4.has(1, inc_pencil=True)) == 0
    assert len(box4.has(2, inc_center=True)) == 0
    box4.set_pencil_marks(1)
    assert len(box4.has(1, inc_pencil=True)) == 9
    assert len(box4.has(2, inc_center=True)) == 0
    box4.set_center_marks(2)
    assert len(box4.has(1, inc_pencil=True)) == 9
    assert len(box4.has(2, inc_center=True)) == 9
    box4.clear_marks()
    assert len(box4.has(1, inc_pencil=True)) == 0
    assert len(box4.has(2, inc_center=True)) == 0

# elements_in_attr()
def test_elements_of_box_4_in_col2(box4):
    res = box4.elements_in_attr(2, attr="col")

    assert len(res) == 3
    assert set(x.box for x in res) == {
        4,
    }
    assert set(x.col for x in res) == {
        2,
    }
    assert set(x.row for x in res) == {4, 5, 6}


# element_has_val()
def test_elements_in_box4_having_5(box4):
    res = box4.has(5, inc_val=False)
    assert len(res) == 0

    res = box4.has(5, inc_val=False, inc_pencil=True)
    assert len(res) == 2

    res = box4.has(5, inc_val=False)
    assert len(res) == 0

    res = box4.has(5, inc_val=True, inc_pencil=True)
    assert len(res) == 2


# attrs_containing_val()
def test_columns_in_box4_with_5(box4):
    res = box4.attrs_containing_val(5, attr="col", inc_pencil=True)
    assert res == {1, 3}


# val_restricted_to_single_attr()
def test_columns_in_box4_with_4(box4):
    res = box4.single_attr_containing_val(4, attr="col", inc_pencil=True)
    assert res == 2
