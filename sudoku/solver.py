#!/usr/bin/env python
# coding: utf-8

import os
import re
import logging
import pkgutil
import importlib
import collections

import pluggy
import sudoku.rules

log = logging.getLogger(__name__)

NAMESPACES = ["sudoku.rules"]
INSTALLED_DIR = [os.path.dirname(__file__)]
KNOWN_OPTS = {"human", "test"}
# we don't actually use opts for anything (yet?)


def _process_opts(opts):
    if isinstance(opts, str):
        opts = opts.split()
    try:
        for item in opts:
            yield item
    except TypeError:
        pass


def process_opts(opts):
    return set(_process_opts(opts)).intersection(KNOWN_OPTS)


class RulesManager(pluggy.PluginManager):
    _loaded = collections.defaultdict(lambda: False)
    _local_modules = set()
    accept_filter = reject_filter = None

    @property
    def local_modules(self):
        yield from self._load_local_modules()

    @classmethod
    def _load_local_modules(cls):
        if cls._loaded:
            return cls._local_modules

        for namespace,base_dir in zip(NAMESPACES, INSTALLED_DIR):
            plugin_path = os.path.join(base_dir, *namespace.split(".")[1:])
            log.debug("loading %s.* from %s", namespace, plugin_path)
            for item in pkgutil.iter_modules([plugin_path], f"{namespace}."):
                if item.name == __name__:
                    continue  # pragma: no cover ; too rare to bother with
                log.debug("loading %s", item.name)
                m = importlib.import_module(item.name)
                cls._local_modules.add(m)

        cls._loaded = True
        return cls._local_modules

    def __init__(
        self,
        opts=None,
        accept_filter=os.environ.get("SUDOKU_RAFILTER", None),
        reject_filter=os.environ.get("SUDOKU_RRFILTER", None),
    ):
        super().__init__("sudoku")

        if accept_filter is not None:
            self.accept_filter = re.compile(accept_filter)

        if reject_filter is not None:
            self.reject_filter = re.compile(reject_filter)

        self.opts = process_opts(opts)
        if not self.opts:
            self.opts.add("human")

        log.debug("RulesManager.init [start]")

        self.add_hookspecs(sudoku.rules)
        for m in self.local_modules:
            m_name = self.get_canonical_name(m)
            if self.reject_filter is not None and self.reject_filter.search(m_name):
                log.debug(
                    "rejecting %s since it matched the curent reject_filter=%s",
                    m_name,
                    self.reject_filter.pattern,
                )
                self.set_blocked(m_name)
                continue
            if self.accept_filter is not None and not self.accept_filter.search(m_name):
                log.debug(
                    "rejecting %s since it did not match the curent accept_filter=%s",
                    m_name,
                    self.accept_filter.pattern,
                )
                self.set_blocked(m_name)
                continue
            log.debug("registering %s", m)
            self.unblock(m_name)
            self.register(m)
            log.debug("registered %s", m)

        # XXX: we shuld really auto-discover plugins… that's the point of pluggy…
        # log.debug("loading setuptools 'sudoku_plugins' entrypoints")
        # self.load_setuptools_entrypoints("sudoku_plugins")

        log.debug("RulesManager.init [end]")

        self.step_count = 0

    def step(self, puzzle):
        # We used to do this (how you're supposed to invoke pluggy hooks):
        #
        #     ret = sum(self.hook.main(puzzle=puzzle, opts=self.opts))
        #
        # ... but pluggy doesn't seem provide any pre/post opportunities to
        # check for puzzle breaks or anything useful like that. We instead
        # iterate over the hooks and check puzzle.broken and puzzle.check() for
        # each one.
        #
        # could maybe be done with add_hookcall_monitoring(), but this seems to
        # be for debug tracing.

        dc = 0
        for name, hook in self.list_name_plugin():
            if hook is None:
                continue
            try:
                dc += hook.main(puzzle=puzzle, opts=self.opts)
            except Exception as e:
                # NOTE: before you go trying to show the file and line-number
                # in this exception (again), stop. pluggy hides this and makes
                # it appear to be in solver.py between try and except 3-5 lines
                # up from here.
                #
                # … but you can import main from the dumb thing and run it on the puzzle
                #   from sudoku.rules.y_wing import main as y_wing_main
                #   y_wing_main(puzzle_in_question)
                puzzle.describe_inference(f"rules module {name} seems broken: {e}", __name__)
            if puzzle.broken:
                break
            elif not (cres := puzzle.check()):
                puzzle.describe_inference(f"puzzle broke during {name}:", __name__)
                for item in cres:
                    puzzle.describe_inference(f"[!]  {item}", __name__)
                break
        return dc

    def solve(self, puzzle, clone=True):
        if clone:
            puzzle = puzzle.clone()

        sv = puzzle.context(solve, sv=set)["sv"]
        if "init" not in sv:
            self.hook.init(puzzle=puzzle, opts=self.opts)
            sv.add('init')

        while self.step(puzzle) > 0:
            if puzzle.broken:
                break

        return puzzle


_manager = None


def get_manager(
    opts=None,
    accept_filter=os.environ.get("SUDOKU_RAFILTER", None),
    reject_filter=os.environ.get("SUDOKU_RRFILTER", None),
):
    return RulesManager(opts=opts, accept_filter=accept_filter, reject_filter=reject_filter)


Solver = Karen = get_manager


def solve(
    puzzle,
    opts=None,
    accept_filter=os.environ.get("SUDOKU_RAFILTER", None),
    reject_filter=os.environ.get("SUDOKU_RRFILTER", None),
    clone=True,
):
    """ instantiate a Solver and solve the given puzzle """
    return Karen(
        opts=opts, accept_filter=accept_filter, reject_filter=reject_filter
    ).solve(puzzle=puzzle, clone=clone)
