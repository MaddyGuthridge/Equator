"""Ensure that expressions have full code coverage
"""

from equator import Number, Constant, Symbol, Operator
from .helpers import doOneSolutionEq, doManySolutionEq, equate, Expression

def test_stringify():
    e = Expression("20 + 22")
    assert(e.getOutputStr() == "42")

def test_stringify_equation():
    e = Expression("20 + 22 = x")
    assert(e.getOutputStr() == "x = 42")

def test_stringify_mixed():
    e = Expression("20 + 22 = x; x + 27")
    assert(e.getOutputStr() == "x = 42\n69")

def test_stringify_multi_solution():
    e = Expression("x^2 + 2*x = 3")
    assert(e.getOutputStr() == 
"""[1]:
\tx = -3
[2]:
\tx = 1""")

def test_get_input_tokens():
    e = Expression("2 + pi - x")
    tokens = e.getInputTokens()
    exp = ([[
         Number("2"),
         Operator("+"),
         Constant("pi"),
         Operator("-"),
         Symbol("x")
     ]],
     "")
    assert(tokens == exp)

def test_get_output_tokens():
    e = Expression("20 + 22")
    exp = [([], [[
         Number("42")
     ]])]
    tokens = e.getOutputTokens()
    assert(tokens == exp)

def test_cache():
    e = Expression("42")
    assert(e.getOutputStr() == "42")
    assert(e.getOutputStr() == "42")
