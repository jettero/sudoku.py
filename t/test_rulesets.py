#!/usr/bin/env python
# coding: utf-8

import logging
from random import randint

log = logging.getLogger(__name__)

def rule_sort(x):
    return randint(1,100)

def do_one_loop(p, rules, immediate_check=True):
    dc = 123456789
    c = p.check()
    p = p.clone()
    while dc > 1:
        dc = 0
        for rule in sorted(rules, key=rule_sort):
            log.debug('running rule %s', rule)
            dc += rule(p)
            c = p.check()
            log.debug('    dc=%d, result=%s', dc, c)

            if immediate_check:
                assert bool(c)

            if not c:
                dc = 0
                break
    return c

def do_many_loops(p, rules, loops, immediate_check=True):
    fail = 0
    for l in range(loops):
        log.info('starting %s loop %s', rules, l)
        c = do_one_loop(p, rules)
        if immediate_check:
            assert bool(c)
        if not c:
            fail += 1
    return fail

def test_2rule(any_p, any_2rule):
    fail_count = do_many_loops(any_p, any_2rule, 5)
    assert fail_count == 0
