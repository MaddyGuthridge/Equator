import sympy as sym

from fractions import Fraction
from decimal import Decimal

from . import operation
from . import consts

class Token:
    """Token base type
    All tokens are derived from this
    """
    def __init__(self, value: str) -> None:
        self._contents = value
    
    def __str__(self) -> str:
        return self._contents
    
    def __repr__(self) -> str:
        return self._contents

    def str_decimal(self):
        """Returns self as a decimal where possible

        Returns:
            str: contents as a decimal if possible
        """
        return self._contents

    def evaluate(self):
        return self._contents
    
    def getOperatorPrecedence(self):
        return operation.NO_OPERATION_PRECEDENCE

class Operator(Token):
    """Token representing an operator
    Evaluate returns operator string
    """

    def __eq__(self, o: object) -> bool:
        if isinstance(o, str):
            return o == self._contents

class Number(Token):
    """Token representing a number
    Evaluate returns numberified version
    """
    def evaluate(self):
        return Decimal(self._contents)

    def str_decimal(self):
        return str(self.evaluate())

    def __str__(self) -> str:
        ev = self.evaluate()
        
        # Check for zeros
        if ev == 0:
            return "0"
        
        # Check for multiples of pi
        pi_div = str(Fraction(ev / consts.CONSTANTS["pi"]).limit_denominator(consts.FRACTION_DENOM_LIMITER))
        if len(pi_div) < 10:
            if pi_div == "1":
                return "pi"
            return pi_div + "*pi"
        
        
        # Present as fraction if possible
        fract = str(Fraction(ev).limit_denominator(consts.FRACTION_DENOM_LIMITER))
        if len(fract) < 10:
            return fract
        
        # Check for square roots
        sqr = Fraction(ev ** 2).limit_denominator(consts.FRACTION_DENOM_LIMITER)
        if len(str(sqr)) < 10:
            mul, rt = operation.reduceSqrt(sqr)
            mul = f"{mul}*" if mul != 1 else ""
            return f"{mul}sqrt({rt})"
        
        return str(ev)
        

class Constant(Number):
    """Token representing a constant such as pi. 
    Stringifies to the name of the constant
    """
    def evaluate(self):
        return consts.CONSTANTS[self._contents]
    
    def __str__(self) -> str:
        return self._contents

class Symbol(Token):
    """Token representing a symbol
    Evaluate regeisters and returns a SymPy symbol
    
    Note, depending on context, this could be a function
    """
    def evaluate(self):
        return sym.Symbol(self._contents)
