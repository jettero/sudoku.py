#!/usr/bin/env python
# coding: utf-8

import pytest

@pytest.fixture
def p_bpm(p_bp):
    cloned = p_bp.clone()
    cloned[9,4].add_pencil_marks(4,5)
    cloned[9,5].add_pencil_marks(4,5)
    cloned[2,9].add_pencil_marks(4,5)
    cloned[7,9].add_pencil_marks(4,5)
    cloned[2,2].value = 4
    yield cloned

def test_puzzle_transpose(p_bpm):
    cloned = p_bpm.clone(transpose=True)
    assert cloned[2,2].value is None
    assert not cloned[2,2].given
    assert cloned[9,4].value == 7
    assert cloned[9,4].given
    assert cloned[4,9].pencil == set()

def test_puzzle_transpose_copy_all(p_bpm):
    cloned = p_bpm.clone(transpose=True, copy_all=True)
    assert cloned[2,2].value == 4
    assert not cloned[2,2].given
    assert cloned[9,4].value == 7
    assert cloned[9,4].given
    assert cloned[4,9].pencil == {4,5}

def test_puzzle_transpose_with_marks(p_bpm):
    cloned = p_bpm.clone(transpose=True, with_marks=True)
    assert cloned[2,2].value is None
    assert not cloned[2,2].given
    assert cloned[9,4].value == 7
    assert cloned[9,4].given
    assert cloned[4,9].pencil == {4,5}

def test_puzzle_copy(p_bp):
    p1 = p_bp.clone()
    p2 = p_bp.copy()

    assert p1 is not p2
    for e1,e2 in zip(p1,p2):
        assert e1.value == e2.value
        assert e1.pencil == e2.pencil
        assert e1.center == e2.center
        assert e1 is not e2

    p1[1,1].set_pencil_marks(3)
    p2[1,1].set_pencil_marks(2)

    assert p1[1,1].pencil != p2[1,1].pencil
