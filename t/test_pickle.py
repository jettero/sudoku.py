#!/usr/bin/env python
# coding: utf-8

import io
import pickle

from sudoku import solve

def test_pickle(q7):
    b = io.BytesIO()
    p = pickle.Pickler(b)
    p.dump(q7)

    b.seek(0)
    u = pickle.Unpickler(b) # XXX: do I have to b.seek(0) before this? after? never?
    q7_copy = u.load()

    assert q7.is_similar(q7_copy) is True
    assert q7.is_similar(q7_copy, with_marks=True) is True
    assert q7.is_similar(q7_copy, with_history=True) is True

    # these are of course false... just making sure they work
    assert q7.is_similar("q7_copy") is False
    assert q7.is_similar(7)         is False
    assert q7.is_similar([7])       is False
