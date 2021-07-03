"""Ensure that eponent notation is calculated correctly
"""

from .helpers import simplifyExp

from lib.smart_equate import equate

def test_basic():
    assert simplifyExp(equate("1E0")) == ["1"]

def test_split_exponent():
    assert simplifyExp(equate("1E+1")) == ["10"]
    assert simplifyExp(equate("1E-1")) == ["1/10"]

def test_huge_exponent():
    assert simplifyExp(equate("1E-20")) == ["1E-20"]
    assert simplifyExp(equate("1E+20")) == ["1E+20"]

def test_decimal():
    assert simplifyExp(equate("1.75E3")) == ["1750"]

def test_decimal_presentation_num():
    assert equate("1.00000000") == ["1"]
    assert equate("1.0000E-1") == ["1/10"]
    assert equate("1E8") == ["100000000"]
    assert equate("1E-8") == ["0.00000001"]
    
def test_deciaml_presentation_exp():
    assert equate("1E9") == ["1E+9"]
    assert equate("1E-9") == ["1E-9"]

def test_decimal_presentation_huge():
    assert equate("1E32") == ["1E+32"]
    assert equate("1E-32") == ["1E-32"]
