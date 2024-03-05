#!/usr/bin/env python
# coding: utf-8

import logging
import pytest

log = logging.getLogger(__name__)

vr_main = bp_main = False
try:
    from sudoku.rules.value_restrictions import main as vr_main
    from sudoku.rules.binary_pairs import main as bp_main
except ModuleNotFoundError:
    pass

@pytest.fixture
def p_bpm(p_bp):
    cloned = p_bp.clone()
    cloned[9,4].add_pencil_marks(4,5)
    cloned[9,5].add_pencil_marks(4,5)
    cloned[2,9].add_pencil_marks(4,5)
    cloned[7,9].add_pencil_marks(4,5)
    yield cloned

@pytest.fixture
def p_bpmt(p_bpm):
    yield p_bpm.clone(transpose=True, copy_all=True)


@pytest.mark.skipif(bp_main is False, reason="binary_pairs rules module required (but missing)")
@pytest.mark.skipif(vr_main is False, reason="value_restrictions rules module required (but missing)")
def test_binary_pairs_p_45(p_45):
    while vr_main(p_45):
        pass

    while bp_main(p_45):
        pass

    log.debug("computed p_45:\n%s", p_45)

    assert set(x.loc for x in p_45 if x.center) == set(((1, 2, 1), (1, 2, 3)))
    assert set(x.loc for x in p_45 if x.pencil) == set(
        ((4, 4, 1), (4, 4, 3), (6, 6, 8), (6, 6, 9))
    )

@pytest.mark.skipif(bp_main is False, reason="binary_pairs rules module required (but missing)")
def test_binary_pairs_p_bp(p_bpm):
    while bp_main(p_bpm):
        pass

    log.debug("computed p_bpm:\n%s", p_bpm)

    assert set(x.loc[1:] for x in p_bpm if x.center) == {(9,4), (9,5), (2,9), (7,9)}

@pytest.mark.skipif(bp_main is False, reason="binary_pairs rules module required (but missing)")
def test_binary_pairs_p_bp(p_bpmt):
    while bp_main(p_bpmt):
        pass

    log.debug("computed p_bpm (transposed):\n%s", p_bpmt)

    assert set(x.loc[1:] for x in p_bpmt if x.center) == {(4,9), (5,9), (9,2), (9,7)}
