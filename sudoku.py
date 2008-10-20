
class solver(object):
    """The solver is given a puzzle to work on, applying rules.
    """

class element(object):
    """This a single element in the puzzle.
       It has a value, but doesn't know anything about the Puzzle itself.
       It knows what values it *can* be based on rules and can report whether it's "solved."
    """
    def __init__(self, value):
        self.possibilities = range(1, 9)
        if value == 0:
            self.val = None
        else:
            self.val = value

    def __str__(self):
        if self.val is not None:
            return str(self.val)
        return "."

    def i_cannot_be(self, value):
        if self.val == value:
            raise Exception, "logical inconsistancy formed, i_cannot_be(%d), but i_am(%d)" % (value,value)

        if self.val is not None:
            return

        if value in self.possibilities:
            self.possibilities.remove(value)

        if len( self.possibilities ) == 1:
            self.i_am( self.possibilities[0] )

    def i_am(self, value):
        if self.val is None:
            return

        self.val = value
        self.possibilities = [value]

        for e in self.col + self.row + self.cel:
            if e is not self:
                e.i_cannot_be(value)

class puzzle(object):
    """This is the puzzle, it's 9x9 Elements.
       It understands rows, cols, and squares.
       Solvers can tell the rows, cols, and squares (sometimes excluding single elements): you can't be <blarg>.
    """
    def assign_cols(self):
        self.cols = []
        for j in range(9):
            col = [ row[j] for row in self.rows ]
            self.cols.append(col)
            for e in col:
                e.col = col

    def assign_cels(self):
        self.cels = [] # #python Crys_:
        for c in [(x, y) for y in range(3) for x in range(3)]:
            cel = [];
            self.cels.append(cel)

            for rn in range(3*c[0], 3*c[0]+3):
                this_row = self.rows[rn]
                for cn in range(3*c[1], 3*c[1]+3):
                    cel.append( this_row[cn] )

            for e in cel:
                e.cel = cel

    def i_am(self, knowns):
        for e in knowns:
            e.i_am(e.val);

    def __init__(self, rows):
        if type([]) != type(rows) or len(rows) != 9:
            raise TypeError, "puzzle(rows) takes 9 rows as an argument"

        self.rows = []
        knowns = []

        for row in rows:
            this_row = []
            self.rows.append(this_row)

            if type([]) != type(row) or len(row) != 9:
                raise TypeError, "puzzle(rows) takes 9 rows with 9 integers (or None) in each"

            for i in row:
                if i == 0 or (type(i)==type(3) and 0<i<10):
                    e = element(i)
                    this_row.append(e)
                    knowns.append(e)

                else:
                    raise TypeError, "every element in a puzzle row must be an integer (0-9) or None"

        for row in self.rows:
            for e in row:
                e.row = row

        self.assign_cols()
        self.assign_cels()
        self.i_am(knowns)

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

