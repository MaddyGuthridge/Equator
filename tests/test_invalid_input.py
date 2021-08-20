"""Ensure that invalid input is detected correctly
"""

import pytest

from ..lib.eq_except import *

from .helpers import equate

def test_bad_symbols_dot():
    with pytest.raises(EqTokeniseException):
        equate("ev.di")

def test_bad_symbols_leading_number():
    with pytest.raises(EqTokeniseException):
        equate("12vjr")

def test_bad_exponent_notation_space():
    with pytest.raises(EqTokeniseException):
        equate("1e + 4")
    with pytest.raises(EqTokeniseException):
        equate("1 e4")

def test_bad_exponent_notation_bad_exp():
    with pytest.raises(EqTokeniseException):
        equate("1e3.5")

def test_bad_symbols_after_semicolon():
    with pytest.raises(EqTokeniseException):
        equate("1 + 1; 1r5i")
