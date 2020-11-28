#!/usr/bin/env python
# coding: utf-8

from sudoku import Element

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
    e = Element(4,5,6)
    assert '|' in e.as_cell
    assert '_' in e.as_cell
    e.reset()
    e.add_pencil_mark(4,5,6)
    assert '4' in e.as_cell
    assert '5' in e.as_cell
    assert '6' in e.as_cell
