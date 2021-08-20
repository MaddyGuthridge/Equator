"""Ensure that output formatters format output correctly

Author: Miguel Guthridge (hdsq@outlook.com.au)
"""

from .helpers import doOneSolutionExp, doOneSolutionEq

def test_output_num():
    # Multiply by 10 to ensure that it isn't doing it in scientific notation
    assert doOneSolutionExp("pi*10 -> num")[0].startswith("31.415")
    # Also check for e
    assert doOneSolutionExp("e -> num")[0].startswith("2.718")
    # And sqrt(2)
    assert doOneSolutionExp("sqrt(2) -> num")[0].startswith("1.414")
    # And a fraction
    assert doOneSolutionExp("1/10 -> num") == ["0.1"]
    # And a tiny fraction (it should go into scientific)
    assert doOneSolutionExp("1/10^12 -> num") == ["1e-12"]

def test_output_dec():
    """Ensure that it's always presented as a decimal, no matter the size"""
    assert doOneSolutionExp("10^100 -> dec") == ["1" + "0"*100]
    assert doOneSolutionExp("10^-10 -> dec") == ["0.0000000001"]

def test_output_sci():
    """Ensure its always scientific notation"""
    assert doOneSolutionExp("1 -> sci") == ["1e+0"]
    assert doOneSolutionExp("103.4 -> sci") == ["1.034e+2"]
    assert doOneSolutionExp("23/1000 -> sci") == ["2.3e-2"]

def test_output_bad_type():
    """Ensure that when an incorrect format type is chosen, it will default
    to smart formatting"""
    assert doOneSolutionExp("sqrt(2) -> notAFormat") == ["sqrt(2)"]

def test_equations():
    """Ensure formatting is applied to sets of equations"""
    assert doOneSolutionEq("x*4 = 2 -> num") == ["x=0.5"]
    assert doOneSolutionEq("x*4 = 2 -> sci") == ["x=5e-1"]
    assert doOneSolutionEq("x*1e+10 = 1 -> dec") == ["x=0.0000000001"]
