"""Ensure that order of operations are interpreted correctly

Author: Miguel Guthridge (hdsq@outlook.com.au)
"""

from .helpers import doOneSolutionExp

def test_operations_add_subtract_multiply_divide():
    assert doOneSolutionExp("1 + 1 * 2") == ["3"]
    assert doOneSolutionExp("1 - 3 * 2") == ["-5"]
    assert doOneSolutionExp("1 + 6 / 2") == ["4"]
    assert doOneSolutionExp("8 - 4 / 2") == ["6"]
    assert doOneSolutionExp("2 + 3*5 + 6") == ["23"]

def test_operations_power():
    assert doOneSolutionExp("2 + 2^2") == ["6"]
    assert doOneSolutionExp("2 * 2^2") == ["8"]
    assert doOneSolutionExp("2^3^2") == ["64"]

def test_brackets():
    assert doOneSolutionExp("(2 + 1) / 3") == ["1"]
    assert doOneSolutionExp("2^(1+1)") == ["4"]
    assert doOneSolutionExp("2^(3^2)") == ["512"]
    assert doOneSolutionExp("-(2 + 9)") == ["-11"]

def test_exponent_operations():
    assert doOneSolutionExp("1E+1 + 2") == ["12"]
    assert doOneSolutionExp("1.25E1 - 0.5") == ["12"]
