#!/usr/bin/env python
# coding: utf-8

import logging
import pytest

log = logging.getLogger(__name__)

main81 = False
try:
    from sudoku.rules.eighty_one import main as main81
except ModuleNotFoundError:
    raise
    pass

@pytest.mark.skipif(main81 is False, reason="eighty_one rules module required, but missing")
def test_test81(p7):
    with open("/tmp/wtf0.txt", 'w') as fh:
        fh.write(str(p7))

    while main81(p7):
        pass

    with open("/tmp/wtf1.txt", 'w') as fh:
        fh.write(str(p7))

    assert p7[6,6].value is None
    assert p7[6,6].center == {5,8}
    assert p7.broken is False

    p7[2,6] = 5 # this breaks the puzzle

    with open("/tmp/wtf2.txt", 'w') as fh:
        fh.write(str(p7))

    while main81(p7):
        pass

    with open("/tmp/wtf3.txt", 'w') as fh:
        fh.write(str(p7))

    assert p7[6,6].value is None
    assert p7[6,6].center == set()
    assert p7.broken is True
