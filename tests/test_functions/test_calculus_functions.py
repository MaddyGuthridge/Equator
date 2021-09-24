"""Ensure that calculus functions work correctly
"""

import pytest

from ..helpers import doOneSolutionEq

from equator import EqFunctionArgumentException

def test_differentiate_contant():
    assert doOneSolutionEq("diff(42, x)") == ["0"]

def test_differentiate_simple():
    assert doOneSolutionEq("diff(2 * x^2 - 5 * x + 4, x)") == ["4*x - 5"]

def test_differentiate_complex():
    assert doOneSolutionEq("diff(sin(x) - cos(x)^2 + 2*ln(2 * x), x)") == ["?"]

def test_differentiate_other_symbols():
    assert doOneSolutionEq("diff(2 * x^2 - 5 * x + a, x)") == ["4*x - 5 + da/dx"]

def test_differentiate_invalid_symbol():
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionEq("diff(2 * x, 1)")

################################################################################

def test_integrate_constant():
    assert doOneSolutionEq("int(42, x)") == ["42 * x"]

def test_integrate_simple():
    assert doOneSolutionEq("int(2 * x - 5, x)") == ["x^2 - 5*x"]

def test_integrate_complex():
    assert doOneSolutionEq("int(sin(x) - cos(x)^2 + 2*ln(2 * x), x)") == ["?"]

def test_integrate_other_symbols():
    assert doOneSolutionEq("int(6 * x + a, x)") == ["?"]

def test_integrate_invalid_symbol():
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionEq("int(2 * x, 1)")

def test_integrate_range():
    assert doOneSolutionEq("int(42, x = 1, 5)") == ["210"] # ?

def test_integrate_invalid_range():
    # Is this even possible?
    ...
