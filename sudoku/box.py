#!/usr/bin/env python
# coding: utf-8

import types
import weakref
import sudoku.otuple as otuple
from .otuple import Otuple
from .element import Element
from .filt import (
    attrs_containing_val,
    val_restricted_to_single_attr,
    elements_in_attr,
)
from .const import BOX_NUMBERS
from .traits import MarksTrait, HasTrait


class Box(MarksTrait, HasTrait):

    def __init__(self, *e, idx=None):
        self.cname = self.__class__.__name__
        self.lcname = self.cname.lower()
        self.ccode = self.lcname[0]

        if len(e) == 0:
            self._elements = Otuple(Element() for _ in range(9))
        elif len(e) == 9:
            self._elements = Otuple(weakref.ref(x) for x in e)
        else:
            raise ValueError(
                f"A {self.__class__} must receive 0 elements or 9, nothing in between"
            )

        self.idx = idx

    attrs_containing_val = attrs_containing_val
    single_attr_containing_val = val_restricted_to_single_attr
    elements_in_attr = elements_in_attr

    def __getitem__(self, i):
        e = self._elements[i]
        if isinstance(e, weakref.ref):
            return e()
        return e

    def __setitem__(self, i, v):
        self._elements[i].value = v

    def __iter__(self):
        for e in self._elements:
            if isinstance(e, weakref.ref):
                yield e()
            else:
                yield e

    def __str__(self):
        return self.long

    def __repr__(self):
        return self.short

    @property
    def long(self):
        e = " ".join(repr(e) for e in self)
        return f"{self.cname}[{e}]"

    @property
    def idx(self):
        return self[1].box

    @idx.setter
    def idx(self, x):
        pass

    @property
    def short(self):
        n = self.lcname
        return f"{self.lcname} {self.idx}"


class Row(Box):
    @property
    def idx(self):
        return self[1].row

    @idx.setter
    def idx(self, i):
        for e in self:
            e.row = i


class Col(Box):
    @property
    def idx(self):
        return self[1].col

    @idx.setter
    def idx(self, i):
        for e in self:
            e.col = i

otuple.BOX_CLASS = Box
