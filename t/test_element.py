#!/usr/bin/env python
# coding: utf-8

from sudoku import Element
from sudoku.element import CELL_WIDTH

def test_element_repr():
    assert repr(Element()) == "E"
    assert repr(Element(value=4)) == "E<4>"
    assert repr(Element(value=4, given=True)) == "E<4>"
    assert repr(Element(value=4, row=1, col=1)) == "E(b1r1c1)<4>"
    assert repr(Element(value=4, row=7, col=6)) == "E(b8r7c6)<4>"
    assert repr(Element(row=7, col=6)) == "E(b8r7c6)"

def test_value_things():
    B = b,r,c = (3,2,9)
    L = (r,c)

    vi = Element(value=4, row=r, col=c)
    gi = Element(value=4, given=True, row=r, col=c)
    vs = Element(); vs.value = 4
    gs = Element(); gs.given = 4

    for e in (vs,gs):
        e.row = r
        e.col = c

    for e in (vi,gi,vs,gs):
        assert e.value == 4
        assert e.loc == B
        e.reset()

    for e in (vi,vs):
        assert e.value is None
        assert e.loc == B

    for e in (gi,gs):
        assert e.value == 4
        assert e.loc == B

def test_element_sort():
    e = Element(4,5,6)
    f = Element(7,8,9)
    g = Element(1,8,9)

    assert f>e
    assert e<f
    assert not f<e
    assert not e>f
    assert not (f<g or f>g)
    assert f == g
    assert e != g
    assert e<f<=g

def test_element_as_cell():
    e = Element()
    for i in range(1,10):
        e.value = i
        for line in e.as_cell.splitlines():
            assert len(line) == CELL_WIDTH

        e.reset()
        e.add_pencil_marks(i)
        assert f'{i}' in e.as_cell
        for j in set(range(1,10)) - {i,}:
            assert f'{j}' not in e.as_cell

        e.reset()
        e.add_center_marks(i)
        assert f'{i}' in e.as_cell
        for j in set(range(1,10)) - {i,}:
            assert f'{j}' not in e.as_cell

    e.reset()
    e.add_pencil_marks(4,5,6)
    assert '4' in e.as_cell
    assert '5' in e.as_cell
    assert '6' in e.as_cell

def test_element_assignments():
    e = Element()
    e.given = 8

    assert e.value == 8

    f = Element()
    f.value = e

    assert f.value == e.value

    e.reset()
    f.reset()

    assert e.value == 8
    assert f.value is None

    assert e.given is True
    e.value = None
    assert e.given is True
    assert e.value is None

    assert e.given is True
    e.given = None
    assert e.given is False
    assert e.value is None

def test_add_remove_marks():
    e = Element()
    assert e.marks == set()

    e.add_pencil_marks(1)
    assert e.marks == {1,}
    e.remove_pencil_marks(1)
    assert e.marks == set()

    e.add_center_marks(1)
    assert e.marks == {1,}
    e.remove_center_marks(1)
    assert e.marks == set()

    e.add_center_marks(1)
    e.add_pencil_marks(1)
    assert e.marks == {1,}
    e.remove_marks(1)
    assert e.marks == set()

    e.add_center_marks(1)
    e.add_pencil_marks(1)
    assert e.marks == {1,}
    e.clear_marks()
    assert e.marks == set()

def test_element_description(p7):
    e = p7[2,6]

    e.set_pencil_marks(2,6)
    e.set_center_marks(3,7)

    assert str(e) == "E(b2r2c6)"
    assert repr(e) == "E(b2r2c6|p26|c37)"

    e.value = 3

    assert str(e) == "E(b2r2c6)<3>"
    assert repr(e) == "E(b2r2c6)<3>"
