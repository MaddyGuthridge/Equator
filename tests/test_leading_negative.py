"""Test for ensuring that leading negatives are interpreted correctly

Author: Miguel Guthridge (hdsq@outlook.com.au)
"""

from .helpers import simplifyExp, simplifyEq

from ..lib.smart_equate import equate

def test_starting_negative():
    assert equate("-1") == ["-1"]

def test_mul_div():
    assert equate("4 * -1") == ["-4"]
    assert equate("4/-2") == ["-2"]

def test_neg_to_power():
    assert simplifyExp(equate("-2^2 *-4^-3")) == ["1/16"]
    assert equate("-2^2") == ["-4"]

def test_to_neg_power():
    assert simplifyExp(equate("4^-1")) == ["1/4"]
    assert simplifyExp(equate("2^-3/2")) == ["1/16"]

def test_equality():
    assert simplifyEq(equate("-1 = -x")) == [{"x": "1"}]
    assert simplifyEq(equate("x = -2 * -3")) == [{"x": "6"}]
