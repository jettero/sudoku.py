#!/usr/bin/env python

import sudoku;

p = sudoku.puzzle([
    [ 2,1,0, 6,0,0, 0,0,0 ],
    [ 0,0,0, 0,0,5, 4,0,0 ],
    [ 0,0,8, 0,0,0, 0,3,0 ],

    [ 9,0,3, 0,2,0, 0,6,0 ],
    [ 0,0,0, 0,0,0, 0,0,0 ],
    [ 0,7,0, 0,1,0, 5,0,4 ],

    [ 0,5,0, 0,0,0, 2,0,0 ],
    [ 0,0,6, 8,0,0, 0,0,0 ],
    [ 0,0,0, 0,0,4, 0,9,7 ],
]);

# s = sudoku.solver(p)
# s._loop_once()

x=1
while x == 1:
    x=0

    for row in p.rows:
        for e in row:
            if e.val is None and len(e.possibilities) == 1:
                e.i_am(e.possibilities[0])
                x=1

print p
