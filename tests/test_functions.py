"""Checks to make sure that functions provide the correct output

Author: Miguel Guthridge (hdsq@outlook.com.au)
"""

import pytest

from .helpers import doOneSolutionExp, equate

from equator import EqFunctionException

################################################################################

def test_too_few_arguments():
    with pytest.raises(EqFunctionException):
        equate("gcd(1)")
    with pytest.raises(EqFunctionException):
        equate("lcm(1)")

def test_too_many_arguments():
    with pytest.raises(EqFunctionException):
        equate("sqrt(4, 9)")

################################################################################

# Simple functions

def test_negative():
    assert doOneSolutionExp("neg(1)") == ["-1"]
    assert doOneSolutionExp("neg(-1)") == ["1"]
    assert doOneSolutionExp("neg(0)") == ["0"]

def test_abs():
    assert doOneSolutionExp("abs(-1)") == ["1"]
    assert doOneSolutionExp("abs(1)") == ["1"]

def test_sqrt():
    assert doOneSolutionExp("sqrt(4)") == ["2"]

################################################################################

# Degrees and radians

def test_radians():
    assert doOneSolutionExp("rad(180)") == ["pi"]
    assert doOneSolutionExp("rad(180/pi)") == ["1"]
    assert doOneSolutionExp("rad(60)") == ["1/3*pi"]

def test_degrees():
    assert doOneSolutionExp("deg(pi)") == ["180"]
    assert doOneSolutionExp("deg(1/3*pi)") == ["60"]
    assert doOneSolutionExp("deg(pi/180)") == ["1"]

################################################################################

# Trig functions

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

################################################################################

# Logarithms and exponents

def test_exp():
    assert doOneSolutionExp("exp(0)") == ["1"]
    assert doOneSolutionExp("exp(1)") == ["e"]
    assert doOneSolutionExp("exp(5)") == ["e^5"]

def test_log10():
    assert doOneSolutionExp("log(1)") == ["0"]
    assert doOneSolutionExp("log(10)") == ["1"]
    assert doOneSolutionExp("log(100)") == ["2"]
    assert doOneSolutionExp("log(1/10)") == ["-1"]

def test_ln():
    assert doOneSolutionExp("ln(1)") == ["0"]
    assert doOneSolutionExp("ln(e)") == ["1"]
    assert doOneSolutionExp("ln(exp(5))") == ["5"]

def test_log_n():
    assert doOneSolutionExp("log_2(4)") == ["2"]
    assert doOneSolutionExp("log_10(1000)") == ["3"]
    assert doOneSolutionExp("log_3(3)") == ["1"]
    #assert doOneSolutionExp("log_0.5(2)") == ["-1"]
