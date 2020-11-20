#!/usr/bin/env python
# coding: utf-8

from collections import OrderedDict
import re

class FrozenHistory(tuple):
    def __getitem__(self, search):
        search = re.compile(search)
        return tuple(x for x in self if search.search(x))

    def __str__(self):
        return "\n".join(self) + "\n"


class History(OrderedDict):
    def append(self, thing, source):
        self[thing.strip()] = source

    def freeze(self):
        return FrozenHistory(f"[{v}] {k}" for k, v in self.items())
