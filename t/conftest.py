#!/usr/bin/env python
# coding: utf-8

import pytest

from sudoku import Grid


@pytest.fixture
def empty_grid():
    yield Grid()
