import math
from decimal import Decimal
from fractions import Fraction

from .sym import sympy as sym

def conditionalDecimal(a):
    return Decimal(str(float(a))) if isinstance(a, Fraction) else a

def conditionalFraction(a):
    if isinstance(a, Decimal):
        fract = Fraction(a)
        if len(str(fract)) < 10:
            return fract
        else:
            return a
    else:
        return a

def doOperation(operator: str, a, b):
    a = conditionalDecimal(a)
    b = conditionalDecimal(b)
    if operator == '^':
        res = a ** b
    elif operator == '*':
        res = a * b
    elif operator == '/':
        res = a / b
    elif operator == '+':
        res = a + b
    elif operator == '-':
        res = a - b
    elif operator == '=':
        res = sym.Eq(a, b)
    else:
        raise ValueError("Unrecognised operation: " + operator)
    return conditionalFraction(res)

def doFunction(func: str, a):
    if func == "sqrt":
        return sym.sqrt(a)
    elif func == "sin":
        return sym.sin(a)
    elif func == "cos":
        return sym.cos(a)
    elif func == "tan":
        return sym.tan(a)
    elif func == "abs":
        return sym.Abs(a)
    elif func == "deg":
        return sym.deg(a)
    elif func == "rad":
        return sym.rad(a)

def getConstant(const: str):
    if const == "pi":
        return str(math.pi)
    else:
        return const
