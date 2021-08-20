"""Contains functions for doing operations on things.
Mostly used inside the evaluate functions of segments and the like

Author: Miguel Guthridge (hdsq@outlook.com.au)
"""

import math
import sympy as sym
from decimal import Decimal
from fractions import Fraction

from . import consts

from .eq_except import EqOperatorException, EqFunctionException

FUNCTION_OPERATOR_PRECEDENCE = 10
NO_OPERATION_PRECEDENCE = 10

def operatorPrecedence(op: str) -> int:
    """Returns an int representing the precedence of an operation

    Args:
        op (str): operator

    Returns:
        int: precedence
    """
    if   op in ['^']: return 3
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

def doOperation(operator: str, a, b):
    """Function for handling the logic of an operation
    In the future we may move to a method where operation token types implement
    their own operate function, to remove nasty things like this

    Args:
        operator (str): operation to do
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
    else:
        raise EqOperatorException("Unrecognised operation: " + operator)
    return res

def doFunction(func: str, a):
    """Function for handling logic of evaluating functions.
    In the future this may be moved into subclasses for each function, in the
    hope of tidying things up

    Args:
        func (str): function to do
        a (Operatable): thing to operate on

    Returns:
        Operatable: result
    """
    if func == "sqrt":
        return sym.sqrt(a)
    elif func == "sin":
        return zeroRound(sym.sin(a))
    elif func == "cos":
        return zeroRound(sym.cos(a))
    elif func == "tan":
        return zeroRound(sym.tan(a))
    elif func == "asin":
        return zeroRound(sym.asin(a))
    elif func == "acos":
        return zeroRound(sym.acos(a))
    elif func == "atan":
        return zeroRound(sym.atan(a))
    elif func == "abs":
        return sym.Abs(a)
    elif func == "deg":
        return a * 180 / consts.NUMERIC_CONSTANTS["pi"]
    elif func == "rad":
        return a / 180 * consts.NUMERIC_CONSTANTS["pi"]
    elif func == consts.NEGATE:
        return -a
    elif func == "exp":
        return sym.exp(a)
    elif func == "log":
        return sym.log(a, 10.0)
    elif func == "ln":
        return sym.log(a)
    elif func.startswith("log_"):
        try:
            base = Decimal(func.replace("log_", ""))
        except:
            raise EqFunctionException(f"Bad base for logarithm \"{func}\"")
        return sym.log(a, base)

def getConstant(const: str):
    """Returns the representation of a constant as a stringified decimal
    r the original string if it isn't a constant

    Args:
        const (str): potential constant to replace

    Returns:
        str: representation of constant if applicable otherwise original str
    """
    if const in consts.NUMERIC_CONSTANTS:
        return str(consts.NUMERIC_CONSTANTS[const])
    else:
        return const

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
