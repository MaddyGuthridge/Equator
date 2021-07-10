"""Ensure that results are presented as fractions where possible

Author: Miguel Guthridge (hdsq@outlook.com.au)
"""

from ..lib.smart_equate import equate

from .helpers import simplifyExp

def test_basic():
    assert simplifyExp(equate("1/2")) == ["1/2"]
    assert simplifyExp(equate("0.5")) == ["1/2"]

def test_with_symbols():
    #assert simplifyExp(equate("1/2 * x")) == ["x/2"]
    pass
