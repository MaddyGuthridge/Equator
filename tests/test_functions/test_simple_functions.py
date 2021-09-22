"""Check simple functions (neg, abs, sqrt) work correctly
"""

from ..helpers import doOneSolutionExp

def test_negative():
    assert doOneSolutionExp("neg(1)") == ["-1"]
    assert doOneSolutionExp("neg(-1)") == ["1"]
    assert doOneSolutionExp("neg(0)") == ["0"]

def test_abs():
    assert doOneSolutionExp("abs(-1)") == ["1"]
    assert doOneSolutionExp("abs(1)") == ["1"]

def test_sqrt():
    assert doOneSolutionExp("sqrt(4)") == ["2"]
