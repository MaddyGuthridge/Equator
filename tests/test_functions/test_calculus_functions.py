"""Ensure that calculus functions work correctly
"""

import pytest

from ..helpers import doOneSolutionExp

from equator import EqFunctionArgumentException

def test_differentiate_contant():
    assert doOneSolutionExp("diff(42, x)") == ["0"]

def test_differentiate_simple():
    assert doOneSolutionExp("diff(2 * x^2 - 5 * x + 4, x)") == ["4*x-5"]

def test_differentiate_complex():
    assert doOneSolutionExp("diff(sin(x) - cos(x)^2 + 2*ln(2 * x), x)") == ["(sin(2*x)+cos(x))+2/x"]

def test_differentiate_other_symbols():
    assert doOneSolutionExp("diff(2 * x^2 - 5 * x + a, x)") == ["4*x-5"]

def test_differentiate_invalid_symbol():
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionExp("diff(2 * x, 1)")

################################################################################

def test_integrate_constant():
    assert doOneSolutionExp("int(42, x)") == ["42*x"]

def test_integrate_simple():
    assert doOneSolutionExp("int(2 * x - 5, x)") == ["x*(x-5)"]

def test_integrate_complex():
    assert doOneSolutionExp("int(sin(x) - cos(x) + 2*ln(2 * x), x)")\
        == ["(((2*x)*log(x)-2*x)+x*log(4))-sqrt(2)*sin(x+pi/4)"]

def test_integrate_square_of_trig():
    assert doOneSolutionExp("int(cos(x)^2, x)") == ["x/2+sin(2*x)/4"]

def test_integrate_other_symbols():
    assert doOneSolutionExp("int(6 * x + a, x)") == ["x*(a+3*x)"]

def test_integrate_invalid_symbol():
    with pytest.raises(EqFunctionArgumentException):
        doOneSolutionExp("int(2 * x, 1)")

def test_integrate_range():
    assert doOneSolutionExp("int(42, x = 1..5)") == ["168"] # ?

def test_integrate_reverse_range():
    assert doOneSolutionExp("int(42, x = 5..1)") == ["-168"]

#def test_integrate_invalid_range():
#    # Is this even possible?
#    ...
