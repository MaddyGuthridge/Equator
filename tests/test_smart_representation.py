"""Ensure that calculations involving smart representation work correctly
"""

from .helpers import simplifyExp

from lib.smart_equate import equate

def test_pi():
    assert equate("pi") == ["pi"]
    assert equate("pi * 2") == ["2*pi"]
    assert equate("1/3 * pi") == ["1/3*pi"]

def test_sqrt():
    assert equate("sqrt(3)/sqrt(4)") == ["sqrt(3/4)"]
    assert equate("sqrt(8)") == ["2*sqrt(2)"]
