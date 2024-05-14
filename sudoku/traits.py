#!/usr/bin/env python
# coding: utf-8

# avoid using __getattribute__ by pre-populating things that would normally be
# done via __getattribute__
#
# I think we could prolly do something with meta classes and function
# signatures and populate these as a blessed list or something, but is it
# really worth it? Meh. Long form ftw.

from .filt import element_has_val


class HasTrait:
    def has(self, val, inc_val=True, inc_pencil=False, inc_center=False):
        return set(
            x for x in self if element_has_val(x, val, inc_val=inc_val, inc_pencil=inc_pencil, inc_center=inc_center)
        )


class MarksTrait:
    def add_pencil_marks(self, *a, **kw):
        for e in self:
            e.add_pencil_marks(*a, **kw)

    def set_pencil_marks(self, *a, **kw):
        for e in self:
            e.set_pencil_marks(*a, **kw)

    def remove_pencil_marks(self, *a, **kw):
        for e in self:
            e.remove_pencil_marks(*a, **kw)

    def clear_pencil_marks(self, *a, **kw):
        for e in self:
            e.clear_pencil_marks(*a, **kw)

    def add_center_marks(self, *a, **kw):
        for e in self:
            e.add_center_marks(*a, **kw)

    def set_center_marks(self, *a, **kw):
        for e in self:
            e.set_center_marks(*a, **kw)

    def remove_center_marks(self, *a, **kw):
        for e in self:
            e.remove_center_marks(*a, **kw)

    def clear_center_marks(self, *a, **kw):
        for e in self:
            e.clear_center_marks(*a, **kw)

    def clear_marks(self, *a, **kw):
        for e in self:
            e.clear_marks(*a, **kw)

    def remove_marks(self, *a, **kw):
        for e in self:
            e.remove_marks(*a, **kw)
