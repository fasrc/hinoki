#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from hinoki.skeleton import fib

__author__ = "Molly Duggan"
__copyright__ = "Molly Duggan"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
