"""Ensure that all input (including whitespace) is preserved when tokenising
input
"""

from .helpers import Expression

def assertPreservation(inp: str):
    assert Expression(inp).getInputStr() == inp

def test_simple():
    """Sanity check"""
    assertPreservation("1+1")

def test_spaces():
    """Ensure that spaces are preserved
    """
    assertPreservation("1 + 1")
    assertPreservation("1 * 2 + 3")

def test_leading_trailing_spaces():
    """Ensure that leading and trailing spaces are preserved
    """
    assertPreservation(" 1 - 2  ")

def test_brackets():
    """Ensure that brackets are preserved properly
    """
    assertPreservation("2 * (3 + 4)")

def test_equations():
    """Ensure that equations are preserved properly too
    """
    assertPreservation("2 * x = 3 * (5 - x)")

def test_multi_statement():
    """Ensure that expressions with multiple statements are preserved
    """
    assertPreservation("6 * x = y + 3; 2*x - 24 = y; x+y")

def test_output_formatting():
    """Ensure that output formatting is also preserved
    """
    assertPreservation("pi * 3 -> num")
