#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from seproject_group18.skeleton import fib

__author__ = "naitao"
__copyright__ = "naitao"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
