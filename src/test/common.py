#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from operator import attrgetter
from mmCif import Category, Item, SaveFrame


# Sorts in place
def ssort(l):
    if isinstance(l, list):
        if len(l) and isinstance(l[0], (Category, Item, SaveFrame)):
            l.sort(key=attrgetter("id"))
        else:
            l.sort()


def assert_equal(l1, l2, msg):
    ssort(l1)
    ssort(l2)

    t = unittest.TestCase("__str__")
    return t.assertEqual(l1, l2, msg)
