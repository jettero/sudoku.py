#!/usr/bin/env python
# coding: utf-8


def test_things(p_45, p_45m):
    p_45[1, 1].given = 7

    assert p_45 is not p_45m
    assert p_45m[1, 1].value is None
