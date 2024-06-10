"""Test for ensuring that leading negatives are interpreted correctly

Author: Maddy Guthridge (hdsq@outlook.com.au)
"""
import pytest
from .helpers import doOneSolutionExp, doOneSolutionEq, equate
from equator import EqParserException

def test_starting_negative():
    assert doOneSolutionExp("-1") == ["-1"]

def test_mul_div():
    assert doOneSolutionExp("4 * -1") == ["-4"]
    assert doOneSolutionExp("4/-2") == ["-2"]

def test_neg_to_power():
    assert doOneSolutionExp("-2^2 *-4^-3") == ["1/16"]
    assert doOneSolutionExp("-2^2") == ["-4"]

def test_to_neg_power():
    assert doOneSolutionExp("4^-1") == ["1/4"]
    assert doOneSolutionExp("2^-3/2") == ["1/16"]

def test_equality():
    assert doOneSolutionEq("-1 = -x") == ["x=1"]
    assert doOneSolutionEq("x = -2 * -3") == ["x=6"]

def test_equation_second_parse():
    assert doOneSolutionEq("0 = a + b + 2") == ["a=-b-2"]

def test_invalid_no_following():
    with pytest.raises(EqParserException):
        assert equate("2 * -")
