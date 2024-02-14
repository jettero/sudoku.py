# What is this?

I started getting interested in the precise mechanics of Sudoku... I would say
the "math," but I don't really understand that, not really. But I wanted to
formalize the rules I was using in my head, so I wrote this.

This package is really meant only for me to use and usually just in the ipython
shell.

1. `pip install -U pip -r ipy-requirements.txt`
2. ipython
3. ???
4. profit

# What's next?

## rules ideas
I'm not really happy with the current ruleset or especially the way the markings
are computed and used in those rules.  I have a new system in mind for that. 

## generation ideas
I'd also like to try my hand at puzzle generation. If I can get the solver to do
all the things I know how to do to solve these... reliably... I could perhaps
design an evaluator thingy that could test computer generated puzzles for things
like "fun" and "complexity" (in the sense of a human solving them).
