"""Test that symbols are operated on correctly, and can be simplified
"""

from .helpers import doOneSolutionExp

def test_square_symbol():
    """Make sure that squaring a symbol doesn't make it die
    """
    assert doOneSolutionExp("x^2") == ["x^2"]

def test_function_symbol():
    """Make sure that symbols can be used in functions without dying
    """
    assert doOneSolutionExp("sqrt(x)") == ["sqrt(x)"]
    assert doOneSolutionExp("cos(x)") == ["cos(x)"]
