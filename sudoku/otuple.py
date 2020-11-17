#!/usr/bin/env python
# coding: utf-8

from fnmatch import fnmatch
from .filt import acceptable_index_value
from .element import Element

BOX_CLASS = None  # populated when Box loads (circular import resolution)


class Otuple(tuple):
    """ (aka One-starting tuple): a boring tuple() that pretends to be indexed 1-9

        Otuples also have silly search features releated to grid elements.
    """

    def __getitem__(self, idx):
        global BOX_CLASS
        try:
            idx = int(idx)
        except (ValueError, TypeError):
            if isinstance(idx, str):
                if "b" in idx or "r" in idx or "c" in idx or "*" in idx:

                    def sgenerator(it, wanted):
                        for item in it:
                            if isinstance(item, Element):
                                if fnmatch(item.short, wanted):
                                    yield item
                            elif isinstance(item, BOX_CLASS):
                                yield from sgenerator(item, wanted)

                    return set(sgenerator(self, idx))
        if isinstance(idx, (list, set, tuple)):
            ret = set()
            for x in idx:
                item = self[x]
                if isinstance(item, (set,BOX_CLASS,Otuple)):
                    ret = ret.union(item)
                else:
                    ret.add(item)
            return ret
        idx = acceptable_index_value(idx)
        return super().__getitem__(idx - 1)
