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

print p._before_string
print p

s = sudoku.solver(p)
solved = 0
while not solved:
    s._loop_once()
    print p
    solved = 1

