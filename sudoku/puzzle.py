#!/usr/bin/env python
# coding: utf-8

import re
import weakref
from fnmatch import fnmatch
from tabulate import tabulate
from pyfiglet import Figlet
from .tools import PYTR, sudoku_table_format

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

VALID_TAG = PYTR(r"(?P<t>[bcr])(?P<n>[1-9])")

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


def acceptable_element_value(x, none_ok=False):
    if x is None:
        if none_ok:
            return x
    elif 1 <= x <= 9:
        return x
    raise ValueError(f"values must be one of {ELEMENT_VALUES}")


def describe_elements(elements):
    return ", ".join(sorted(e.short for e in elements))


class Element:
    _box = _col = _row = _value = _given = None

    def __init__(self, value=None, given=False):
        self.value = value
        self._pencil = set()
        self._center = set()
        self.tags = set()
        self.given = given

    def reset(self):
        self._pencil = set()
        self._center = set()
        if not self.given:
            self.value = None

    def __repr__(self):
        r = ["E"]
        if self.tags:
            tags = "".join(sorted(self.tags))
            r.append(f"({tags})")
        if self.value:
            r.append(f"<{self.value}>")
        return "".join(r)

    def __gt__(self, other):
        if isinstance(other, Element):
            other = other.short
        return self.short > other

    def __ge__(self, other):
        if isinstance(other, Element):
            other = other.short
        return self.short >= other

    @property
    def loc(self):
        return (self.box, self.row, self.col)

    @property
    def short(self):
        return "".join(sorted(self.tags))

    @property
    def box(self):
        if self._box is None:
            self._box = self._t2n(t="b")
        return self._box

    @property
    def column(self):
        if self._col is None:
            self._col = self._t2n(t="c")
        return self._col

    col = column

    @property
    def row(self):
        if self._row is None:
            self._row = self._t2n(t="r")
        return self._row

    def _t2n(self, t=None):
        for tag in self.tags:
            if VALID_TAG.match(tag):
                if VALID_TAG.groupdict.t == t:
                    return int(VALID_TAG.groupdict.n)

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
        self._pencil = set()
        self._center = set()

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


class Otuple(tuple):
    def __getitem__(self, idx):
        try:
            idx = int(idx)
        except (ValueError,TypeError):
            pass
        if isinstance(idx, str):
            if 'b' in idx or 'r' in idx or 'c' in idx or '*' in idx:
                def sgenerator(it, wanted):
                    for item in it:
                        if isinstance(item, Element):
                            if fnmatch(item.short, wanted):
                                yield item
                        elif isinstance(item, Box):
                            yield from sgenerator(item, wanted)
                return set(sgenerator(self, idx))
        if isinstance(idx, (list,set,tuple)):
            if len(idx) != 1:
                ret = set()
                for x in idx:
                    item = self[x]
                    if isinstance(item, Box):
                        ret = ret.union(item)
                    else:
                        ret.add(item)
                return ret
            idx, = idx
        if not 1 <= idx <= 9:
            raise IndexError("1 <= idx <= 9")
        return super().__getitem__(idx - 1)



class Box:
    def __init__(self, *e, idx=None):
        if len(e) == 0:
            self._elements = Otuple(Element() for _ in range(9))
        elif len(e) == 9:
            self._elements = Otuple(weakref.ref(x) for x in e)
        else:
            raise ValueError(
                f"A {self.__class__} must receive 0 elements or 9, nothing in between"
            )

        if idx is not None:
            for e in self:
                e.tags.add(f"{self.ccode}{idx}")

    def has(self, v):
        for e in self:
            if e.value == v:
                return True
        return False

    @property
    def cname(self):
        return self.__class__.__name__

    @property
    def lcname(self):
        return self.__class__.__name__.lower()

    @property
    def ccode(self):
        return self.__class__.__name__[0].lower()

    def __getitem__(self, i):
        e = self._elements[i]
        if isinstance(e, weakref.ref):
            return e()
        return e

    def __setitem__(self, i, v):
        self._elements[i].value = v

    def __iter__(self):
        yield from (self[i] for i in BOX_NUMBERS)

    def __repr__(self):
        e = " ".join(repr(e) for e in self)
        return f"{self.cname}[{e}]"

    @property
    def short(self):
        n = self.lcname
        return f"{n} {getattr(self[1], n)}"


class Row(Box):
    pass


class Col(Box):
    pass


class Puzzle:
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
        self._history = list()
        self._context = dict()

    def context(self, thing, **kw):
        try:
            if thing in self._context:
                return self._context[thing]
        except TypeError:
            thing = id(thing)
        if thing not in self._context:
            for k,v in kw.items():
                if v in (set,dict,tuple,list):
                    kw[k] = v()
            self._context[thing] = dict(**kw)
        return self._context[thing]

    def clone(self):
        ret = self.__class__()
        for r in ROW_NUMBERS:
            for c in COLUMN_NUMBERS:
                e = self[r, c]
                if e.given:
                    ret[r, c].given = e.value
        return ret

    def reset(self):
        for e in self:
            e.reset()
        self._history = list()

    def describe_inference(self, desc):
        desc = desc.strip() + "\n"
        if desc not in self._history:
            self._history.append(desc)

    @property
    def history(self):
        return "".join(self._history)

    def __iter__(self):
        for row in self.rows:
            for e in row:
                yield e

    def __getitem__(self, idx):
        if isinstance(idx, (list, tuple)) and len(idx) == 2:
            return self.rows[idx[0]][idx[1]]
        try:
            idx = int(idx)
        except (ValueError,TypeError):
            pass
        if isinstance(idx, str):
            ret = set()
            for row in self.rows:
                ret = ret.union( row[idx] )
            return ret
        return self.rows[idx]

    def __setitem__(self, idx, val):
        if isinstance(idx, (list, tuple)) and len(idx) == 2:
            self.rows[idx[0]][idx[1]] = val
            return
        raise IndexError(f"grids require tuple indexes to set elements (given: {idx})")

    def __repr__(self):
        dat = [[x.as_cell for x in row] for row in self.rows]
        return tabulate(dat, tablefmt=sudoku_table_format, stralign=None)

    @property
    def box_rows(self):
        yield (self.boxes[1], self.boxes[2], self.boxes[3])
        yield (self.boxes[4], self.boxes[5], self.boxes[6])
        yield (self.boxes[7], self.boxes[8], self.boxes[9])

    @property
    def box_cols(self):
        yield (self.boxes[1], self.boxes[4], self.boxes[7])
        yield (self.boxes[2], self.boxes[5], self.boxes[8])
        yield (self.boxes[3], self.boxes[6], self.boxes[9])