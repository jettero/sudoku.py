
class solver(object):
    """The solver is given a puzzle to work on, applying rules.
    """

    def __init__(self, puzzle):
        self.puzzle = puzzle

    def _loop_once(self):
        self.find_aligned_pairs()

    def find_aligned_pairs(self):
        """ Find elements in which i occur such that they are the ony two
            elements where i can occur and they're in the same row or column.
            This eliminates their changes of being elsewhere in the row or
            column.

            (This could be generalized to any two *or* three elements easily.)
        """

        for cell in self.puzzle.cels:
            for i in range(1, 9+1):
                can_be_i = []

                for e in cell:
                    if i in e.possibilities:
                        can_be_i.append(e)

                if len(can_be_i) > 1:
                    first = can_be_i.pop()
                    same_row = reduce(lambda a,b: a and b, [first.row is e.row for e in can_be_i])
                    same_col = reduce(lambda a,b: a and b, [first.col is e.row for e in can_be_i])
                    can_be_i.append(first)

                    if same_row:
                        for e in can_be_i:
                            self.puzzle.log("found %d isolated in a single row %s" % (i, repr(e._loc)))
                        for e in first.row:
                            if e not in can_be_i:
                                e.i_cannot_be(i)

                    if same_col:
                        for e in can_be_i:
                            self.puzzle.log("found %d isolated in a single col %s" % (i, repr(e._loc)))
                        for e in first.col:
                            if e not in can_be_i:
                                e.i_cannot_be(i)

    def find_bound_double_pairs(self):
        """ Find pair of elements where i and j may occur such that i and j
            must occur only in those two elements.  This eliminates the two
            elements chance of being anything but i or j.
        """
        for cell in self.puzzle.cels:
            for i in range(1, 9+1):
                for j in range(1, 9+1):
                    for e in cell:
                        for f in cell:
                            if e is not f:
                                # wow, this deep? really?
