#!/usr/bin/env python

# -- coding: utf-8 --
# @Time : 2024/1/5 13:59
# @Author : Genesis Ai
# @File : test_func.py

import pytest

def add(x,y):
    return  x+y
@pytest.mark.parametrize(
    "x,y,expected",
    [
        (1,1,2),
        (2,2,4),
        (10,10,20),
    ]
)
def test_add(x,y,expected):
    assert add(x,y) == expected