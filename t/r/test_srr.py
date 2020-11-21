#!/usr/bin/env python
# coding: utf-8

import logging
from sudoku.rules.single_rowcol_restricted import main as srr_main

log = logging.getLogger(__name__)


def test_binary_pairs(p_srr):
    for box in (p_srr.boxes[7], p_srr.boxes[3]):
        for e in box:
            if e.value:
                continue
            e.add_pencil_marks(4,5,6)

    srr_main(p_srr)
    log.debug("computed p_srr:\n%s", p_srr)

    assert len(p_srr.has(1, inc_val=False, inc_marks=True)) == 3
    assert len(p_srr.has(2, inc_val=False, inc_marks=True)) == 1
    assert len(p_srr.has(3, inc_val=False, inc_marks=True)) == 3
    assert len(p_srr.has(4, inc_val=False, inc_marks=True)) == 9
    assert len(p_srr.has(5, inc_val=False, inc_marks=True)) == 9

    assert len(p_srr.has(6, inc_marks=True)) == 15
