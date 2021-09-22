"""Check degree and radian functions work correctly
"""

from ..helpers import doOneSolutionExp

def test_radians():
    assert doOneSolutionExp("rad(180)") == ["pi"]
    assert doOneSolutionExp("rad(180/pi)") == ["1"]
    assert doOneSolutionExp("rad(60)") == ["1/3*pi"]

def test_degrees():
    assert doOneSolutionExp("deg(pi)") == ["180"]
    assert doOneSolutionExp("deg(1/3*pi)") == ["60"]
    assert doOneSolutionExp("deg(pi/180)") == ["1"]
