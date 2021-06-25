"""Ensure that order of operations are considered correctly
"""

from lib.smart_equate import equate

def test_operations_add_subtract_multiply_divide():
    assert equate("1 + 1 * 2") == ["3"]
    assert equate("1 - 3 * 2") == ["-5"]
    assert equate("1 + 6 / 2") == ["4"]
    assert equate("8 - 4 / 2") == ["6"]

def test_operations_power():
    assert equate("2 + 2^2") == ["6"]
    assert equate("2 * 2^2") == ["8"]
    assert equate("2^3^2") == ["64"]

def test_leading_negative():
    assert equate("-1") == ["-1"]
    assert equate("-2^2") == ["-4"]
    assert equate("4^-1") == ["1 / 4"]
    assert equate("4 * -1") == ["-4"]

def test_brackets():
    assert equate("(2 + 1) / 3") == ["1"]
    assert equate("2^(1+1)") == ["4"]
    assert equate("2^(3^2)") == ["512"]
    assert equate("-(2 + 9)") == ["-11"]
