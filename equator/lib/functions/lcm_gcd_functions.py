"""Lowest common multiple amd greatest common denominator functions
"""

from decimal import Decimal

from .. import tokens

from .function import Function
from ..argset import ArgSet
from ..eq_except import EqFunctionArgumentException
from ..segment import Segment

def gcdAlgorithm(a: int, b: int) -> int:
    """An implementation of the Euclidean Algorithm for the greatest common
    divisor. Refer to: 
    https://en.wikipedia.org/wiki/Greatest_common_divisor#Euclidean_algorithm

    Args:
        a (int): first element
        b (int): second element, which is > a

    Returns:
        int: greatest common divisor
    """

    # Set b to it'smodulus with a
    b %= a

    # If that's zero, a is the GCD
    if b == 0: return a

    # Otherwise, recurse, swapping values around to maintain a < b condition
    return gcdAlgorithm(b, a)

def lcmAlgorithm(a: int, b: int) -> int:
    """An implementation of the greatest common divisor algorithm for the
    lowest common multiple. Refer to:
    https://en.wikipedia.org/wiki/Least_common_multiple#Using_the_greatest_common_divisor

    Args:
        a (int): first element
        b (int): second element, which is > a

    Returns:
        int: lowest common multiple
    """
    
    # Special case, all zero return zero to prevent divide by zero
    if a == b == 0:
        return 0

    return abs(a * b) / gcdAlgorithm(a, b)

class GcdFunction(Function):
    """Greatest common demononator of 2 integers
    """
    def __init__(self, on: Segment):
        super().__init__(tokens.Symbol("gcd"), on)
        
        # Ensure correct number of args
        # TODO: Make this a helper function
        if isinstance(on[0], ArgSet):
            args = on[0]
            if len(args) != 2:
                raise EqFunctionArgumentException("Wrong number of arguments "
                                                  "function gcd (expect 2, got"
                                                  f"{len(args)}"
                                                  )
        else:
            raise EqFunctionArgumentException("Not enough arguments for "
                                              "function gcd (expected "
                                              "2, got 1)"
                                              )
        
        # Ensure correct token type of arguments (Number, integer)
        args = on[0]
        
        try:
            a = Decimal(args[0].evaluate())
            b = Decimal(args[1].evaluate())
        
            assert int(a) == a and int(b) == b
        except:
            raise EqFunctionArgumentException("Incorrect argument types for"
                                              "function gcd (expected " 
                                              "integers)")
        
        
    def evaluate(self):
        args = self._on[0]
        a = int(args[0].evaluate())
        b = int(args[1].evaluate())
        
        if a > b: a, b = b, a

        return gcdAlgorithm(a, b)

class LcmFunction(Function):
    def __init__(self, on: Segment):
        super().__init__(tokens.Symbol("lcm"), on)
        
        # Ensure correct number of args
        # TODO: Make this a helper function
        if isinstance(on[0], ArgSet):
            args = on[0]
            if len(args) != 2:
                raise EqFunctionArgumentException("Wrong number of arguments "
                                                  "function lcm (expect 2, got"
                                                  f"{len(args)}"
                                                  )
        else:
            raise EqFunctionArgumentException("Not enough arguments for "
                                              "function lcm (expected "
                                              "2, got 1)"
                                              )
        
        # Ensure correct token type of arguments (Number, integer)
        args = on[0]
        
        try:
            a = Decimal(args[0].evaluate())
            b = Decimal(args[1].evaluate())
        
            assert int(a) == a and int(b) == b
        except:
            raise EqFunctionArgumentException("Incorrect argument types for"
                                              "function lcm (expected " 
                                              "integers)")
        
        
    def evaluate(self):
        args = self._on[0]
        a = int(args[0].evaluate())
        b = int(args[1].evaluate())
        
        if a > b: a, b = b, a

        return lcmAlgorithm(a, b)
        
