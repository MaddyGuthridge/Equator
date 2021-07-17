"""Test that symbols are operated on correctly, and can be simplified
"""

from .helpers import doOneSolutionExp

def test_square_symbol():
    """Make sure that squaring a symbol doesn't make it die
    """
    assert doOneSolutionExp("x^2") == ["x^2"]
