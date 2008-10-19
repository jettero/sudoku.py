
class solver(object):
    """The solver is given a puzzle to work on, applying rules.
    """

class element(object):
    """This a single element in the puzzle.
       It has a value, but doesn't know anything about the Puzzle itself.
       It knows what values it *can* be based on rules and can report whether it's "solved."
    """

class puzzle(object):
    """This is the puzzle, it's 9x9 Elements.
       It understands rows, cols, and squares.
       Solvers can tell the rows, cols, and squares (sometimes excluding single elements): you can't be <blarg>.
    """

    def __init__(self, *rows):
        pass
