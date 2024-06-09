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

def test_puzzle_compare_copy_to_clone(any_q):
    p1 = any_q.clone()
    p2 = any_q.copy()

    assert len(p1.history) < len(p2.history)

    assert p1 is not p2
    for e1,e2 in zip(p1,p2):
        assert e1.given == e2.given
        assert len(e1.pencil) <= len(e2.pencil)
        assert len(e1.center) <= len(e2.center)
        assert e1 is not e2

    p1[1,1].set_pencil_marks(3)
    p2[1,1].set_pencil_marks(2)

    assert p1[1,1].pencil == {3,}
    assert p2[1,1].pencil == {2,}
