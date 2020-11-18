#!/usr/bin/env python
# coding: utf-8

import pytest
from sudoku.tools import PYTR

@pytest.fixture
def aba_pat():
    yield r'(?P<a1>a)(?P<b>b)(?P<a2>a)'

@pytest.fixture(scope='function')
def aba(aba_pat):
    yield PYTR(aba_pat)

def test_pytr_match(aba):
    assert not aba.match('this is aba')
    assert aba.groups == tuple()
    assert aba.groupdict == dict()

def test_pytr_search(aba):
    assert aba.search('this is aba')
    assert aba.groups == ('a', 'b', 'a')
    assert aba.groupdict.a1 == 'a'
    assert aba.groupdict.b  == 'b'
    assert aba.groupdict.a2 == 'a'

    assert aba[0] == 'a'
    assert aba[1] == 'b'
    assert aba[2] == 'a'

    assert aba['a1'] == 'a'
    assert aba['b']  == 'b'
    assert aba['a2'] == 'a'

def test_pytr_failkey(aba):
    aba.match('supz')
    with pytest.raises(TypeError):
        assert not aba[{'supz',}]

def test_pytr_repr(aba, aba_pat):
    assert repr(aba) == aba_pat
