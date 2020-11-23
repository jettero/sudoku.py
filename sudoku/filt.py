#!/usr/bin/env python
# coding: utf-8

from .const import ELEMENT_VALUES


def acceptable_element_value(x, none_ok=False):
    if x is None:
        if none_ok:
            return x
    elif 1 <= x <= 9:
        return x
    raise ValueError('values must be in the range 1-9')


def acceptable_index_value(x, none_ok=False):
    if x is None:
        if none_ok:
            return x
    elif 1 <= x <= 9:
        return x
    raise IndexError('indexes must be in the range 1-9')


def element_has_val(e, val, inc_val=True, inc_marks=True):
    if inc_val and e.value == val:
        return True
    if inc_marks and val in e.marks:
        return True
    return False


def attrs_containing_val(box, val, attr="row", inc_val=True, inc_marks=True):
    return set(
        getattr(e, attr)
        for e in box
        if element_has_val(e, val, inc_val=inc_val, inc_marks=inc_marks)
    )


def val_restricted_to_single_attr(box, val, attr="row", inc_val=True, inc_marks=True):
    s = attrs_containing_val(box, val, attr=attr, inc_val=inc_val, inc_marks=inc_marks)
    if len(s) == 1:
        return next(iter(s))


def elements_in_attr(box, no, attr="row"):
    return set(x for x in box if getattr(x, attr) == no)
