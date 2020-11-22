#!/usr/bin/env python
# coding: utf-8

import logging

log = logging.getLogger(__name__)

from sudoku.rules.value_restrictions import main as vr_main
from sudoku.rules.binary_pairs import main as bp_main


def test_binary_pairs_p_45(p_45):
    while vr_main(p_45, {}):
        pass

    while bp_main(p_45, {}):
        pass

    log.debug("computed p_45:\n%s", p_45)

    assert set(x.loc for x in p_45 if x.center) == set(((1, 2, 1), (1, 2, 3)))
    assert set(x.loc for x in p_45 if x.pencil) == set(
        ((4, 4, 1), (4, 4, 3), (6, 6, 8), (6, 6, 9))
    )

def test_binary_pairs_p_bp(p_bp):
    p_bp[9,4].add_pencil_marks(4,5)
    p_bp[9,5].add_pencil_marks(4,5)
    p_bp[2,9].add_pencil_marks(4,5)
    p_bp[7,9].add_pencil_marks(4,5)

    while bp_main(p_bp, {}):
        pass

    log.debug("computed p_bp:\n%s", p_bp)

    assert set(x.loc for x in p_bp if x.center) == {(8,9,4), (8,9,5), (3,2,9), (9,7,9)}
