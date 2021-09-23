"""Ensure that series functions (sum, mul) work correctly
"""

import pytest

from ..helpers import doOneSolutionExp

from equator import EqFunctionArgumentException

def test_sum_simple():
    doOneSolutionExp("sum(n = 1, 4, n)") == ["10"]
    doOneSolutionExp("sum(x = -5, 5, n * 5)") == ["0"]

def test_sum_constant():
    doOneSolutionExp("sum(n = 1, 5, 1)") == ["5"]
    
def test_sum_with_symbols():
    doOneSolutionExp("sum(n = 1, 5, n * x)") == ["15 * x"]
    doOneSolutionExp("sum(x = -5, 5, n * 5)") == ["55 * n"]

def test_sum_complex():
    doOneSolutionExp("sum(n = -10, 5, 2 * (n * 4)^3)") == ["-358400"]

def test_mul_simple():
    doOneSolutionExp("mul(n = 1, 5, n)") == ["120"]
    doOneSolutionExp("mul(n = -5, 5, n)") == ["0"]

def test_mul_constant():
    doOneSolutionExp("mul(n = 1, 5, 2)") == ["32"]

def test_mul_with_symbols():
    doOneSolutionExp("mul(n = 1, 5, n * x)") == ["120 * x ^ 5"]
    doOneSolutionExp("mul(x = -5, 5, n * 5)") == ["48828125 * n ^ 11"]

def test_mul_complex():
    doOneSolutionExp("mul(n = 1, 3, 2 * (n * 4)^3)") == ["452984832"]

def test_series_invalid_range():
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionExp("sum(n = 5, 1, n)")
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionExp("mul(n = 62, 37, n + 1)")
