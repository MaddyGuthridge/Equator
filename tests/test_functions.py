"""Checks to make sure that functions provide the correct output
"""

from .helpers import simplifyExp

from lib.smart_equate import equate

def test_negative():
    assert equate("neg(1)") == ["-1"]
    assert equate("neg(-1)") == ["1"]
    assert equate("neg(0)") == ["0"]

def test_radians():
    assert simplifyExp(equate("rad(180)")) == ["pi"]
    assert simplifyExp(equate("rad(180/pi)")) == ["1"]
    assert simplifyExp(equate("rad(60)")) == ["1/3*pi"]

def test_degrees():
    assert simplifyExp(equate("deg(pi)")) == ["180"]
    assert simplifyExp(equate("deg(1/3*pi)")) == ["60"]
    assert simplifyExp(equate("deg(pi/180)")) == ["1"]

def test_abs():
    assert simplifyExp(equate("abs(-1)")) == ["1"]
    assert simplifyExp(equate("abs(1)")) == ["1"]

def test_sqrt():
    assert simplifyExp(equate("sqrt(4)")) == ["2"]
    #assert simplifyExp(equate("sqrt(x^2)")) == ["x"]

def test_sin():
    assert simplifyExp(equate("sin(pi)")) == ["0"]
    assert simplifyExp(equate("sin(pi/2)")) == ["1"]
    assert simplifyExp(equate("sin(pi/3)")) == ["1/2*sqrt(3)"]

def test_cos():
    assert simplifyExp(equate("cos(pi)")) == ["-1"]
    assert simplifyExp(equate("cos(pi/2)")) == ["0"]
    assert simplifyExp(equate("cos(pi/3)")) == ["1/2"]
