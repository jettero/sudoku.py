#!/usr/bin/env python
# coding: utf-8

from .const import ELEMENT_VALUES


def acceptable_element_value(x, none_ok=False, word="values", ecls=ValueError):
    if x is None:
        if none_ok:
            return x
    elif 1 <= x <= 9:
        return x
    raise ecls(f'{word} must be one of {ELEMENT_VALUES}, not "{x!r}"')


def acceptable_index_value(x, none_ok=False):
    return acceptable_element_value(x, none_ok=none_ok, word="indexes", ecls=IndexError)


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