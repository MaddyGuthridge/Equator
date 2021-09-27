"""Check trig functions work correctly
"""

import pytest

from ..helpers import doOneSolutionExp

from equator import EqFunctionArgumentException

def test_lcm_simple():
    assert doOneSolutionExp("lcm(2, 3)") == ["6"]

def test_lcm_symbol():
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionExp("lcm(x, 1)")
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionExp("lcm(1, x)")
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionExp("lcm(x, y)")

def test_lcm_decimal():
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionExp("lcm(1.5, 2)")

def test_gcd_simple():
    assert doOneSolutionExp("gcd(8, 12)") == ["4"]
    assert doOneSolutionExp("gcd(48, 18)") == ["6"]

def test_gcd_symbol():
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionExp("gcd(x, 1)")
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionExp("gcd(1, x)")
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionExp("gcd(x, y)")

def test_gcd_decimal():
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionExp("gcd(1.5, 2)")

def test_gcd_zero():
    assert doOneSolutionExp("gcd(183, 0)") == ["183"]
