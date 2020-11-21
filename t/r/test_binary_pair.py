#!/usr/bin/env python
# coding: utf-8

import logging

log = logging.getLogger(__name__)

from sudoku.rules.value_restrictions import main as vr_main
from sudoku.rules.binary_pairs import main as bp_main


def test_binary_pairs(p_45):
    while vr_main(p_45, {}):
        pass

    while bp_main(p_45, {}):
        pass

    log.debug("computed p_45:\n%s", p_45)

    assert set(x.loc for x in p_45 if x.center) == set(((1, 2, 1), (1, 2, 3)))
    assert set(x.loc for x in p_45 if x.pencil) == set(
        ((4, 4, 1), (4, 4, 3), (6, 6, 8), (6, 6, 9))
    )
