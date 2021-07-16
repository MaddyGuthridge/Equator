"""Ensure that the most basic of the basic features work

Author: Miguel Guthridge (hdsq@outlook.com.au)
"""

from .helpers import doOneSolutionExp, doOneSolutionEq

def test_constant():
    """Ensure constants work
    """
    assert doOneSolutionExp("1") == ["1"]
    assert doOneSolutionExp("0") == ["0"]

def test_symbol():
    """Ensure symbols work
    """
    assert doOneSolutionExp("x") == ["x"]

def test_operation():
    """Ensure operations work
    """
    assert doOneSolutionExp("1 + 1") == ["2"]

def test_equation():
    """Ensure equations are solved correctly
    """
    a = doOneSolutionEq("x - 1 = 0")
    assert a == ["x=1"]
