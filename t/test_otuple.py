#!/usr/bin/env python
# coding: utf-8

def test_otouple(empty_puzzle):
    b1r2 = empty_puzzle['b1r2*']

    assert len(b1r2) == 3
    assert set(x.short for x in b1r2) == {'b1r2c1', 'b1r2c2', 'b1r2c3'}

    b1r2c3 = empty_puzzle['b1r2c3']
    assert len(b1r2c3) == 1
    assert next(iter(b1r2c3)) is empty_puzzle[ 2,3 ]

    r1 = empty_puzzle.rows['*r1*']
    assert len(r1) == 9

    r1r2 = empty_puzzle.rows['*r1*', '*r2*']
    assert len(r1r2) == 18

    r1r2 = empty_puzzle.rows[1,2]
    assert len(r1r2) == 18

    r1 = empty_puzzle.rows[1]
    rf = r1['*c2']
    assert len(rf) == 1

    r1 = empty_puzzle.rows[1]
    rf = r1[1,2]
    assert len(rf) == 2

    r1 = empty_puzzle.rows[1]
    rf = r1[1,]
    assert len(rf) == 1
