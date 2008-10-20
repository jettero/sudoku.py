
class solver(object):
    """The solver is given a puzzle to work on, applying rules.
    """

class element(object):
    """This a single element in the puzzle.
       It has a value, but doesn't know anything about the Puzzle itself.
       It knows what values it *can* be based on rules and can report whether it's "solved."
    """
    def __init__(self, value):
        if value == 0:
            self.val = None
        else:
            self.val = value

    def __str__(self):
        if self.val is not None:
            return str(self.val)
        return "."

class puzzle(object):
    """This is the puzzle, it's 9x9 Elements.
       It understands rows, cols, and squares.
       Solvers can tell the rows, cols, and squares (sometimes excluding single elements): you can't be <blarg>.
    """

    def __init__(self, rows):
        self.rows = []

        if type([]) != type(rows) or len(rows) != 9:
            raise TypeError, "puzzle(rows) takes 9 rows as an argument"

        for row in rows:
            this_row = []
            self.rows.append(this_row)

            if type([]) != type(row) or len(row) != 9:
                raise TypeError, "puzzle(rows) takes 9 rows with 9 integers (or None) in each"

            for i in row:
                if i == 0 or (type(i)==type(3) and 0<i<10):
                    this_row.append(element(i))

                else:
                    raise TypeError, "every element in a puzzle row must be an integer (0-9) or None"

        for row in self.rows:
            for e in row:
                e.row = row

        self.cols = []
        for j in range(9):
            col = [ row[j] for row in self.rows ]
            self.cols.append(col)
            for e in col:
                e.col = col

        self.cels = [] # #python Crys_:
        for c in [(x, y) for y in range(3) for x in range(3)]:
            this_cell = [];
            self.cels.append(this_cell)

            for rn in range(3*c[0], 3*c[0]+3):
                this_row = self.rows[rn]
                for cn in range(3*c[1], 3*c[1]+3):
                    this_cell.append( this_row[cn] )

    def __str__(self):
        ret = ""
        for i, row in enumerate(self.rows):
            for j, element in enumerate(row):
                ret += "%s " % element
                if j % 3 == 2:
                    ret += " "
            ret += "\n";
            if i % 3 == 2:
                ret += "\n"
        return ret
