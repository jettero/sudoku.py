# stolen from http://code.activestate.com/recipes/190465/
# does not produce lists with repeat elements (e.g. [1,1])
def _xcomb(items, n):
    if n==0:
        yield []

    else:
        for i in xrange(len(items)):
            for cc in _xcomb(items[i+1:], n-1):
                yield [items[i]] + cc

def _not_in(to_exclude, complete_set):
    nots = []
    for r in complete_set:
        if r not in to_exclude:
            nots.append(r)
    return nots


class solver(object):
    """The solver is given a puzzle to work on, applying rules.
    """

    def __init__(self, puzzle):
        self._puzzle = puzzle

    def _loop_once(self):
        self.find_aligned_i_elements()
        self.find_n_bound_elements()

    def find_aligned_i_elements(self):
        """ Find elements in which some number (i) can only occure in that row
            or in that column.  This eliminates their changes of being
            elsewhere in the row or column.
        """

        self._puzzle.log("looking for aligned i elements")
        self._puzzle.indent()
        for cell in self._puzzle.cels:
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
                            self._puzzle.log("found %d isolated in a single row %s" % (i, repr(e._loc)))
                        for e in first.row:
                            if e not in can_be_i:
                                e.i_cannot_be(i)

                    if same_col:
                        for e in can_be_i:
                            self._puzzle.log("found %d isolated in a single col %s" % (i, repr(e._loc)))
                        for e in first.col:
                            if e not in can_be_i:
                                e.i_cannot_be(i)
        self._puzzle.outdent()

    def find_n_bound_elements(self):
        """ Find some number (n) of bound elements where some
            combination of numbers (ar) of length (n) can only
            occur within those elements.  This eliminates the
            possibility of their being any number besides those
            in (ar).

        """

        self._save_for_double_bound_2_element_sets = []
        self._puzzle.log("looking n-bound elements")
        self._puzzle.indent()
        for n in range(1, 3+1):
            self._puzzle.log("looking %d-bound elements" % n)
            for cell in self._puzzle.cels:
                for ee in _xcomb(cell, n):
                    ne = _not_in(ee, cell)

                    self._puzzle.indent()
                    for i,l in enumerate([e._loc for e in ee]):
                        self._puzzle.log("ee[%d]=%s" % (i,l))
                    self._puzzle.outdent()

                    for ar in _xcomb([range(1, 9+1)], n):
                        all_yes = True

                        for i in ar:
                            if i not in ee or i in ne:
                                all_yes = False
                                break;

                        if all_yes:
                            self._puzzle.log("found %-bound elements around %s" % (n, str(ar)))
                            for i in _not_in(ar, range(1, 9+1)):
                                for e in ee:
                                    e.i_cannot_be(i);
        self._puzzle.outdent()

    def find_double_bound_2_element_sets(self):
        """ If we can find two sets of two double bound elements
            in neighboring cells:  They can, if both elements of
            both sets of the double bound pairs are in the same
            rows (or columns) of the adjacent cells, elminate
            those rows (or columns) for those numbers from the
            third cell in the cell-row (or cell-column).
        """

        # we should use the pairs found in self._save_for_double_... blah which
        # is simply a list of bound pairs
        pass
