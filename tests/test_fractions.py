"""Ensure that results are presented as fractions where possible

Author: Maddy Guthridge (hdsq@outlook.com.au)
"""

from .helpers import doOneSolutionExp

def test_basic():
    assert doOneSolutionExp("1/2") == ["1/2"]
    assert doOneSolutionExp("0.5") == ["1/2"]

def test_with_symbols():
    #assert doOneSolutionExp("1/2 * x") == ["x/2"]
    pass
