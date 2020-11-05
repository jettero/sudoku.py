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

    def solve(self, puzzle):
        while sum(self.hook.hidden(puzzle=puzzle)):
            pass

        while sum(self.hook.human(puzzle=puzzle)):
            pass


_manager = None


def get_manager():
    global _manager
    if _manager is None:
        _manager = RulesManager()
    return _manager


Karen = get_manager

def solve(puzzle):
    Karen().solve(puzzle=puzzle)
