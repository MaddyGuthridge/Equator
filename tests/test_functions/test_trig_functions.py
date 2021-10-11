"""Check trig functions work correctly
"""

from ..helpers import doOneSolutionExp

def test_sin():
    assert doOneSolutionExp("sin(pi)") == ["0"]
    assert doOneSolutionExp("sin(pi/2)") == ["1"]
    assert doOneSolutionExp("sin(pi/3)") == ["1/2*sqrt(3)"]

def test_cos():
    assert doOneSolutionExp("cos(pi)") == ["-1"]
    assert doOneSolutionExp("cos(pi/2)") == ["0"]
    assert doOneSolutionExp("cos(pi/3)") == ["1/2"]

def test_tan():
    assert doOneSolutionExp("tan(pi)") == ["0"]
    assert doOneSolutionExp("tan(pi/4)") == ["1"]
    assert doOneSolutionExp("tan(pi/2)") == ["oo"]

def test_asin():
    assert doOneSolutionExp("asin(0)") == ["0"]
    assert doOneSolutionExp("asin(1)") == ["1/2*pi"]
    assert doOneSolutionExp("asin(1/2*sqrt(3))") == ["1/3*pi"]

def test_acos():
    assert doOneSolutionExp("acos(-1)") == ["pi"]
    assert doOneSolutionExp("acos(0)") == ["1/2*pi"]
    assert doOneSolutionExp("acos(1/2)") == ["1/3*pi"]

def test_atan():
    assert doOneSolutionExp("atan(0)") == ["0"]
    assert doOneSolutionExp("atan(1)") == ["1/4*pi"]
    assert doOneSolutionExp("atan(oo)") == ["1/2*pi"]
