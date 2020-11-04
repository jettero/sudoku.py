#!/usr/bin/env python
# coding: utf-8

import re
import weakref
from tabulate import tabulate
from pyfiglet import Figlet

BOX_NUMBERS = ROW_NUMBERS = COLUMN_NUMBERS = ELEMENT_VALUES = tuple(range(1, 9 + 1))

# NOTE: CELL_WIDTH is pretty fiddly. To get the grid to work out, at
# CELL_WIDTH=6, you have to width=CELL_WIDTH+1; at CELL_WIDTH=8 you have to
# width=CELL_WIDTH+2. I haven't thought about why since I got it working, but
# it's not screaming: I'm super stable, depend on me.

CELL_WIDTH = 8
FUCKED_UP_LINEAR_SCALING = 2
FIG = Figlet(
    font="small", justify="center", width=CELL_WIDTH + FUCKED_UP_LINEAR_SCALING
)
BLANK = re.sub(r"[^\n]", " ", FIG.renderText("X"))

# rather than making an adaptive pencil mark layout; ... I just hardcoded it... lame
PENCIL_POS = ( None,
    (0,1), (0,3), (0,5),
    (1,0), (1,7),
    (3,0),
    (4,1), (4,3), (4,5)
)

CENTER_POS = ( None,
    (1,2), (1,3), (1,4),
    (2,2), (2,3), (2,4),
    (3,2), (3,3), (3,4),
)

def acceptable_element_value(x):
    if x is None:
        return x
    if 1 <= x <= 9:
        return x
    raise ValueError(f"values must be one of {ELEMENT_VALUES}")


class Element:
    def __init__(self, value=None, given=False):
        self.value = value
        self.pencil = set()
        self.center = set()
        self.tags = set()
        self.given = given

    def __repr__(self):
        r = ["E"]
        if self.tags:
            tags = "".join(sorted(self.tags))
            r.append(f"({tags})")
        if self.value:
            r.append(f"<{self.value}>")
        return "".join(r)

    @property
    def as_cell(self):
        if self.value:
            def pad():
                for x in FIG.renderText(str(self.value)).split("\n"):
                    if not x:
                        continue
                    if len(x) < CELL_WIDTH:
                        x += " " * (CELL_WIDTH - len(x))
                    yield f"{x}\n"

            return "".join(pad()) #.replace(" ", ".")
        blank = [ list(x) for x in BLANK.split('\n')[:-1] ]
        for i in self.pencil:
            r,c = PENCIL_POS[i]
            blank[r][c] = f'{i}'
        for i in self.center:
            r,c = CENTER_POS[i]
            blank[r][c] = f'{i}'
        return '\n'.join(''.join(x) for x in blank)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, x):
        if isinstance(x, Element):
            x = x.value
        self._value = acceptable_element_value(x)

    def add_pencil_mark(self, *m):
        for a in m:
            a = acceptable_element_value(a)
            self.pencil.add(a)

    def remove_pencil_mark(self, *m):
        for a in m:
            a = acceptable_element_value(a)
            self.pencil.remove(a)

    def add_center_mark(self, *m):
        for a in m:
            a = acceptable_element_value(a)
            self.center.add(a)

    def remove_center_mark(self, *m):
        for a in m:
            a = acceptable_element_value(a)
            self.center.remove(a)

class Otuple(tuple):
    def __getitem__(self, idx):
        if not 1 <= idx <= 9:
            raise IndexError("1 <= idx <= 9")
        return super().__getitem__(idx - 1)


class Box:
    def __init__(self, *e, idx=None):
        if len(e) == 0:
            self.elements = Otuple(Element() for _ in range(9))
        elif len(e) == 9:
            self.elements = Otuple(weakref.ref(x) for x in e)
        else:
            raise ValueError(
                f"A {self.__class__} must receive 0 elements or 9, nothing in between"
            )

        if idx is not None:
            for e in self:
                e.tags.add(f"{self.ccode}{idx}")

    @property
    def cname(self):
        return self.__class__.__name__

    @property
    def ccode(self):
        return self.__class__.__name__[0].lower()

    def __getitem__(self, i):
        e = self.elements[i]
        if isinstance(e, weakref.ref):
            return e()
        return e

    def __setitem__(self, i, v):
        self.elements[i].value = v

    def __iter__(self):
        yield from (self[i] for i in BOX_NUMBERS)

    def __repr__(self):
        e = " ".join(repr(e) for e in self)
        return f"{self.cname}[{e}]"


class Row(Box):
    pass


class Col(Box):
    pass


class Grid:
    def __init__(self):
        self.rows = Otuple(Row(idx=r) for r in ROW_NUMBERS)
        self.cols = Otuple(
            Col(*(r[c] for r in self.rows), idx=c) for c in COLUMN_NUMBERS
        )

        def box_elements(b):
            b -= 1
            c = (3 * b) % 9
            C = tuple(range(c, c + 3))
            r = (b // 3) * 3
            R = tuple(range(r, r + 3))
            for r in R:
                for c in C:
                    yield self.rows[r + 1][c + 1]

        self.boxes = Otuple(Box(*box_elements(b), idx=b) for b in BOX_NUMBERS)

    def __getitem__(self, idx):
        if isinstance(idx, (list, tuple)) and len(idx) == 2:
            return self.rows[idx[0]][idx[1]]
        return self.rows[idx]

    def __setitem__(self, idx, val):
        if isinstance(idx, (list, tuple)) and len(idx) == 2:
            self.rows[idx[0]][idx[1]] = val
            return
        raise IndexError(f"grids require tuple indexes to set elements (given: {idx})")

    def __repr__(self):
        dat = [[x.as_cell for x in row] for row in self.rows]
        return tabulate(dat, tablefmt="grid", stralign=None)
