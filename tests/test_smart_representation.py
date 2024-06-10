"""Ensure that calculations involving smart representation work correctly
This includes representing in terms of pi, e, and as square roots

Author: Maddy Guthridge (hdsq@outlook.com.au)
"""

from .helpers import doOneSolutionExp

def test_pi():
    assert doOneSolutionExp("pi") == ["pi"]
    assert doOneSolutionExp("pi * 2") == ["2*pi"]
    assert doOneSolutionExp("1/3 * pi") == ["1/3*pi"]

def test_sqrt():
    assert doOneSolutionExp("sqrt(3)/sqrt(4)") == ["1/2*sqrt(3)"]
    assert doOneSolutionExp("sqrt(8)") == ["2*sqrt(2)"]

def test_e():
    assert doOneSolutionExp("exp(1)") == ["e"]
    assert doOneSolutionExp("exp(10)") == ["e^10"]
    assert doOneSolutionExp("exp(-5)") == ["e^-5"]
