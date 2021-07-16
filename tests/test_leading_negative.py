"""Test for ensuring that leading negatives are interpreted correctly

Author: Miguel Guthridge (hdsq@outlook.com.au)
"""

from .helpers import doOneSolutionExp, doOneSolutionEq

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
