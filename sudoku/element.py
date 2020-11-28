#!/usr/bin/env python
# coding: utf-8

import re
from pyfiglet import Figlet
from .tools import PYTR, rc2b
from .filt import acceptable_element_value

# NOTE: CELL_WIDTH is pretty fiddly. To get the grid to work out, at
# CELL_WIDTH=6, you have to width=CELL_WIDTH+1; at CELL_WIDTH=8 you have to
# width=CELL_WIDTH+2. I haven't thought about why since I got it working, but
# it's not screaming: I'm super stable, depend on me.

FUCKED_UP_LINEAR_SCALING = 2
CELL_WIDTH = 8
FIG = Figlet(
    font="small", justify="center", width=CELL_WIDTH + FUCKED_UP_LINEAR_SCALING
)
BLANK = re.sub(r"[^\n]", " ", FIG.renderText("X"))

# rather than making an adaptive pencil mark layout; ... I just hardcoded it... lame
PENCIL_POS = (
    None,
    (0, 1),
    (0, 3),
    (0, 5),
    (1, 0),
    (1, 7),
    (3, 0),
    (4, 1),
    (4, 3),
    (4, 5),
)

CENTER_POS = (
    None,
    (1, 2),
    (1, 3),
    (1, 4),
    (2, 2),
    (2, 3),
    (2, 4),
    (3, 2),
    (3, 3),
    (3, 4),
)


class Element:
    _row = _col = _value = _given = None

    def __init__(self, value=None, row=None, col=None, given=False):
        self._center = set()
        self._pencil = set()
        self.row = row
        self.col = col
        self.given = given
        self.value = value

    def reset(self):
        self.clear_marks()
        if not self.given:
            self.value = None

    def __repr__(self):
        r = ["E"]
        if self.tags:
            r.append(f"({self.short})")
        if self.value:
            r.append(f"<{self.value}>")
        return "".join(r)

    def __eq__(self, other):
        if isinstance(other, Element):
            other = other.loc
        return self.loc == other

    def __gt__(self, other):
        if isinstance(other, Element):
            other = other.loc
        return self.loc > other

    def __ge__(self, other):
        if isinstance(other, Element):
            other = other.loc
        return self.loc >= other

    @property
    def loc(self):
        return (self.box, self.row, self.col)

    @property
    def short(self):
        return "".join(self.tags)

    @property
    def box(self):
        return self._box

    @property
    def row(self):
        return self._row

    def _compute_box(self):
        self._box = rc2b(self._row, self._col)

    @row.setter
    def row(self, v):
        self._row = acceptable_element_value(v, none_ok=True)
        self._compute_box()

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, v):
        self._col = acceptable_element_value(v, none_ok=True)
        self._compute_box()

    column = col

    @property
    def tags(self):
        ret = list()
        for t in ('box', 'row', 'col'):
            a = getattr(self, t)
            if a:
                ret.append(f'{t[0]}{a}')
        return ret

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

            return "".join(pad())  # .replace(" ", ".")
        blank = [list(x) for x in BLANK.split("\n")[:-1]]
        for i in self._pencil:
            r, c = PENCIL_POS[i]
            blank[r][c] = f"{i}"
        for i in self._center:
            r, c = CENTER_POS[i]
            blank[r][c] = f"{i}"
        return "\n".join("".join(x) for x in blank)

    @property
    def value(self):
        return self._value

    @property
    def center(self):
        return set(self._center)

    @property
    def pencil(self):
        return set(self._pencil)

    @property
    def marks(self):
        return self.pencil.union(self.center)

    @value.setter
    def value(self, x):
        if isinstance(x, Element):
            x = x.value
        self._value = acceptable_element_value(x, none_ok=True)
        self.clear_marks()

    @property
    def given(self):
        return self._given

    @given.setter
    def given(self, v):
        if v is None:
            self._given = False
            self.value = None
        elif isinstance(v, bool):
            self._given = v
        else:
            self._given = True
            self.value = int(v)

    def add_pencil_mark(self, *m):
        for a in m:
            a = acceptable_element_value(a)
            self._pencil.add(a)

    def remove_pencil_mark(self, *m):
        for a in m:
            a = acceptable_element_value(a)
            if a in self._pencil:
                self._pencil.remove(a)

    def clear_pencil_marks(self):
        self._pencil.clear()

    def add_center_mark(self, *m):
        for a in m:
            a = acceptable_element_value(a)
            self._center.add(a)

    def remove_center_mark(self, *m):
        for a in m:
            a = acceptable_element_value(a)
            if a in self._center:
                self._center.remove(a)

    def clear_center_marks(self):
        self._center.clear()

    def remove_mark(self, *m):
        self.remove_center_mark(*m)
        self.remove_pencil_mark(*m)

    def clear_marks(self):
        self.clear_center_marks()
        self.clear_pencil_marks()

    remove_marks = remove_mark
    add_center_marks = add_center_mark
    remove_center_marks = remove_center_mark
    add_pencil_marks = add_pencil_mark
    remove_pencil_marks = remove_pencil_mark
