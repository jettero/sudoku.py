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
        # this doesn't give me pre/post functions for each hook
        # in any way I can actually figure out:
        #
        # ret = sum(self.hook.main(puzzle=puzzle, opts=self.opts))
        #
        # So, ima just do it myself:

        dc = 0
        for name, hook in self.list_name_plugin():
            try:
                dc += hook.main(puzzle=puzzle, opts=self.opts)
            except Exception as e:
                puzzle.describe_inference(f"rules module {__name__} seems broken: {e}", __name__)
            if puzzle.broken:
                break
            elif not (cres := puzzle.check()):
                puzzle.describe_inference(f"puzzle broke during {name}:", __name__)
                for item in cres:
                    puzzle.describe_inference(f"[!]  {item}", __name__)
                break
        return dc

    def solve(self, puzzle):
        puzzle = puzzle.clone()

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
):
    """ instantiate a Solver and solve the given puzzle """
    return Karen(
        opts=opts, accept_filter=accept_filter, reject_filter=reject_filter
    ).solve(puzzle=puzzle)
