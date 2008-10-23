
class element(object):
    """This a single element in the puzzle.
       It has a value, but doesn't know anything about the Puzzle itself.
       It knows what values it *can* be based on rules and can report whether it's "solved."
    """
    def __init__(self, value, caller, loc):
        self._puzzle = caller
        self._loc = loc

        if value == 0:
            self.val = None
            self.possibilities = range(1, 9+1)
        else:
            self.val = value
            self.possibilities = [value]

    def __str__(self):
        if self.val is not None:
            return str(self.val)
        return "."

    def i_cannot_be(self, value):
        if self.val == value:
            txt = "logical inconsistancy formed, %s.i_cannot_be(%d), but %s.val==%d, previous puzzle state:\n%s" % \
              (repr(self._loc),value, repr(self._loc),self.val, str(self._puzzle))
            self._puzzle.log("Exception: %s" % txt)
            raise Exception, txt

        if self.val is not None:
            return

        if value in self.possibilities:
            self.possibilities.remove(value)
            self._puzzle.log("i_cannot_be(%d)" % value, self._loc)

        if len( self.possibilities ) == 1:
            self._puzzle.log("only one possibility left: %d" % self.possibilities[0], self._loc)
            self._puzzle.indent()
            self.i_am( self.possibilities[0] )
            self._puzzle.outdent()

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

