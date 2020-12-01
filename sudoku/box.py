#!/usr/bin/env python
# coding: utf-8

import weakref
import sudoku.otuple as otuple
from .otuple import Otuple
from .element import Element
from .filt import (
    attrs_containing_val,
    val_restricted_to_single_attr,
    element_has_val,
    elements_in_attr,
)
from .const import BOX_NUMBERS


class Box:

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

        # In Box, this makes no sense but child classes Row and Col need this
        if idx is not None:
            self.idx = idx

    def has(self, val, inc_val=True, inc_marks=False):
        return set(
            x
            for x in self
            if element_has_val(x, val, inc_val=inc_val, inc_marks=inc_marks)
        )

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

    def __repr__(self):
        e = " ".join(repr(e) for e in self)
        return f"{self.cname}[{e}]"

    @property
    def idx(self):
        return self[1].box
    # this property has setters in Row and Col

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
