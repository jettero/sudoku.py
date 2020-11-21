#!/usr/bin/env python
# coding: utf-8

import logging
from sudoku.rules.uniqueness import main as u_main

log = logging.getLogger(__name__)


def test_binary_pairs(p_1t9m4):
    u_main(p_1t9m4)
    log.debug("computed p_1t9m4:\n%s", p_1t9m4)

    assert tuple(x.value for x in p_1t9m4 if x.value and not x.given) == (4, 4)
