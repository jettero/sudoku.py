import re,time,os

from element import element

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
        self.knowns = []
        self.givens = []

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
                        self.givens.append(e)

                else:
                    raise TypeError, "every element in a puzzle row must be an integer (0-9) or None"

        for row in self.rows:
            for e in row:
                e.row = row

        self.log("populating cols")
        self.assign_cols()

        self.log("populating cels")
        self.assign_cels()

        self._before_string = str(self) # after the line below, the puzzle starts solving itself

        self.log("telling initial knowns: i_am()")
        self.i_am()
        self.outdent()
        self.log("done building puzzle")

    def assign_cols(self):
        self.cols = []
        for j in range(9):
            col = [ row[j] for row in self.rows ]
            self.cols.append(col)
            for e in col:
                e.col = col

    def assign_cels(self):
        self.cels = []
        self.celcols = [[],[],[]] # columns of cells
        self.celrows = [[],[],[]] # rows of cells

        for c in [(x, y) for y in range(3) for x in range(3)]: # <-- #python Crys_ showed me how to do this
            cel = [];
            self.cels.append(cel)
            self.celcols[c[1]].append(cel)
            self.celrows[c[0]].append(cel)

            for rn in range(3*c[0], 3*c[0]+3):
                this_row = self.rows[rn]
                for cn in range(3*c[1], 3*c[1]+3):
                    cel.append( this_row[cn] )

            for e in cel:
                e.cel = cel

    def i_am(self):
        self.indent()
        for e in self.givens:
            e.i_am(e.val); # this fills in knowns for us
        self.outdent()

    def flux_score(self):
        poss_score = 0
        for i, row in enumerate(self.rows):
            for j, element in enumerate(row):
                poss_score += len(element.possibilities)
        return poss_score - len(self.knowns)

    def __str__(self):
        ret = "- - -  " * 3 + "\n"

        for i, row in enumerate(self.rows):
            for j, element in enumerate(row):
                ret += "%s " % element
                if j % 3 == 2:
                    ret += " "
            ret += "\n";
            if i % 3 == 2:
                if i!=8:
                    ret += "\n"

        return ret + " flux_score: %d" % self.flux_score() + "\n"

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
    
    ### debugging queries
    def psb(self, *loc):
        if len(loc) != 2 and 0<=loc[0]<=8 and 0<=loc[1]<=8:
            raise TypeError, "psb takes a location as two x,y arguments"

        e = self.rows[loc[1]][loc[0]]
        if e.val is not None:
            return self.val
        return e.possibilities
