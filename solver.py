
class solver(object):
    """The solver is given a puzzle to work on, applying rules.
    """

    def __init__(self, puzzle):
        self.puzzle = puzzle

    def _loop_once(self):
        self.find_aligned_pairs()

    def find_aligned_pairs(self):
        for cell in self.puzzle.cels:
            for i in range(1, 9+1):
                can_be_i = []

                for e in cell:
                    if i in e.possibilities:
                        can_be_i.append(e)

                if len(can_be_i) == 2:

                    if can_be_i[0].col is can_be_i[1].col:
                        for e in can_be_i[0].col:
                            if e is not can_be_i[0] and e is not can_be_i[1]:
                                e.i_cannot_be(i)

                    if can_be_i[0].row is can_be_i[1].row:
                        for e in can_be_i[0].row:
                            if e is not can_be_i[0] and e is not can_be_i[1]:
                                e.i_cannot_be(i)
