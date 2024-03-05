#!/usr/bin/env python
# coding: utf-8


def test_given(p_45, p_45m):
    p_45[1, 1].given = 7

    assert p_45 is not p_45m
    assert p_45m[1, 1].value is None

def test_marks(p_45m):
    sum = 0
    for e in p_45m:
        sum += len(e.marks)
        assert len(e.pencil) + len(e.center) == len(e.marks)
    assert sum > 0
