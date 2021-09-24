"""Contains functions for doing operations on things.
Mostly used inside the evaluate functions of segments and the like

Author: Miguel Guthridge (hdsq@outlook.com.au)
"""

import math
import sympy as sym
from decimal import Decimal
from fractions import Fraction

from . import consts

from .eq_except import EqRangeError, EqInternalException

FUNCTION_OPERATOR_PRECEDENCE = 10
NO_OPERATION_PRECEDENCE = 10

def operatorPrecedence(op: str) -> int:
    """Returns an int representing the precedence of an operation

    Args:
        op (str): operator

    Returns:
        int: precedence
    """
    if   op in ['..']: return 4
    elif op in ['^']: return 3
    elif op in ['*', '/']: return 2
    elif op in ['+', '-']: return 1
    elif op in ['=']: return 0

def zeroRound(num):
    """Replaces values close to zero with zero
    And values close(ish) to infinity with infinity

    Args:
        num (Decimal | Any): value to check (will only round 
                             if can be converted to decimal)

    Returns:
        Decimal | Any: value, rounded if necessary
    """
    try:
        num = Decimal(float(num))
        if abs(num) < 10**(-consts.MAX_PRECISION):
            num = Decimal(0)
        elif abs(num) > 10**consts.MAX_PRECISION:
            num = Decimal("inf")
    except Exception:
        pass
    return num

def doOperation(operator: 'tokens.Operator', a, b):
    """Function for handling the logic of an operation
    In the future we may move to a method where operation token types implement
    their own operate function, to remove nasty things like this

    Args:
        operator (Operator Token): operation to do
        a (Operatable): left
        b (Operatable): right

    Raises:
        ValueError: unrecognised operation (something is horribly wrong)

    Returns:
        Operatable: result
    """
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
    elif operator == "..":
        raise EqRangeError("Range operator must be used in the context of a "
                           "function")
    else: # pragma: no cover
        raise EqInternalException("Unrecognised operation: " + operator)
    return res

def _doReduceSqrt(num: int):
    # Generate a list of all perfect squares up to num
    iterator = range(2, int(math.sqrt(num)) + 1)
    squares = [i**2 for i in iterator]
    roots = [i for i in iterator]
    multiple = 1
    for rt, sq in zip(roots, squares):
        if num % sq == 0:
            multiple *= rt
            num //= sq
    return multiple, num

def reduceSqrt(sq: Fraction):
    """Returns a reduced equivalent of a square root

    Args:
        sq (Decimal): input decimal (squared)

    Returns:
        tuple: (a [Fraction], b [Fractions]) representing a*sqrt(b)
    """
    # Operate on numerator and denominator separately
    
    numerator, denominator = sq.numerator, sq.denominator
    
    num_a, num_b = _doReduceSqrt(numerator)
    den_a, den_b = _doReduceSqrt(denominator)
    
    return Fraction(num_a, den_a), Fraction(num_b, den_b)

from . import tokens
