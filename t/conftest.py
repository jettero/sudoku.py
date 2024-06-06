#!/usr/bin/env python
# coding: utf-8

import os
import glob
import logging
import pytest
import pstats
import subprocess
import itertools

from sudoku import Puzzle, get_puzzles, ROW_NUMBERS, solve
from sudoku.tools import PYTR
from sudoku import __file__ as __sfile__
import sudoku.solver

sudoku.solver.NAMESPACES.append('t.rules')
sudoku.solver.INSTALLED_DIR.append(os.path.dirname(__file__))

log = logging.getLogger(__name__)

tdir = os.path.dirname(__file__)
rdir = os.path.dirname(tdir)
adir = os.path.join(tdir, "asset")
odir = os.path.join(tdir, 'output')
sdir = os.path.dirname(__sfile__)

already_spammed = set()

def spam(name, puzzle):
    if name not in already_spammed:
        log.debug("%s:\n%s", name, puzzle)
        already_spammed.add(name)

PUZZLES = tuple(get_puzzles())
RULES = dict( (n.split('.')[-1],m.main) for n,m in sudoku.solver.Karen().list_name_plugin() )
RULE2 = tuple( f'{first}|{second}' for first,second in itertools.combinations(RULES, 2) )

@pytest.fixture(scope='function', params=tuple(f'p{i}' for i in range(len(PUZZLES))))
def any_p(request):
    p = PUZZLES[int(request.param[1:])]
    return p

@pytest.fixture(scope='session', params=tuple(RULE2))
def any_2rule(request):
    r1,r2 = request.param.split('|')
    return (RULES[r1], RULES[r2])

@pytest.fixture(scope="function")
def puzzles():
    yield PUZZLES

@pytest.fixture(scope="function")
def empty_puzzle():
    yield Puzzle()

@pytest.fixture(scope="function")
def diag_puzzle():
    p = Puzzle()
    for x in ROW_NUMBERS:
        p[x, x] = x
    yield p

def _wrap_in_bound_scope(p, name):
    def _bound_to_p():
        yield p
    _bound_to_p.__name__ = name
    return _bound_to_p

def _load_all_assets_as_fixtures(): # provides fixtures p_bp, p_45, p_srr, p_1t9m4 and p_empty via t/asset/*.txt
    short_name = PYTR(r"^p?_?(?P<short>.+?)\.txt$")
    for file in glob.glob(os.path.join(adir, "*.txt")):
        if short_name.search(os.path.basename(file)):
            short = "p_" + short_name[0]
            (p,) = get_puzzles(file=file)
            spam(short, p)
            globals()[short] = pytest.fixture(scope="function")(_wrap_in_bound_scope(p, short))
            log.info("loaded %s into fixture %s", file, short)

_load_all_assets_as_fixtures()

def _provide_each_puzzle_as_a_fixture():
    for n,p in enumerate(PUZZLES):
        name = f'p{n}'
        globals()[name] = pytest.fixture(scope='function')(_wrap_in_bound_scope(p, name))

_provide_each_puzzle_as_a_fixture()

@pytest.fixture(scope="function")
def q7(p7):
    return solve(p7)

@pytest.fixture(scope="function")
def p_45m(p_45):
    p = p_45.clone()

    p[2, 1].add_center_marks(4, 5)
    p[2, 3].add_center_marks(4, 5)

    p[4, 1].add_pencil_marks(5)
    p[4, 3].add_pencil_marks(5)

    p[6, 8].add_pencil_marks(4)
    p[6, 9].add_pencil_marks(4)

    p[7, 5].add_pencil_marks(4)
    p[8, 5].add_pencil_marks(4)
    p[9, 5].add_pencil_marks(4)

    p[7, 7].add_pencil_marks(5)

    spam("p_45m", p)

    yield p

##### profiling
prof_filenames = set()

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    if os.environ.get('TEST_PROFILE'):
        import cProfile
        filename, lineno, funcname = item.location # item.name is just the function name
        profile_name = filename.split('/')[-1][:-3]
        profile_name += '-' + funcname + '.pstats'
        prof_filename = os.path.join(odir, profile_name)
        prof_filenames.add(prof_filename)
        try:
            os.makedirs(odir)
        except OSError:
            pass
        prof = cProfile.Profile()
        prof.enable()

    yield

    if os.environ.get('TEST_PROFILE'):
        prof.dump_stats(prof_filename)
        prof_filenames.add(prof_filename)

def pytest_sessionfinish(session, exitstatus):
    if os.environ.get('TEST_PROFILE'):
        # shamelessly ripped from pytest-profiling — then modified to taste
        if prof_filenames:
            combined = None
            for pfname in prof_filenames:
                if not os.path.isfile(pfname):
                    continue
                if combined is None:
                    combined = pstats.Stats(pfname)
                else:
                    combined.add(pfname)

            if combined:
                cfilename = os.path.join(odir, 'combined.pstats')
                csvg      = os.path.join(odir, 'combined.svg')
                combined.dump_stats(cfilename)

                gp_cmd = [ 'gprof2dot', '-f', 'pstats', cfilename, '--path', sdir ]

                gp = subprocess.Popen(gp_cmd, stdout=subprocess.PIPE)
                dp = subprocess.Popen(['dot', '-Tsvg', '-o', csvg], stdin=gp.stdout)
                dp.communicate()
