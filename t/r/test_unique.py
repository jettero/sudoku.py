#!/usr/bin/env python
# coding: utf-8

import logging
import pytest

log = logging.getLogger(__name__)

main = False
try:
    from sudoku.rules.unique import main, init
except ModuleNotFoundError:
    pass

@pytest.mark.skipif(main is False, reason="unique rules module required, but missing")
def test_testu(p7):
    with open("/tmp/wtf0.txt", 'w') as fh:
        fh.write(str(p7))

    init(p7)
    while main(p7):
        pass

    with open("/tmp/wtf1.txt", 'w') as fh:
        fh.write(str(p7))

    assert p7[6,6].value is None
    assert p7[6,6].center == {5,8}
    assert p7.broken is False

    p7[2,6] = 5
    p7[8,6] = 8

    while main(p7):
        pass

    with open("/tmp/wtf2.txt", 'w') as fh:
        fh.write(str(p7))

    assert p7.broken is True
    assert p7[6,6].center == set()
