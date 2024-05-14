#!/usr/bin/env python
# coding: utf-8


def test_pencil_marks(empty_puzzle):
    assert len(empty_puzzle.has(1, inc_val=False, inc_pencil=True)) == 0
    empty_puzzle.set_pencil_marks(1)
    assert len(empty_puzzle.has(1, inc_val=False, inc_pencil=True)) == 81
    empty_puzzle.remove_pencil_marks(1)
    assert len(empty_puzzle.has(1, inc_val=False, inc_pencil=True)) == 0
    empty_puzzle.set_pencil_marks(1)
    assert len(empty_puzzle.has(1, inc_val=False, inc_pencil=True)) == 81
    empty_puzzle.clear_pencil_marks()
    assert len(empty_puzzle.has(1, inc_val=False, inc_pencil=True)) == 0
    empty_puzzle.add_pencil_marks(2)
    assert len(empty_puzzle.has(2, inc_val=False, inc_pencil=True)) == 81
    empty_puzzle.set_pencil_marks(1)
    assert len(empty_puzzle.has(1, inc_val=False, inc_pencil=True)) == 81
    assert len(empty_puzzle.has(2, inc_val=False, inc_pencil=True)) == 0
    empty_puzzle.clear_marks()
    assert len(empty_puzzle.has(1, inc_val=False, inc_pencil=True)) == 0

def test_center_marks(empty_puzzle):
    assert len(empty_puzzle.has(1, inc_val=False, inc_center=True)) == 0
    empty_puzzle.set_center_marks(1)
    assert len(empty_puzzle.has(1, inc_val=False, inc_center=True)) == 81
    empty_puzzle.remove_center_marks(1)
    assert len(empty_puzzle.has(1, inc_val=False, inc_center=True)) == 0
    empty_puzzle.set_center_marks(1)
    assert len(empty_puzzle.has(1, inc_val=False, inc_center=True)) == 81
    empty_puzzle.clear_center_marks()
    assert len(empty_puzzle.has(1, inc_val=False, inc_center=True)) == 0
    empty_puzzle.add_center_marks(2)
    assert len(empty_puzzle.has(2, inc_val=False, inc_center=True)) == 81
    empty_puzzle.set_center_marks(1)
    assert len(empty_puzzle.has(1, inc_val=False, inc_center=True)) == 81
    assert len(empty_puzzle.has(2, inc_val=False, inc_center=True)) == 0
    empty_puzzle.clear_marks()
    assert len(empty_puzzle.has(1, inc_val=False, inc_center=True)) == 0

def test_mixed_marks(empty_puzzle):
    assert len(empty_puzzle.has(1, inc_val=False, inc_pencil=True, inc_center=True)) == 0
    assert len(empty_puzzle.has(2, inc_val=False, inc_pencil=True, inc_center=True)) == 0
    assert len(empty_puzzle.has(3, inc_val=False, inc_pencil=True, inc_center=True)) == 0
    empty_puzzle.set_center_marks(1,2)
    empty_puzzle.set_pencil_marks(1,3)
    assert len(empty_puzzle.has(1, inc_val=False, inc_pencil=True, inc_center=True)) == 81
    assert len(empty_puzzle.has(2, inc_val=False, inc_pencil=True, inc_center=True)) == 81
    assert len(empty_puzzle.has(3, inc_val=False, inc_pencil=True, inc_center=True)) == 81
    empty_puzzle.remove_marks(1)
    assert len(empty_puzzle.has(1, inc_val=False, inc_pencil=True, inc_center=True)) == 0
    assert len(empty_puzzle.has(2, inc_val=False, inc_pencil=True, inc_center=True)) == 81
    assert len(empty_puzzle.has(3, inc_val=False, inc_pencil=True, inc_center=True)) == 81
    empty_puzzle.remove_marks(2)
    assert len(empty_puzzle.has(1, inc_val=False, inc_pencil=True, inc_center=True)) == 0
    assert len(empty_puzzle.has(2, inc_val=False, inc_pencil=True, inc_center=True)) == 0
    assert len(empty_puzzle.has(3, inc_val=False, inc_pencil=True, inc_center=True)) == 81
    empty_puzzle.remove_marks(3)
    assert len(empty_puzzle.has(1, inc_val=False, inc_pencil=True, inc_center=True)) == 0
    assert len(empty_puzzle.has(2, inc_val=False, inc_pencil=True, inc_center=True)) == 0
    assert len(empty_puzzle.has(3, inc_val=False, inc_pencil=True, inc_center=True)) == 0
