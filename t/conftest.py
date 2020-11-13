#!/usr/bin/env python
# coding: utf-8

import pytest

from sudoku import Puzzle


@pytest.fixture
def empty_puzzle():
    yield Puzzle()
