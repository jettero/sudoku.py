def _xcomb(items, n):
    # stolen from http://code.activestate.com/recipes/190465/
    # does not produce lists with repeat elements (e.g. [1,1])
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

    def solve(self,pre_callback=None,post_callback=None):
        self._puzzle.log("solver starting")
        flux_score = self._puzzle.flux_score()
        last_score = 0
        while last_score != flux_score:
            last_score = flux_score

            if pre_callback:
                pre_callback(self._puzzle)

            self._loop_once()
            flux_score = self._puzzle.flux_score()

            if last_score != flux_score and post_callback:
                post_callback(self._puzzle)

    def _loop_once(self):
        self._puzzle.log("solver main-loop started")
        self._puzzle.indent()

        self.find_aligned_i_elements()
        self.find_n_bound_elements()

        self._puzzle.outdent()
        self._puzzle.log("solver main-loop ended")

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
                    same_col = reduce(lambda a,b: a and b, [first.col is e.col for e in can_be_i])
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
            self._puzzle.indent()
            for cell in self._puzzle.cels:
                for ee in _xcomb(filter(lambda x: x.val is None, cell), n):
                    ne = _not_in(ee, cell)

                    eep = set(reduce(lambda x,y: x+y, [e.possibilities for e in ee]))
                    nep = set(reduce(lambda x,y: x+y, [e.possibilities for e in ne]))

                    for ar in _xcomb(range(1, 9+1), n):
                        all_yes = True

                        for i in ar:
                            if i not in eep or i in nep:
                                all_yes = False
                                break;

                        if all_yes:
                            self._puzzle.log("found %d-bound elements around %s" % (n, str(ar)))
                            for i in _not_in(ar, range(1, 9+1)):
                                for e in ee:
                                    e.i_cannot_be(i);

            self._puzzle.outdent()
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
        # is simply a list of bound pairs co-incidentally, this will solve the
        # last puzzle
        pass
