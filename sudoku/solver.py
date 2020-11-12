#!/usr/bin/env python
# coding: utf-8

import os
import logging
import pkgutil
import importlib

import pluggy
import sudoku.rules

log = logging.getLogger(__name__)

NAMESPACES = ("sudoku.rules",)
INSTALLED_DIR = os.path.dirname(__file__)

class RulesManager(pluggy.PluginManager):
    _local_modules = set()

    @property
    def local_modules(self):
        yield from self._local_modules if self._local_modules else self._load_local_modules()

    @classmethod
    def _load_local_modules(cls):
        if cls._local_modules:
            return cls._local_modules

        for namespace in NAMESPACES:
            plugin_path = os.path.join(INSTALLED_DIR, *namespace.split(".")[1:])
            log.debug("loading %s.* from %s", namespace, plugin_path)
            for item in pkgutil.iter_modules([plugin_path], f"{namespace}."):
                if item.name == __name__:
                    continue
                log.debug("loading %s", item.name)
                m = importlib.import_module(item.name)
                cls._local_modules.add(m)

        return cls._local_modules

    def __init__(self):
        super().__init__("sudoku")

        log.debug("RulesManager.init [start]")

        self.add_hookspecs(sudoku.rules)
        for m in self.local_modules:
            log.debug("registering %s", m)
            self.register(m)
            log.debug("registered %s", m)

        # log.debug("loading setuptools 'sudoku_plugins' entrypoints")
        # self.load_setuptools_entrypoints("sudoku_plugins")

        log.debug("RulesManager.init [end]")

        self.step_count = 0

    def step(self, puzzle):
        if self.step_count > 0:
            puzzle.describe_inference(f'step {self.step_count}')
        return sum(self.hook.hidden(puzzle=puzzle)) + sum(self.hook.human(puzzle=puzzle))

    def solve(self, puzzle):
        puzzle = puzzle.clone()

        self.step_count = 1
        while self.step(puzzle):
            self.step_count += 1

        puzzle.describe_inference(f'FIN')
        self.step_count = 0

        return puzzle


_manager = None


def get_manager():
    global _manager
    if _manager is None:
        _manager = RulesManager()
    return _manager


Solver = Karen = get_manager

def solve(puzzle):
    """ instantiate a Solver and solve the given puzzle """
    return Karen().solve(puzzle=puzzle)
