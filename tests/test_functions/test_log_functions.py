"""Check exponent and logarithm functions work correctly
"""

from ..helpers import doOneSolutionExp

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

