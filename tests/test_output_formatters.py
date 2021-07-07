"""Ensure that output formatters format output correctly
"""

from .helpers import simplifyExp

from lib.smart_equate import equate

def test_output_num():
    # Multiply by 10 to ensure that it isn't doing it in scientific notation
    assert equate("pi*10 -> num")[0].startswith("31.415")
    # Also check for e
    assert equate("e -> num")[0].startswith("2.718")
    # And sqrt(2)
    assert equate("sqrt(2) -> num")[0].startswith("1.414")
    # And a fraction
    assert equate("1/10 -> num") == ["0.1"]
    # And a tiny fraction (it should go into scientific)
    assert equate("1/10^12 -> num") == ["1e-12"]

def test_output_dec():
    # Ensure that it's always presented as a decimal, no matter the size
    assert equate("10^100 -> dec") == ["1" + "0"*100]
    assert equate("10^-10 -> dec") == ["0.0000000001"]

def test_output_sci():
    # Esnure its always scientific notation
    assert equate("1 -> sci") == ["1e+0"]
    assert equate("103.4 -> sci") == ["1.034e+2"]
    assert equate("23/1000 -> sci") == ["2.3e-2"]
