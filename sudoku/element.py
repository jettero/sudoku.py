#!/usr/bin/env python
# coding: utf-8

import re
import types, inspect
from pyfiglet import Figlet
from .tools import PYTR, rc2b, format_digits_in_row_cols
from .filt import acceptable_element_value

# NOTE: CELL_WIDTH is pretty fiddly. To get the grid to work out, at
# CELL_WIDTH=6, you have to width=CELL_WIDTH+1; at CELL_WIDTH=8 you have to
# width=CELL_WIDTH+2. I haven't thought about why since I got it working, but
# it's not screaming: I'm super stable, depend on me.

FUCKED_UP_LINEAR_SCALING = 2
CELL_WIDTH = 8
FIG = Figlet(font="small", justify="center", width=CELL_WIDTH + FUCKED_UP_LINEAR_SCALING)
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


class Element:
    _row = _col = _value = _given = None

    def __init__(self, value=None, row=None, col=None, given=False):
        self._ = dict(center=set(), pencil=set())
        self.row = row
        self.col = col
        self.given = given
        self.value = value

    def __getstate__(self):
        return (self.row, self.col, self.given, self.value, self._)

    def __setstate__(self, args):
        row, col, given, value, marks, *args = args
        self.__init__(value=value, row=row, col=col, given=given)
        self._ = marks
        if args:
            raise ValueError(f'{self.__class__.__name__}.__setstate__(loc=({row}, {col}), given={given}, value={value}) -- remaining state data: {args}')

    def reset(self):
        self.clear_marks()
        if not self.given:
            self.value = None

    def __str__(self):
        r = ["E"]
        if self.tags:
            r.append(f"({self.short})")
        return "".join(r)

    def __repr__(self):
        r = ["E"]
        if self.tags:
            r.append(f"({self.long})")
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

    def __hash__(self):
        r = 0
        for i, x in zip((1, 10, 100), self.loc):
            if x:
                r += i * x
        return r

    @property
    def loc(self):
        return (self.box, self.row, self.col)

    @property
    def short(self):
        return "".join(self.tags)

    @property
    def long(self):
        return "".join(self.ltags)

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
    def ltags(self):
        ret = self.tags
        for t in ("pencil", "center"):
            a = getattr(self, t)
            if a:
                a = "".join(str(x) for x in sorted(a))
                ret.append(f"|{t[0]}{a}")
        return ret

    @property
    def tags(self):
        ret = list()
        for t in ("box", "row", "col"):
            a = getattr(self, t)
            if a:
                ret.append(f"{t[0]}{a}")
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
        for i in self._["pencil"]:
            r, c = PENCIL_POS[i]
            blank[r][c] = f"{i}"
        fd = format_digits_in_row_cols(self._["center"])
        for r, tup in enumerate(fd):
            for c, item in enumerate(tup):
                blank[r + 1][c + 2] = item
        return "\n".join("".join(x) for x in blank)

    @property
    def value(self):
        return self._value

    @property
    def center(self):
        return set(self._["center"])

    @property
    def pencil(self):
        return set(self._["pencil"])

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

    def add_xmarks(self, X, *m):
        for a in m:
            a = acceptable_element_value(a)
            self._[X].add(a)

    def set_xmarks(self, X, *m):
        self.clear_xmarks(X)
        self.add_xmarks(X, *m)

    def remove_xmarks(self, X, *m):
        for a in m:
            a = acceptable_element_value(a)
            if a in self._[X]:
                self._[X].remove(a)

    def clear_xmarks(self, X):
        self._[X].clear()

    def add_pencil_marks(self, *m):
        self.add_xmarks("pencil", *m)

    def set_pencil_marks(self, *m):
        self.set_xmarks("pencil", *m)

    def remove_pencil_marks(self, *m):
        self.remove_xmarks("pencil", *m)

    def clear_pencil_marks(self):
        self.clear_xmarks("pencil")

    def add_center_marks(self, *m):
        self.add_xmarks("center", *m)

    def set_center_marks(self, *m):
        self.set_xmarks("center", *m)

    def remove_center_marks(self, *m):
        self.remove_xmarks("center", *m)

    def clear_center_marks(self):
        self.clear_xmarks("center")

    def clear_marks(self):
        self.clear_pencil_marks()
        self.clear_center_marks()

    def remove_marks(self, *m):
        self.remove_pencil_marks(*m)
        self.remove_center_marks(*m)
