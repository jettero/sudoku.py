#!/usr/bin/env python
# coding: utf-8

import logging
import pytest

try:
    from sudoku.rules.uniqueness import main as u_main
except ModuleNotFoundError:
    u_main = False

log = logging.getLogger(__name__)


@pytest.mark.skipif(u_main is False, reason="uniqueness rules module required, but missing")
def test_binary_pairs(p_1t9m4):
    u_main(p_1t9m4)
    log.debug("computed p_1t9m4:\n%s", p_1t9m4)

    assert tuple(x.value for x in p_1t9m4 if x.value and not x.given) == (4, 4)
