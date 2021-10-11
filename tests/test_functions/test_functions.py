"""Checks to make sure that functions provide the correct output

Author: Miguel Guthridge (hdsq@outlook.com.au)
"""

import pytest

from ..helpers import doOneSolutionExp, equate

from equator import EqFunctionArgumentException, EqFunctionNameException

################################################################################

def test_too_few_arguments():
    with pytest.raises(EqFunctionArgumentException):
        equate("gcd(1)")
    with pytest.raises(EqFunctionArgumentException):
        equate("lcm(1)")

def test_too_many_arguments():
    with pytest.raises(EqFunctionArgumentException):
        equate("sqrt(4, 9)")

def test_bad_function_name():
    with pytest.raises(EqFunctionNameException):
        equate("nonexistentfunction(1)")
