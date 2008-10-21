import re,time,os,sys

sys.tracebacklimit = 5
sys.recursionlimit = 10000

class solver(object):
    """The solver is given a puzzle to work on, applying rules.
    """

    def __init__(self, puzzle):
        self.puzzle = puzzle

    def _loop_once(self):
        self.find_aligned_pairs()

class element(object):
    """This a single element in the puzzle.
       It has a value, but doesn't know anything about the Puzzle itself.
       It knows what values it *can* be based on rules and can report whether it's "solved."
    """
    def __init__(self, value, caller, loc):
        self.possibilities = range(1, 9)
        self._puzzle = caller
        self._loc = loc

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

        self._puzzle.log("i_cannot_be(%d)" % value, self._loc);

        if value in self.possibilities:
            self.possibilities.remove(value)

      # if len( self.possibilities ) == 1:
      #     self._puzzle.log("only one possibility left: %d" % self.possibilities[0], self._loc);
      #     self._puzzle.indent()
      #     self.i_am( self.possibilities[0] )
      #     self._puzzle.outdent()

    def i_am(self, value):
        if not (type(value)==type(3) and 0<value<10):
            raise TypeError, "i_am() values must be integers, 1-9, received: " + repr(value)

        self.val = value
        self.possibilities = [value]
        self._puzzle.knowns.append(self)

        self._puzzle.log("i_am(%d)" % value, self._loc)
        for e in self.col + self.row + self.cel:
            if e is not self:
                self._puzzle.indent()
                e.i_cannot_be(value)
                self._puzzle.outdent()

class puzzle(object):
    """This is the puzzle, it's 9x9 Elements.
       It understands rows, cols, and squares.
       Solvers can tell the rows, cols, and squares (sometimes excluding single elements): you can't be <blarg>.
    """

    def __init__(self, rows):
        if type([]) != type(rows) or len(rows) != 9:
            raise TypeError, "puzzle(rows) takes 9 rows as an argument"

        if os.getenv("DEBUG"):
            self.debugging = True

        self.rows = []
        knowns = []

        self.log("starting puzzle")
        self.indent()
        self.log("populating rows")

        for ypos, row in enumerate(rows):
            this_row = []
            self.rows.append(this_row)

            if type([]) != type(row) or len(row) != 9:
                raise TypeError, "puzzle(rows) takes 9 rows with 9 integers (or None) in each"

            for xpos, i in enumerate(row):
                if i == 0 or (type(i)==type(3) and 0<i<10):
                    e = element(i, self, (xpos,ypos))
                    this_row.append(e)
                    if i>0:
                        knowns.append(e)

                else:
                    raise TypeError, "every element in a puzzle row must be an integer (0-9) or None"

        for row in self.rows:
            for e in row:
                e.row = row

        self.log("populating cols")
        self.assign_cols()

        self.log("populating cels")
        self.assign_cels()

        self.log("telling initial knowns: i_am() (known elements: %d)" % len(knowns))
        self.i_am(knowns)

        self.outdent()
        self.log("done building puzzle (known elements: %d)" % len(knowns))

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
        self.indent()
        self.knowns = []
        self.indent()
        for e in knowns:
            e.i_am(e.val); # this fills in knowns for us
        self.outdent()

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

    def indent(self,i=1):
        if not hasattr(self, '_indstr'):
            self._indstr = ""
        self._indstr += "  " * i

    def outdent(self,i=1):
        if not hasattr(self, '_indstr'):
            self._indstr = ""
        if i>0:
            self._indstr = self._indstr[0:-i*2]

    def log(self,msg,*id):
        if hasattr(self, 'debugging'):
            if not hasattr(self, '_indstr'):
                self._indstr = ""

            if hasattr(self, 'prev'):
                logfile = open("debug.log", "a")
            else:
                logfile = open("debug.log", "w")
                self.prev = 1

            logfile.write( time.ctime() + " [" + str(os.getpid()) + "]: " + self._indstr )

            for i in id:
                logfile.write( "<" + str(i) + "> " )

            logfile.write( re.sub("[\r\n]", "", msg) )
            logfile.write( "\n" )

            logfile.close()
