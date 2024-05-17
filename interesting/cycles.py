
from itertools import combinations
from sudoku.const import LongJump

def cycles(puzzle, N=3, C=(2,2)):
    binners = set(x for x in puzzle if not x.value and C[0] <= len(x.center) <= C[1])
    already = set()
    for item in binners:
        cycle = [ item ]
        remaining = binners - set(cycle)
        while remaining:
            try:
                for item in remaining:
                    if item not in cycle and (cycle[0].row == item.row or cycle[0].col == item.col or cycle[0].box == item.box) and cycle[0].center & item.center:
                        cycle.insert(0, item)
                        remaining.remove(item)
                        raise LongJump()
                    if item not in cycle and (cycle[-1].row == item.row or cycle[-1].col == item.col or cycle[-1].box == item.box) and cycle[-1].center & item.center:
                        cycle.append(item)
                        remaining.remove(item)
                        raise LongJump()
            except LongJump:
                continue
            break
        if len(cycle) >= N:
            k = (cycle[0], cycle[-1])
            if k not in already and k[0].center & k[-1].center:
                already.add(k)
                yield cycle
