import math
import sympy as sym
from decimal import Decimal
from fractions import Fraction

from . import consts

FUNCTION_OPERATOR_PRECEDENCE = 10
NO_OPERATION_PRECEDENCE = 10

def operatorPrecedence(op: str):
    if   op in ['^']: return 3
    elif op in ['*', '/']: return 2
    elif op in ['+', '-']: return 1
    elif op in ['=']: return 0

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
    elif func == consts.NEGATE:
        return -a

def getConstant(const: str):
    if const == "pi":
        return str(math.pi)
    if const == "I":
        return sym.sqrt(-1)
    else:
        return const
