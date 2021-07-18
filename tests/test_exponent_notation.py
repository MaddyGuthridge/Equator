"""Ensure that exponent notation is calculated correctly

Author: Miguel Guthridge (hdsq@outlook.com.au)
"""

from .helpers import doOneSolutionExp

def test_basic():
    assert doOneSolutionExp("1E0") == ["1"]
    assert doOneSolutionExp("1e0") == ["1"]

def test_split_exponent():
    assert doOneSolutionExp("1E+1") == ["10"]
    assert doOneSolutionExp("1e+1") == ["10"]
    assert doOneSolutionExp("1E-1") == ["1/10"]
    assert doOneSolutionExp("1e-1") == ["1/10"]

def test_huge_exponent():
    assert doOneSolutionExp("1E-20") == ["1e-20"]
    assert doOneSolutionExp("1E+20") == ["1e+20"]

def test_decimal():
    assert doOneSolutionExp("1.75E3") == ["1750"]

def test_decimal_presentation_num():
    assert doOneSolutionExp("1.00000000") == ["1"]
    assert doOneSolutionExp("1.0000E-1") == ["1/10"]
    assert doOneSolutionExp("1E8") == ["100000000"]
    assert doOneSolutionExp("1E-8") == ["0.00000001"]
    
def test_deciaml_presentation_exp():
    assert doOneSolutionExp("1E9") == ["1e+9"]
    assert doOneSolutionExp("1E-9") == ["1e-9"]

def test_decimal_presentation_huge():
    assert doOneSolutionExp("1E32") == ["1e+32"]
    assert doOneSolutionExp("1E-32") == ["1e-32"]

def test_decimal_presentation_huge_no_round():
    """Ensure numbers are presented in scientific notation even if they're 
    really long, and can't just be rounded away"""
    assert doOneSolutionExp("52^8") == ["5.3459728531456e+13"]
