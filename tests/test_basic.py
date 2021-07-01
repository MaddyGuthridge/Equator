"""Ensure that the most basic of the basic features work
"""
from lib.smart_equate import equate

from .helpers import simplifyEq

def test_constant():
    """Ensure constants work
    """
    assert equate("1") == ["1"]
    assert equate("0") == ["0"]

def test_symbol():
    """Ensure symbols work
    """
    assert equate("x") == ["x"]

def test_operation():
    """Ensure operations work
    """
    assert equate("1 + 1") == ["2"]

def test_equation():
    """Ensure equations are solved correctly
    """
    a = simplifyEq(equate("x - 1 = 0"))
    assert a == [{'x': '1'}]
