#!/usr/bin/env python
# coding: utf-8

EV = R19 = BOX_NUMBERS = ROW_NUMBERS = COLUMN_NUMBERS = ELEMENT_VALUES = tuple(
    range(1, 9 + 1)
)

BOX_MATRIX = (
    (1, 1, 1, 2, 2, 2, 3, 3, 3),
    (1, 1, 1, 2, 2, 2, 3, 3, 3),
    (1, 1, 1, 2, 2, 2, 3, 3, 3),
    (4, 4, 4, 5, 5, 5, 6, 6, 6),
    (4, 4, 4, 5, 5, 5, 6, 6, 6),
    (4, 4, 4, 5, 5, 5, 6, 6, 6),
    (7, 7, 7, 8, 8, 8, 9, 9, 9),
    (7, 7, 7, 8, 8, 8, 9, 9, 9),
    (7, 7, 7, 8, 8, 8, 9, 9, 9),
)

SEV = set(EV)
